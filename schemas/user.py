from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: str
    password: str
    role: Optional[str] = "User"


class UserUpdate(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: str
    password: Optional[str] = None
    role: Optional[str] = None
    disabled: Optional[bool] = None
