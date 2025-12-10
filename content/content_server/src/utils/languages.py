LANG2LANG3 = {
    "ar": "ara",
    "cs": "ces",
    "de": "deu",
    "el": "ell",
    "en": "eng",
    "es": "spa",
    "fr": "fra",
    "he": "heb",
    "hi": "hin",
    "it": "ita",
    "ja": "jpn",
    "pt": "por",
    "pt-PT": "por",
    "ru": "rus",
    "zh-Hans": "zho",
} 
LANG2COUNTY = {
    "ar": "ar-",
    "cs": "cs-CZ",
    "de": "de-DE",
    "el": "el-GR",
    "en": "en-US",
    "es": "es-ES",
    "fr": "fr-FR",
    "he": "he-IL",
    "hi": "hi-IN",
    "it": "it-IT",
    "ja": "ja-JP",
    "pt": "pt-PT",
    'pt-BR': 'pt-BR',
    "ru": "ru-RU",
    "zh-Hans": "zh-CN",
}

LANG32LANG = {v: k for k, v in LANG2LANG3.items()}

def get_lang3(lang2: str) -> str:
    return LANG2LANG3.get(lang2, lang2)

def get_lang2(lang3: str) -> str:
    return LANG32LANG.get(lang3, lang3)

def list_langs2() -> list[str]:
    return list[str](LANG2LANG3.keys())

def list_langs3() -> list[str]:
    return list[str](LANG32LANG.keys())

def get_county(lang2: str) -> str:
    return LANG2COUNTY.get(lang2, lang2)
