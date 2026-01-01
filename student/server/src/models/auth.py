from pydantic import BaseModel
from typing import Optional

from pydantic import Field
from models.enums import CurrentPracticeEnum
import time
import hashlib

class User(BaseModel):
    customer_id: str = "polyglots"
    email: str
    user_id: Optional[str] = ''
    full_name: Optional[str] = ''
    lang: Optional[str] = ''
    to_lang: Optional[str] = ''

    def as_dict(self):
        self.generate_user_id()
        data =  dict(self)
        data["_id"] = self.email
        return data
    
    def generate_user_id(self):
        self.user_id = hashlib.shake_128(str.encode(self.email)).hexdigest(6)
        return self.user_id





class UserAuth0Request(BaseModel):
    email: str = ""
    full_name: str = ""
    sub: str = ""



class UserStatusRequest(BaseModel):
    user_id: str
    lang: str
    to_lang: str = ""


