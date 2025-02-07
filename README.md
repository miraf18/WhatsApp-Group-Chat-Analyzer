
# 📊 WhatsApp Group Chat Analyzer

This repository contains a comprehensive tool for analyzing WhatsApp group chats. The project processes exported chat logs by cleaning and converting them into a structured CSV file, generates basic visualizations (e.g., heatmaps, user activity bar charts, top emoji usage, and word clouds), and performs advanced topic modeling using BERTopic. Optional integration with OpenAI’s ChatGPT or KeyBERT enhances text representation. Finally, all outputs are consolidated into an interactive HTML summary report.

## ✨ Main Feature

1. ⚙️ Configurable Processing: Easily adjust settings such as chat language, group name, API keys, and file paths through a simple configuration file.

2. 📑 Robust Data Extraction: Automatically convert raw WhatsApp chat logs into a clean, structured CSV format by filtering out system messages and normalizing user names.

3. 📊 Comprehensive Visualizations: Generate a suite of visual outputs including heatmaps that show active days and hours, bar charts for user activity, top emoji usage charts, and word clouds.

- Activity Heatmap.
- Top Users Bar Chart.
- Emoji Usage Chart.
- Wordcloud.
- Topics Over Time.
- Topics Map (Intertopic Distance Map).
- Topic Pie Chart.
- Topic Hierarchy Diagram.
- Topic Bar Chart.

4. 🧠 Advanced Topic Modeling: Leverage BERTopic to extract and visualize discussion themes over time, with optional support from ChatGPT or KeyBERT to enhance text representation.

5. 🖥️ Interactive HTML Report: Consolidate all analytics and visualizations into a single, user-friendly HTML report for an overview of group chat insights.

![Example HTML Recap](https://github.com/miraf18/WhatsApp-Group-Chat-Analyzer/blob/main/html.gif)

## 🛠️ Configuration and Usage
1. Install the packages.
```bash
pip install -r requirements.txt
```

2. Before running the project, update the configuration file, "_config.yaml_", with your settings.
_**Note**: If you want to use the representation with ChatGPT (recommended, but much slower), enter your OpenAI API key; otherwise, the KeyBERT model will be used._

3. Extract the WhatsApp chat from the app (watch a tutorial if you don't know how to do it) and place the "__chat.txt_" file in the designated folder:
```
.../data/raw/_chat.txt
```
4. run "_main.py_". The charts will be saved in the output folder.

_**Note**: If the system messages are in languages other than English, they need to be manually modified in the file: "DataProcessing.py"._

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)

The MIT License allows anyone to use, modify, and distribute the code, even for commercial purposes, as long as the original copyright and license are retained. However, the software is provided "as is" with no warranty, and the author is not liable for any issues arising from its use.
