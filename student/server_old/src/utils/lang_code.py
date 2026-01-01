
LANGS3 = {
    "deu" : "de",
    "eng": "en",
    "fra": "fr",
    "hin": "hi",
    "ita": "it",
    "jpn": "ja",
    "kor":"ko",
    "nld": "nl",
    "por": "po-BR",
    "rus": "ru",
    "spa": "es",
    "cmn": "zh-Hans",
    "ell": "el",
    "ara": "ar",
    "heb": "he",

}

LANGS_SHORT = {
"de": "deu",
"en": "eng",
"fr": "fra",
"hi": "hin",
"it": "ita",
"ja": "jpn",
"ko": "kor",
"nl": "nld",
"po-BR": "por",
"ru": "rus",
"es": "spa",
"zh-Hans": "cmn",
"el": "ell",
"ar": "ara",
"he": "heb",
}

def lang_to_lang3(lang: str) -> str:
    """
    Convert a language code to its 3-letter ISO 639-3 code.
    """
    return LANGS_SHORT.get(lang, lang)

def lang3_to_lang(lang: str) -> str:
    """
    Convert a language code to its 3-letter ISO 639-3 code.
    """
    return LANGS3.get(lang, lang)