import yaml
import multiprocessing
import seaborn as sns
sns.set()
from src.BasicGraphs import BasicGraph
from src.TopicModeling import TopicModeling
from src.DataProcessing import DataProcessing
from src.BasicGraphs import BasicGraph
from src.SpacyNLP import SpacyNLP
import pandas as pd
import os
from src.RecapPageGenerator import RecapPageGenerator



def main():
    # Config
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    # Access configuration values
    gName = config["chat_group_name"]                    # Chat group name
    raw_path = config["paths"]["raw"]               # Path to the raw chat file
    processed_path = config["paths"]["processed"]   # Path to the processed dataset
    outputs_path = config["paths"]["outputs"]       # Path to save outputs
    language = config["language"]                   # Chat language
    outputs_path_TM = config["paths"]["outputsTM"]  # Path to save outputs (Topic Modeling)
    api_key_openai = config['api_key_openai']       # Your API key (OpenAI) if you want use the chatGPT's representation model
    n_top_users = config['parameters_for_graphs']['n_top_users']  # Number of top users displayed in the chart
    n_top_emoji = config['parameters_for_graphs']['n_top_emoji']  # Number of top emojis displayed in the chart
    n_topics_vis_pie = config['parameters_for_graphs']['n_topics_vis_pie']  # Number of topics displayed in the pie chart

    # Make sure the directory exists
    os.makedirs(outputs_path, exist_ok=True)
    os.makedirs(outputs_path_TM, exist_ok=True)

    NLP = SpacyNLP(language)
    # Chat cleanup and loading
    df_clean = DataProcessing.load_and_clean_data(gName, raw_path, processed_path)
    print("✅ done!\n")

    # Get stopwords for the language (wordcloud)
    stopwords = NLP.get_stopwords()
    print("✅ done!\n")

    # ------------------------------ BasicGraphs ------------------------------
    basic_graph = BasicGraph(df_clean, outputs_path)
    
    # Crea i singoli grafici
    basic_graph.create_heatmap()            # For PNG : basic_graph.create_heatmap(html = False) 
    basic_graph.create_top_users(n_top_users)          # For PNG : basic_graph.create_top_users(html = False)
    basic_graph.create_emoji_chart(n_top_emoji)        # For PNG : basic_graph.create_emoji_chart(html = False)
    basic_graph.create_wordcloud(stopwords) # For PNG : basic_graph.create_wordcloud(stopwords, html = False)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ------------------------------ Topic Modeling spaCy ------------------------------
    # Analisi topic
    print("📑 Topic analysis...")
    topic_analyzer = TopicModeling(language, list(stopwords), api_key_openai, outputs_path_TM)
    topics, probs = topic_analyzer.fit_transform(df_clean)
    
    # get df of topic
    df_topic = topic_analyzer.get_csv()
    if outputs_path_TM:
        os.makedirs(outputs_path_TM, exist_ok=True)
        df_topic.to_csv(outputs_path_TM + "topic_info.csv", index=False)


    # Salva visualizzazioni
    topic_analyzer.save_vis_hierarchy()
    topic_analyzer.save_vis_map()    
    topic_analyzer.save_vis_barchart()
    topic_analyzer.save_vis_topics_over_time()
    custom_colors = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8']
    topic_analyzer.save_vis_pie(
        n_topics_vis_pie,
        exclude_topics=[-1],
        max_title_length=40,
        n_examples=3,
        color_sequence=custom_colors
    )
    print("\n✅ Analysis completed!")
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



    # ------------------------------ Recap HTML ------------------------------
    # Set the output directory and base URL (e.g., local file for testing)
    base_url = f"file://{os.path.abspath(outputs_path)}/"
    
    
    start_date = df_clean['date'].min().strftime('%d/%m/%Y')
    end_date = df_clean['date'].max().strftime('%d/%m/%Y')

    # Create an instance of the generator
    generator = RecapPageGenerator(
        outputs_path = outputs_path, 
        base_url = base_url,
        group_name = gName,
        start_date= start_date,
        end_date=  end_date
        )
    
    # Add optional graph, 
    # you can duplicate this if you have another graph to show
    generator.add_graph(
        graph_id="custom1",
        graph_url=f"{base_url}TopicModeling//topic_topics_over_time.html",
        title="Topics Over Time",
        icon="fas fa-chart-line"
    )
    
    # Save HTML 
    generator.save_page()
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    print(f'\n💾 All charts have been successfully saved in: {outputs_path}')


if __name__ == '__main__':
    multiprocessing.freeze_support()  # Necessary if the program is frozen into an executable

    main()