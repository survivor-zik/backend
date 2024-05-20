from pydantic import BaseModel, Field
from typing import Optional
import uuid


class ProductModel(BaseModel):
    id: str
    name: str
    price: float
    description: str
    colors: str
    categories: str
    image: str
