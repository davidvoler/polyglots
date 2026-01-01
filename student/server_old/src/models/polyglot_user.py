from pydantic import BaseModel
from models.users import User
from models.user_vocab import UserVocab


class PolyglotUser(BaseModel):
    user: User = None
    user_vocab: UserVocab = None