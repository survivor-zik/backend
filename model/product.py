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
    categories: Optional[str] = None
    image: Optional[str] = None
