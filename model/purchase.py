from pydantic import BaseModel, Field
from typing import Optional, Any
from bson import ObjectId
from datetime import datetime


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


class PurchaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    product_id: PyObjectId
    date: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        json_schema_extra = {
            "example": {
                "user_id": "60d9f1c3b6eaf9aaf0d24b11",
                "product_id": "60d9f1c3b6eaf9aaf0d24b12",
                "date": "2024-05-18T12:00:00"
            }
        }
