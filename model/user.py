from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, Any


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls):
        schema = {
            "type": "string",
            "format": "ObjectId",
            "examples": [str(ObjectId())]
        }
        return schema

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    full_name: Optional[str] = None
    email: str
    hashed_password: str
    disabled: Optional[bool] = None
    role: str = "User"

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "username": "tim",
                "full_name": "Tim Ruscica",
                "email": "tim@gmail.com",
                "hashed_password": "$2b$12$HxWHkvMuL7WrZad6lcCfluNFj1/Zp63lvP5aUrKlSTYtoFzPXHOtu",
                "disabled": False,
                "role": "Admin"
            }
        }
