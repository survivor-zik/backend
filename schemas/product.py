from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    colors: str
    categories: str


class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    description: Optional[str]
    colors: Optional[str]
    image: Optional[str]
    categories: Optional[str]
