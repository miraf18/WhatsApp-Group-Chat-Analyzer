import spacy
from typing import Set, Tuple, List

class SpacyNLP:     
    def __init__(self, language: str):
        self.language = language
        # Load the spaCy model based on the specified language
        print("⏳ Loading the NLP model (spaCy)...\n")
        try:
            # nlp = en_core_web_md.load()  web, I believe it doesn't download
            self.nlp = spacy.load(f"{language}_core_news_sm")
        except OSError:
            print(f"⏳ Downloading spaCy model for {language}...")
            from spacy.cli import download
            download(f"{language}_core_news_sm")
            self.nlp = spacy.load(f"{language}_core_news_sm")

        self.stopwords = self.get_stopwords()

    # Stopwords: 
    #   you have the option to customize them for more effective filtering in specific cases
    def get_stopwords(self) -> Set[str]:
        # Get spaCy stopwords
        print("⏳ Retrieval of stopwords...")
        nlp_stopwords = self.nlp.Defaults.stop_words
        other_stopwords  = {
            'ahah', 'ahahah', 'ahahaha', 'ahahahah', 'ahahahahah',
            'this', 'message', 'was', 'deleted', 'omitted',
            'votes', 'option', 'edited', 'ok', 'oky', 'okay', 
            '<This message was edited>',
            # add other here

            # Numbers and single letters
            *[str(i) for i in range(100)],
            *'abcdefghijklmnopqrstuvwxyz'
        }
        stopwords = nlp_stopwords | other_stopwords

        return stopwords