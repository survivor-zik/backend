from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Any


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


class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    price: float
    description: str
    colors: str
    image: bytes

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "description": """Core i5 """,
                "colors": "Blue"
            }
        }
