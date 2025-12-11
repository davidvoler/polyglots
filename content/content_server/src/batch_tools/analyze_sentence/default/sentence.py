

def analyze_sentence(text:str, id:int, lang:str) -> dict:
   
    text = text.strip()
    elements = text.split()
  
    return {
        "text": text,
        "id": id,
        "elements": elements,
        "words": elements,
    }
