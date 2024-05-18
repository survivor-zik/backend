from pydantic import BaseModel, Field
from typing import Optional, Any


class UserModel(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: str
    hashed_password: str
    disabled: Optional[bool] = None
    role: str = "User"
