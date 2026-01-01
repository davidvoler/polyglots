from pydantic import BaseModel, EmailStr
from typing import Optional

class Customer(BaseModel):
    customer_id: int
    name: str
    admin_email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True
    create_schema: bool = False
    langs: Optional[list[str]] = None
    to_langs: Optional[list[str]] = None

