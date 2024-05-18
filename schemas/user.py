from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: str
    password: str
    role: Optional[str] = "User"


class UserUpdate(BaseModel):
    username: Optional[str]
    full_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role: Optional[str]
    disabled: Optional[bool]
