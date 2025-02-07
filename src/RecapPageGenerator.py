import os 

class RecapPageGenerator:
    def __init__(self, outputs_path, base_url, group_name=None, start_date=None, end_date=None):
        # Initialize the generator with the output path and the base URL.
        # Set up the pre-configured charts.
        self.outputs_path = outputs_path
        self.base_url = base_url
        self.group_name = group_name
        self.start_date = start_date
        self.end_date = end_date   
        # Default charts
        self.paths_config = {
            'heatmap': f"{base_url}heatmap.html",
            'topusers': f"{base_url}topusers.html",
            'emojichart': f"{base_url}emojichart.html",
            'wordcloud': f"{base_url}wordcloud.png",
            'topic_map': f"{base_url}TopicModeling/topic_map.html",
            'topic_pie': f"{base_url}TopicModeling/topic_pie.html"
        }
        # List for additional charts
        self.additional_graphs = []

    def add_graph(self, graph_id, graph_url, title, icon):
        """
        Adds a new chart section to the page.
        :param graph_id: unique identifier of the chart
        :param graph_url: URL of the chart
        :param title: title to display in the section
        :param icon: icon class (e.g., 'fas fa-chart-line')
        """
        self.additional_graphs.append({
            'id': graph_id,
            'url': graph_url,
            'title': title,
            'icon': icon
        })

    def generate_html(self):
        """
        Generates the HTML content of the page.
        :param font_family: string for the font to use, default is the default font
        :return: string containing the complete HTML
        """
        # Generates sections for pre-configured charts
        preconfigured = [
            ('Chat Activity HeatMap', 'fas fa-fire', self.paths_config['heatmap']),
            ('Top Most Active Users', 'fas fa-crown', self.paths_config['topusers']),
            ('Top Emojis', 'fas fa-smile', self.paths_config['emojichart']),
            ('Word Cloud', 'fas fa-cloud', self.paths_config['wordcloud'], 'wordcloud'),
            ('Topic Map (Intertopic Distance Map)', 'fas fa-comments', self.paths_config['topic_map']),
            ('Topic Distribution', 'fas fa-chart-pie', self.paths_config['topic_pie'])
        ]
        sections_html = ""
        for entry in preconfigured:
            # If the chart is of type wordcloud, use a different structure
            if len(entry) == 4 and entry[3] == 'wordcloud':
                title, icon, src, _ = entry
                section = f"""
        <div class="section">
            <h2><i class="{icon} icon"></i>{title}</h2>
            <div class="wordcloud-container">
                <img src="{src}" alt="{title}">
            </div>
        </div>
                """
            else:
                title, icon, src = entry[:3]
                section = f"""
        <div class="section">
            <h2><i class="{icon} icon"></i>{title}</h2>
            <iframe class="visualization" src="{src}"></iframe>
        </div>
                """
            sections_html += section

        # Aggiungi le sezioni per i grafici aggiuntivi
        for graph in self.additional_graphs:
            section = f"""
        <div class="section">
            <h2><i class="{graph['icon']} icon"></i>{graph['title']}</h2>
            <iframe class="visualization" src="{graph['url']}"></iframe>
        </div>
            """
            sections_html += section

        # Header section
        header_content = ""
        if self.group_name:
            header_content += f'<h1>Chat Analytics: {self.group_name}</h1>'
        else:
            header_content += '<h1>Chat Analytics</h1>'

        if self.start_date and self.end_date:
            header_content += f'''
            <p style="color: #00ff88; font-size: 1.2em; margin-top: 15px;">
                Analysis Period: {self.start_date} - {self.end_date}
            </p>'''

        header_content += '''
        <p style="color: #666; margin-top: 10px;">This page provides a comprehensive, interactive summary of the analysis performed on WhatsApp group chats. After uploading the exported chat logs, the system processes the data, cleans the text, and converts it into a structured CSV file. It then generates easy-to-understand visualizations.</p>
        <p style="color: #666; margin-top: 10px;">For deeper insights, the system also applies advanced topic modeling using BERTopic. Optional integration with OpenAI's ChatGPT or KeyBERT enhances text representation, providing more precise analysis. </p>
        <p style="color: #999797; margin-top: 10px;">For more details, check out the project on <a href="https://github.com/miraf18/WhatsApp-Group-Chat-Analyzer" target="_blank">GitHub</a>.</p>
        '''


        # Template HTML completo
        html_template = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Chat Recap</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,200..1000;1,200..1000&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Nunito', serif;
            background: #0a0a0a;
            color: #fff;
            line-height: 1.6;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }}

        header {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 40px 20px;
            margin: 20px 0;
            background: #161616;
            border-radius: 12px;
            border: 1px solid #252525;
        }}

        h1 {{
            font-size: 2.5rem;
            background: linear-gradient(45deg, #00ff88, #00ffcc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }}

        .section {{
            min-height: 650px;
            background: #161616;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #252525;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }}

        .section:hover {{
            transform: translateY(-5px);
            border-color: #00ff88;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.1);
        }}

        .section h2 {{
            font-size: 1.4rem;
            margin-bottom: 15px;
            color: #00ff88;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 0;
            border-bottom: 2px solid #252525;
        }}

        .visualization {{
            flex: 1;
            width: 100%;
            border: none;
            border-radius: 8px;
            background: #1a1a1a;
            margin-top: 15px;
        }}

        .wordcloud-container {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #1a1a1a;
            border-radius: 8px;
            padding: 15px;
        }}

        .wordcloud-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            object-fit: contain;
        }}

        .icon {{
            font-size: 1.2rem;
            color: #00ff88;
        }}

        footer {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 30px;
            margin-top: 40px;
            background: #161616;
            border-radius: 12px;
            border: 1px solid #252525;
        }}

        footer p {{
            color: #666;
            margin-top: 10px;
            font-size: 0.9em;
        }}

        @media (max-width: 1000px) {{
            .container {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            .section {{
                min-height: 400px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            {header_content}
        </header>
        {sections_html}
        <footer>
            <p>Created by <a href="https://github.com/miraf18" style="color: #00ff88;">@miraf18</a></p>
            <p>Automatically generated with Python</p>
        </footer>
    </div>
</body>
</html>
        """
        return html_template

    # Save de page
    def save_page(self, filename="index.html"):
        html = self.generate_html()
        output_path_page = os.path.join(self.outputs_path, filename)
        with open(output_path_page, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"💾 Recap: HTML successfully generated in: {output_path_page}")
