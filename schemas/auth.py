from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserCreate(BaseModel):
    username: str
    full_name: str | None = None
    email: str
    password: str
    role: str | None = "User"


class UserSignIn(BaseModel):
    email: str
    password: str
