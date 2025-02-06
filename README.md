
# WhatsApp Group Chat Analyzer

This repository contains a comprehensive tool for analyzing WhatsApp group chats. The project processes exported chat logs by cleaning and converting them into a structured CSV file, generates basic visualizations (e.g., heatmaps, user activity bar charts, top emoji usage, and word clouds), and performs advanced topic modeling using BERTopic. Optional integration with OpenAI’s ChatGPT or KeyBERT enhances text representation. Finally, all outputs are consolidated into an interactive HTML summary report.

## Main Feature

1. Configurable Processing: Easily adjust settings such as chat language, group name, API keys, and file paths through a simple configuration file.

2. Robust Data Extraction: Automatically convert raw WhatsApp chat logs into a clean, structured CSV format by filtering out system messages and normalizing user names.

3. Comprehensive Visualizations: Generate a suite of visual outputs including heatmaps that show active days and hours, bar charts for user activity, top emoji usage charts, and word clouds.

- Activity Heatmap.
- Top Users Bar Chart.
- Emoji Usage Chart.
- Wordcloud.
- Topics Over Time.
- Topics Map (Intertopic Distance Map).
- Topic Pie Chart.
- Topic Hierarchy Diagram.
- Topic Bar Chart.

4. Advanced Topic Modeling: Leverage BERTopic to extract and visualize discussion themes over time, with optional support from ChatGPT or KeyBERT to enhance text representation.

5. Interactive HTML Report: Consolidate all analytics and visualizations into a single, user-friendly HTML report for an overview of group chat insights.

## Configuration
Before running the project, update the configuration file with your settings:

- Chat Language: Specify the language used in the chat.
- OpenAI API Key (Optional): Provide your API key to enable enhanced text representation.
- Group Name: Set the name of the WhatsApp group.
- File Paths: Define the paths for the raw chat data and output directories.