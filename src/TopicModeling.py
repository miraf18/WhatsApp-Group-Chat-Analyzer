from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from hdbscan import HDBSCAN
import openai
from bertopic.representation import OpenAI
from bertopic.representation import KeyBERTInspired
import plotly.express as px
from plotly.express import pie
import plotly.graph_objects as go
from textwrap import wrap
import pandas as pd
from typing import Optional, List
import re
import os

class TopicModeling:
    def __init__(self, language, stopwords, api_key_openai, outputs_path_TM):

        # Initialize the BERTopic analyzer
        print("⏳ Initialize the BERTopic analyzer (for Topic Modeling)...")
        
        self.outputs_path_TM = outputs_path_TM
        # If you want to use a representation model with ChatGPT:
        # Configure OpenAI-compatible client and testing API 
        self.openai_client = None
        if api_key_openai:
            try:
                # Initialize the client with a global timeout
                self.openai_client = openai.OpenAI(
                    api_key=api_key_openai,
                    timeout=30.0,  # Global timeout for all requests
                    max_retries=3  # Maximum number of retry attempts
                )
                # Connection test with updated parameters
                test_response = self.openai_client.chat.completions.create(
                    messages=[{"role": "user", "content": "Connectivity test"}],
                    model="gpt-3.5-turbo",
                    timeout=15  # Correct parameter for v1.x (request_timeout is deprecated)
                )
                print(f"✅ API test successful. Tokens used: {test_response.usage.total_tokens}")

            except openai.APIConnectionError as e:
                print("❌ Permanent connection error. Possible reasons:")
                print("- Unstable internet connection")
                print("- Firewall/proxy blocking")
                print("- Incorrect DNS configuration")
                raise e
            except Exception as e:
                print(f"❌ Error during OpenAI initialization: {str(e)}")
                self.openai_client = None

        # Configure representation model (with ChatGPT or KeyBERT)
        if self.openai_client:
            self.representation_model = OpenAI(
                client=self.openai_client,
                model="gpt-3.5-turbo-0125",     # Specific model for consistency
                delay_in_seconds=20,            # Increases the delay between requests
                chat=True
            )
        else:
            # If API key is not present, use the Keybert model
            print("⚠️ Falling back to KeyBERT for local representations")
            self.representation_model = KeyBERTInspired()


        # Initialize the embedding model, using a SentenceTransformer model ('paraphrase-multilingual-MiniLM-L12-v2')
        # Trained on 50 different languages, a good balance between speed and accuracy...
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


        # Initialize HDBSCAN for Clustering
        self.hdbscan_model = HDBSCAN(
            min_cluster_size=17,            # Groups of at least 17 messages
            min_samples=3,                  # Reduces sensitivity to noise
            cluster_selection_epsilon=0.3,  # Merges nearby clusters
        )

        # Initialize the Vectorizer Model.
        # Unlike simple stopword removal, this model also constructs n-grams and filters terms based on frequency,
        # providing a more robust feature extraction process.
        self.vectorizer_model = CountVectorizer(
            stop_words=stopwords,
            ngram_range=(1, 3),  # Considers unigrams, bigrams, and trigrams
            min_df=2,            # Excludes terms that appear too rarely
            max_df=0.95,         # Excludes terms that appear too frequently
        )
            

        # Initialize BERTopic
        self.topic_model = BERTopic(
            embedding_model = self.embedding_model, 
            hdbscan_model= self.hdbscan_model, 
            language=language,
            vectorizer_model = self.vectorizer_model,
            representation_model = self.representation_model,
            nr_topics = "auto",
            verbose=True
        )

        print("✅ BERTopic Analyzer successfully initialized")
    
    # Train and transform the BERTopic model on the provided dataframe
    def fit_transform(self, df, text_column='message'):
        # Train the BERTopic model on the messages
        print("⏳ Training BERTopic model...")
        self.documents = df[text_column].fillna('')
        self.timestamps = df['date'].tolist()
        topics, probs = self.topic_model.fit_transform(self.documents)
        
        # Reduce the number of topics based on the documents
        self.topic_model.reduce_topics(self.documents)
        
        return topics, probs

    # Retrieve the topic information as a DataFrame
    def get_csv(self):
        topic_df = self.topic_model.get_topic_info()
        return topic_df
    


    ##### For Visualization: ##### 
    
    # Hierarchical visualization of the topics
    def save_vis_hierarchy(self):
        if self.outputs_path_TM:
            os.makedirs(self.outputs_path_TM, exist_ok=True)
            output_path_hierarchy = os.path.join(self.outputs_path_TM, "topic_hierarchy.html")
            self.topic_model.visualize_hierarchy().write_html(output_path_hierarchy)
    
    # Intertopic distance visualization
    def save_vis_map(self):
        if self.outputs_path_TM:
            os.makedirs(self.outputs_path_TM, exist_ok=True)
            output_path_map = os.path.join(self.outputs_path_TM, "topic_map.html")
            self.topic_model.visualize_topics().write_html(output_path_map)

    # Barchart visualization
    def save_vis_barchart(self, ):
        if self.outputs_path_TM:
            os.makedirs(self.outputs_path_TM, exist_ok=True)
            output_path_barchart = os.path.join(self.outputs_path_TM, "topic_barchart.html")
            self.topic_model.visualize_barchart().write_html(output_path_barchart) 

    # topics_over_time visualization (nr_bins=24)
    # nr_bins: Number of time intervals (bins) used to group the timestamps.
    #          This parameter allows you to aggregate the data to reduce the number of unique timestamps,
    #          making it easier to visualize the evolution of topics over time. 
    def save_vis_topics_over_time(self):
        topics_over_time = self.topic_model.topics_over_time(self.documents, self.timestamps, nr_bins=24)
        if self.outputs_path_TM:
            os.makedirs(self.outputs_path_TM, exist_ok=True)
            output_path_barchart = os.path.join(self.outputs_path_TM, "topic_topics_over_time.html")
            self.topic_model.visualize_topics_over_time(topics_over_time).write_html(output_path_barchart) 

    # Pie visualization 
    def save_vis_pie(
        self,
        n_topics: int,                              
        exclude_topics: List[int] = [-1],
        max_title_length: int = 30,
        n_examples: int = 2,
        color_sequence: Optional[List[str]] = None
    ):

        # Filter out excluded topics
        df = self.topic_model.get_topic_info()
        # Filter out excluded topics
        df = df[~df['Topic'].isin(exclude_topics)]

        # Sort by Count and take top N topics
        df = df.nlargest(n_topics-1, 'Count')

        def clean_representation(rep):
            if isinstance(rep, list):
                rep = " ".join(rep)
            cleaned = re.sub(r'\s+', ' ', rep.strip('[]\'\"').strip())
            if len(cleaned) > max_title_length:
                cleaned = cleaned[:max_title_length] + "..."
            return cleaned

        def clean_text(text):
            # Clean text by removing extra spaces and normalizing punctuation
            # Remove extra spaces
            text = re.sub(r'\s+', ' ', text.strip())
            # Add space after punctuation if missing
            text = re.sub(r'([.!?])([^\s])', r'\1 \2', text)
            # Remove space before punctuation
            text = re.sub(r'\s+([.!?])', r'\1', text)
            return text

        def format_example(text):
            # Format a single example with proper line breaks and spacing
            # Clean the text first
            text = clean_text(text)
            
            # Split on punctuation marks
            sentences = re.split(r'(?<=[.!?])\s+', text)
            
            # Clean each sentence and join with line breaks
            return '<br>'.join(s.strip() for s in sentences if s.strip())

        def clean_docs(docs_str):
            try:
                # If docs_str is already a list
                if isinstance(docs_str, list):
                    docs_list = docs_str
                else:
                    # If it's a string representing a list
                    docs_str = docs_str.strip('"\'')
                    if docs_str.startswith('[') and docs_str.endswith(']'):
                        docs_str = docs_str[1:-1]
                        import re
                        docs_list = [s.strip().strip('\'\"') for s in re.findall(r'\'[^\']*\'|\"[^\"]*\"|\S+', docs_str)]
                    else:
                        docs_list = [docs_str]
                    
                # Take the first n_examples and format each one
                formatted_docs = []
                for doc in docs_list[:n_examples]:
                    if isinstance(doc, str):  # Ensure it's a string
                        formatted = format_example(doc)
                        if formatted:  # Only if it's not empty
                            formatted_docs.append(formatted)
                
                # Join examples with double line breaks
                return '<br><br>'.join(formatted_docs)
            except Exception as e:
                print(f"Error in clean_docs: {str(e)}")
                return "Examples not available"

        # Process the data
        df['clean_representation'] = df['Representation'].apply(clean_representation)
        df['clean_docs'] = df['Representative_Docs'].apply(clean_docs)

        # Create hover text with better formatting
        df['hover_text'] = df.apply(
            lambda row: f"<b>Topic:</b> {row['clean_representation']}<br><br>" +
                        f"<b>Count:</b> {row['Count']}<br><br>" +
                        f"<b>Examples:</b><br>{row['clean_docs']}", 
            axis=1
        )

        # Create the pie chart
        fig = px.pie(
            df,
            values='Count',
            names='clean_representation',
            hover_data=['hover_text'],
            color_discrete_sequence=color_sequence
        )

        # Update layout for better presentation
        fig.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate="%{customdata[0]}<extra></extra>"
        )

        fig.update_layout(
            hoverlabel={
                'align': 'left',
                'bgcolor': 'white',
                'font_size': 12,
                'font_family': 'Arial'
            },
            showlegend=True,
            legend={'orientation': 'h', 'y': -0.1},
        )

        # Save the figure (HTML)
        if self.outputs_path_TM:
            os.makedirs(self.outputs_path_TM, exist_ok=True)
            output_path_pie = os.path.join(self.outputs_path_TM, "topic_pie.html")
            fig.write_html(output_path_pie)
   
