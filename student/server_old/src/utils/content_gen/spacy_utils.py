import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import spacy
from thinc.api import prefer_gpu
is_gpu = prefer_gpu()

NLPS = {}

def get_lang_model_name(lang):
    if lang in ["ca", 'cat']: return "ca_core_news_sm"
    elif lang in ["zh", "zh-Hans", "cmn"]: return "zh_core_web_trf"
    elif lang in ["hr",'hrv' ]: return "hr_core_news_sm"
    elif lang in ["da", "dan"]: return "da_core_news_sm"
    elif lang in ["nl","nld"]: return "nl_core_news_lg"
    elif lang in ["en", 'eng']: return "en_core_web_trf"
    elif lang in["fi","fin"]: return "fi_core_news_lg"
    elif lang in ["fr", "fra"]: return "fr_dep_news_trf"
    elif lang in ["de", "deu"]: return "de_dep_news_trf"
    elif lang in ["el", "ell"]: return "el_core_news_lg"
    elif lang in ["it", "ita"]: return "it_core_news_lg"
    elif lang in ["ja", "jpn"]: return "ja_core_news_trf"
    elif lang in ["ko", "kor"]: return "ko_core_news_sm"
    elif lang in ["lt","lit"]: return "lt_core_news_sm"
    elif lang in ["mk", "mkd"]: return "mk_core_news_sm"
    elif lang in ["nb","nob"]: return "nb_core_news_sm"
    elif lang in ["pl","pol"]: return "pl_core_news_sm"
    elif lang in ["pt-PT", "pt-BR","pt", "por"]: return "pt_core_news_lg"
    elif lang in ["ro", "ron"]: return "ro_core_news_sm"
    elif lang in ["ru", "rus"]: return "ru_core_news_sm"
    elif lang in ["es", "spa"] : return "es_dep_news_trf"
    elif lang in ["sl","slv"]: return "sl_core_news_sm"
    elif lang in ["sv","swe"]: return "sv_core_news_sm"
    elif lang in ["uk", "ukr"]: return "uk_core_news_trf"
    else: return None

def get_nlp(lang):
    global NLPS
    nlp = NLPS.get(lang)
    if not nlp:
        model = get_lang_model_name(lang)
        if model is None:
            return None
        print("Loading model", model)
        nlp = spacy.load(model)
        NLPS[lang] = nlp
    return nlp

def get_spacy_langs():
    return (
        'ca',
        'zh',
        'zh-Hans',
        'hr',
        'da',
        'nl',
        'en',
        'fi',
        'fr',
        'de',
        'el',
        'it',
        'ja',
        'ko',
        'lt',
        'mk',
        'nb',
        'pl',
        'pt',
        'pt-PT',
        'pt-BR',
        'ro',
        'ru',
        'es',
        'sv',
        'uk',
    )