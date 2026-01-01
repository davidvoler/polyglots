import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import re
from utils.content_gen.spacy_utils import get_nlp

def split_sentences_simple(text):
    sentences = re.split(r'[.?!]', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def split_sentences_nlp(text, lang):
    nlp = get_nlp(lang)
    sentences = [i for i in nlp(text).sents]
    return [str(i) for i in sentences]

def sentences_breaker(text, lang):
    nlp = get_nlp(lang)
    sentences = [i for i in nlp(text).sents]
    return sentences


def remove_punct(s:str):
    s = s.strip()
    while s and s[-1] in ["!",".","?", ",", '"', "'", ":", ";", ":", ";", "¿", "¡", '?']:
        s = s[:-1]
    while s and s[0] in ["!",".","?", ",", '"', "'", ":", ";", "¿", "¡", '?']:
        s = s[1:]
    return s

        
def split_words_simple(sentence:str, lang:str):
    nlp = get_nlp(lang)
    doc = nlp(sentence)
    words = []
    for token in doc:
        if not token.is_punct and not token.is_space:
            words.append(token.text.lower())
    return words


def _get_words_all_structure(sentence:str, nlp,remove_stop=False):
    doc = nlp(sentence)
    words = []
    all_words = []
    stop_words = []
    pos = []
    propn = []
    root = ""
    for token in doc:
        if not token.is_punct and not token.is_space:
            all_words.append(token.text.lower())
            pos.append(token.pos_)
            if token.pos_ == "PROPN":
                propn.append(token.text)
            elif token.is_stop:
                stop_words.append(token.text.lower())
            else:
                words.append(token.text.lower())
            if token.dep_ == "ROOT":
                root = token.text.lower()
    return words, all_words, pos, root, propn, stop_words

def get_words_all_structure(sentence:str, lang:str, remove_stop=False):
    nlp = get_nlp(lang)
    return _get_words_all_structure(sentence, nlp, remove_stop)

def _get_words_nlp(nlp, sentence:str, include_stop_words=False):
    doc = nlp(sentence)
    words = []
    for token in doc:
        if include_stop_words:
        # if not token.is_stop and not token.is_punct and not token.is_space:
            if not token.is_punct and not token.is_space:
                words.append(token.text)
        else:
            if not token.is_stop and not token.is_punct and not token.is_space:
                words.append(token.text)
    return words          
        
