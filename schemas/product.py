from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    colors: str
    categories: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    colors: Optional[str] = None
    image: Optional[str] = None
    categories: Optional[str] = None
