from spacy import load
import spacy

nlp = load('ja_core_news_trf')

def get_root(text:str):
    doc = nlp(text)
    root = []
    root_lemma = ''
    for token in doc:
        if token.dep_ == "ROOT":
            root = token.text
            root_lemma = token.lemma_
    return root, root_lemma


