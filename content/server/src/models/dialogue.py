from pydantic import BaseModel

class DialogueRequest(BaseModel):
    corpus: str
    lang: str
    to_lang: str
    review: bool = True
    limit: int = -1
    offset: int = 0


class Dialogue(BaseModel):
    dialogue_id: int
    line_no: int
    text: str
    source: str
    spacy_analysis: dict
    transliteration: dict
    element_tags: dict
    elements: list
    verbs: list
    auxiliary_verbs: list
    nouns: list
    adjectives: list