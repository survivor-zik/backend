from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    iden: str
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
    categories: Optional[str]


class ProductPatch(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    colors: Optional[str] = None
    categories: Optional[str] = None
