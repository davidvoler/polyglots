from pydantic import BaseModel

class Language(BaseModel):
    code2: str
    name: str
    code3: str = None
    native_name:str = None
    icon: str = None
    sound: bool = False
    rtl: bool = False
    icon: str = None
    translit: bool = False
    min_step: int = 1
    max_step: int = 270
    

DIALOGUE_LANGUAGES = [
    Language(code2= 'ar', name =  'Arabic', namtive_name =  'العربية', icon = '🇸🇦', sound =  False, rtl= True),
    Language(code2= 'cs', name =  'Czech', namtive_name =  'Čeština', icon = '🇨🇿', sound =  True, rtl= False),
    Language(code2= 'de', name =  'German', namtive_name =  'Deutsch', icon = '🇩🇪', sound =  True, rtl= False),
    Language(code2= 'el', name =  'Greek', namtive_name =  'Ελληνικά', icon = '🇬🇷', sound =  True, rtl= False),
    Language(code2= 'en', name =  'English', namtive_name =  'English', icon = '🇺🇸', sound =  True, rtl= False),
    Language(code2= 'es', name =  'Spanish', namtive_name =  'Español', icon = '🇪🇸', sound =  True, rtl= False),
    Language(code2= 'fr', name =  'French', namtive_name =  'Français', icon = '🇫🇷', sound =  True, rtl= False),
    Language(code2= 'he', name =  'Hebrew', namtive_name =  'עברית', icon = '🇮🇱', sound =  True, rtl= True),
    Language(code2= 'hi', name =  'Hindi', namtive_name =  'Français', icon = '🇮🇳', sound =  True, rtl= False),
    Language(code2= 'it', name =  'Italian', namtive_name =  'Italiano', icon = '🇮🇹', sound =  True, rtl= False),
    Language(code2= 'ja', name =  'Japanese', namtive_name =  '日本語', icon = '🇯🇵', sound =  True, rtl= False),
    Language(
      code2= 'pt',
      name =  'Portuguese Brazil',
      namtive_name =  'Português',
      icon = '🇧🇷',
      sound =  True,
      rtl= False,
    ),
    Language(
      code2= 'pt-PT',
      name =  'Portuguese Portugal',
      namtive_name =  'Português',
      icon = '🇵🇹',
      sound =  True,
      rtl= False,
    ),
    Language(code2= 'ru', name =  'Russian', namtive_name =  'Русский', icon = '🇷🇺', sound =  True, rtl= False),
    Language(code2= 'zh-Hans', name =  'Chinese', namtive_name =  '中文', icon = '🇨🇳', sound =  False, rtl= False),
]