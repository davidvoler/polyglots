from transformers import pipeline
import torch

# Define the device
device = torch.device("mps")

# Pass the device to the pipeline
generator = pipeline("text-generation", model="gpt2", device=device)

from farasa.diacratizer import FarasaDiacritizer
import stanza
nlp = stanza.Pipeline('ar', device='mps',processors='tokenize,pos,lemma,depparse')




# Initialize the diacritizer
# This might take a few seconds the first time to load the Java JAR
dg = FarasaDiacritizer()



def get_deacratized(text:str) -> str:
    deacratized = dg.diacritize(text)
    return deacratized


def get_elements(text:str) -> list:
    doc = nlp(text)
    elements = []
    words = []
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.upos == "PUNCT":
                continue
            if word.upos == "SPACE":
                continue
            if word.upos == "NUM":
                continue
            if word.upos == "SYM":
                continue
            if word.upos == "X":
                continue
            words.append(word.text)
            elements.append({
                "text": word.text,
                "pos": word.upos})
    return elements, words

def analyze_sentence(text:str, id:int, lang:str) -> dict:
   
    text = text.strip()
    elements, words = get_elements(text)
    # deacratized = get_deacratized(text)
    deacratized = ''
  
    return {
        "text": text,
        "id": id,
        "elements": elements,
        "words": words,
        "text_alt1": deacratized,
        "text_alt2": '',
        "text_alt3": '',
    }
