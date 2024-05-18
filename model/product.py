from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Any


class ProductModel(BaseModel):
    name: str
    price: float
    description: str
    colors: str
    image: bytes
