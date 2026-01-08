from spacy import load
import spacy
loaded_models = {}

SPACY_MODELS_SHORT= {
    "nl": "nl_core_news_lg",
    "en": "en_core_web_trf",
    "fi": "fi_core_news_lg",
    "fr": "fr_dep_news_trf",
    "de": "de_dep_news_trf",
    "el": "el_core_news_lg",
    "it": "it_core_news_lg",
    "ja": "ja_core_news_trf",
    "pt": "pt_core_news_lg",
    "es": "es_dep_news_trf",
    "sv": "sv_core_news_lg",
}


SPACY_MODELS = {
    "ca": "ca_core_news_trf",
    "zh": "zh_core_web_trf",
    "nl": "nl_core_news_lg",
    "en": "en_core_web_trf",
    "fi": "fi_core_news_lg",
    "fr": "fr_dep_news_trf",
    "de": "de_dep_news_trf",
    "el": "el_core_news_lg",
    "it": "it_core_news_lg",
    "ja": "ja_core_news_trf",
    "ko": "ko_core_news_lg",
    "nb": "nb_core_news_lg",
    "pt": "pt_core_news_lg",
    "ro": "ro_core_news_lg",
    "ru": "ru_core_news_lg",
    "es": "es_dep_news_trf",
    "sv": "sv_core_news_lg",
}

def has_spacy_model(lang:str):
    return lang in SPACY_MODELS


def get_nlp(lang:str):
    global loaded_models
    if lang not in loaded_models:
        loaded_models[lang] = load(SPACY_MODELS[lang])
    return loaded_models[lang]


def get_text(token) -> str:
    if token.pos_ == "PROPN":
        return token.text
    return token.text.lower()


def analyze_sentence(text:str, id:int, lang:str) -> dict:
    nlp = get_nlp(lang)
    doc = nlp(text)
    elements = []
    words = []
    verbs = []
    nouns = []
    adjectives = []
    adverbs = []
    auxiliary_verbs = []
    verb_count = 0
    noun_count = 0
    adjective_count = 0
    adverb_count = 0
    auxiliary_verb_count = 0
    propn = []
    root = []
    i = 1
    for token in doc:
        if token.pos_ == "PUNCT":
            continue
        if token.pos_ == "SPACE":
            continue
        if token.pos_ == "NUM":
            continue
        if token.pos_ == "SYM":
            continue
        if token.pos_ == "X":
            continue
        words.append(token.text)
        if token.dep_ == "ROOT":
            root = [token.lemma_, get_text(token)]
        if token.pos_ == "VERB":

            verbs.append([token.lemma_, get_text(token)])
        if token.pos_ == "NOUN":
            nouns.append([token.lemma_, get_text(token)])    
        if token.pos_ == "ADJECTIVE":
            adjectives.append([token.lemma_, get_text(token)])
        if token.pos_ == "ADV":
            adverbs.append([token.lemma_, get_text(token)])
        if token.pos_ == "AUX":
            auxiliary_verbs.append([token.lemma_, get_text(token)])
        if token.pos_ == "PROPN":
            propn.append([token.lemma_, get_text(token)])
            continue
        elements.append({
            "text": get_text(token),
            "lemma": token.lemma_,
            "pos": token.pos_,
            "dep": token.dep_,

        })

    results = {
        "text": get_text(token),
        "id": id,
        "elements": elements,
        "words": words,
        "len_c": len(text),
        "len_elm": len(elements),
        "len_words": len(words),
    }
    for verb in verbs:
        verb_count += 1
        results[f"verb_lemma{verb_count}"] = verb[0]
        results[f"verb{verb_count}"] = verb[1]
    for noun in nouns:
        noun_count += 1
        results[f"noun_lemma{noun_count}"] = noun[0]
        results[f"noun{noun_count}"] = noun[1]
    for adjective in adjectives:
        adjective_count += 1
        results[f"adjective_lemma{adjective_count}"] = adjective[0]
    for adverb in adverbs:
        adverb_count += 1
        results[f"adverb{adverb_count}"] = adverb[0]
    for auxiliary_verb in auxiliary_verbs:
        auxiliary_verb_count += 1
        results[f"auxiliary_verb{auxiliary_verb_count}"] = auxiliary_verb[0]
    results["verb_count"] = verb_count
    results["noun_count"] = noun_count
    results["adjective_count"] = adjective_count
    results["adverb_count"] = adverb_count
    results["auxiliary_verb_count"] = auxiliary_verb_count
    results["propn"] = propn
    if len(root) > 1:
        results["root_lemma"] = root[0]
        results["root"] = root[1]
    else:
        results["root_lemma"] = ''
        results["root"] = ''
    return results

if __name__ == "__main__":
    res = analyze_sentence("Content manager - for creating, loading and generating content", 1, "en")
    print(res)