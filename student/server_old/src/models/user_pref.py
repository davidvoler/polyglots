from pydantic import BaseModel
from models.auth import User
from models.user_vocab import UserVocab
from typing import Optional


class UserPref(BaseModel):
    user: User = None
    user_vocab: UserVocab = None


class UpdatePreferences(BaseModel):
    user_id: str
    customer_id : str = 'polyglots'
    lang: Optional[str] = None
    to_lang: Optional[str] = None
    practice_type: Optional[bool] = None
    practice_id: Optional[bool] = None
    show_text: Optional[bool] = None
    auto_play: Optional[bool] = None
    play_speed: Optional[bool] = None

