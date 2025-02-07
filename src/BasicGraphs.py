import pandas as pd
import plotly.express as px
import emoji
from collections import defaultdict
from wordcloud import WordCloud






class BasicGraph:

    def __init__(self, df : pd.DataFrame, outputs_path : str):
        self.df = df.copy()
        self.outputs_path = outputs_path

    # Creating a heatmap
    def create_heatmap(self, html : bool = True) -> None:
        print("⏳ Creating  a heatmap...")

        self.df['hour'] = self.df['date'].dt.hour
        self.df['day_of_week'] = self.df['date'].dt.day_name()

        # Sort the days of the week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.df['day_of_week'] = (
            pd.Categorical(self.df['day_of_week'], 
            categories=day_order, 
            ordered=True)
        )
        
        # Create a matrix for the heatmap
        heatmap_data = (
            self.df.groupby(['day_of_week', 'hour'], observed=True)
            .size()
            .reset_index(name='messages')
            .sort_values(['day_of_week', 'hour'])   
        )
        
        fig = px.density_heatmap(
            heatmap_data,
            y='hour',
            x='day_of_week',
            z='messages',
            color_continuous_scale='greens',
            labels={
                'hour': 'Hour of the day',
                'day_of_week': 'Weekday',
                'counts': 'Messages'
            },
        )
        fig.update_layout(
            xaxis_tickangle=-45,                         
            font=dict(size=12),
        )

        
        fig.update_coloraxes(showscale=False)

        if html:
            # Save HTML file
            fig.write_html( self.outputs_path + "heatmap.html")
        else:
            # Save PNG file
            fig.write_image( self.outputs_path + "heatmap.png") 

        print(f"✅ File saved in: { self.outputs_path}\n")

    # Creating a Top Users barchart
    def create_top_users(self, n_top_users: int = 10, html: bool = True) -> None:
        print("⏳ Creating  a Top Users barchart...")
        
        # Count Messages
        user_counts = self.df['user'].value_counts().reset_index()
        user_counts.columns = ['user', 'count']

        # Top 10 Users
        top_users = user_counts.head(n_top_users)

        # Create barchart
        fig = px.bar(
            top_users,
            x='user',      
            y='count',
            labels={'user': 'Users', 'count': 'Message Count'},
            text='count',
            color='count', 
            color_continuous_scale='greens',
        )
        fig.update_layout(
            font=dict(size=12),
            xaxis_tickangle=-45,
            barcornerradius = 12
            )
        
        fig.update_coloraxes(showscale=False)
        

        if html:
            # Save HTML file
            fig.write_html( self.outputs_path + "TopUsers.html")
        else:
            # Save PNG file
            fig.write_image( self.outputs_path + "TopUsers.png" ) 

        print(f"✅ File saved in: { self.outputs_path}\n")

    # Creating a Top emoji chart
    def create_emoji_chart(self, n_top_emoji: int = 5, html: bool = True) -> None:
        print("⏳ Creating an emoji chart...")
    
        # Count the emojis
        emoji_freq = defaultdict(int)
        for message in self.df['message']:
            emojis = ''.join(char for char in message if char in emoji.EMOJI_DATA)
            for emoji_char in emojis:
                emoji_freq[emoji_char] += 1

        # Create a DataFrame with the top emojis
        df_emoji = pd.DataFrame(
            sorted(emoji_freq.items(), key=lambda x: x[1], reverse=True)[:n_top_emoji],
            columns=['Emoji', 'Count']
        )

        # Create the chart
        fig = px.bar(
            df_emoji,
            y='Emoji',
            x='Count',
            color='Count',
            color_continuous_scale='greens',
            orientation='h',
            text = 'Emoji',
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            font=dict(size=12),
            xaxis_tickangle=-45,
            barcornerradius = 12
        )
        
        fig.update_coloraxes(showscale=False)


        if html:
            # Save HTML file
            fig.write_html( self.outputs_path + "EmojiChart.html" ) 
        else:
            # Save PNG file
            fig.write_image( self.outputs_path + "EmojiChart.png" ) 
            
        print(f"✅ File saved in: { self.outputs_path}\n")
    
    # Creating a WordCloud
    def create_wordcloud(self, stopwords: set) -> None:
        print("⏳ Creating an emoji chart...")
        
        # Concatenate all messages into a single string
        words = self.df['message'].astype(str).str.cat(sep=' ')
        
        # Create a PNG
        fig = WordCloud(
            width=1000, 
            height=800,
            stopwords=stopwords,
        ).generate(words)

        # Save PNG file
        fig.to_file( self.outputs_path + "wordcloud.png" ) 
        print(f"✅ File saved in: { self.outputs_path}\n")

