from pydantic import BaseModel
from typing import List, Optional


class PurchaseCreateItemModel(BaseModel):
    product_id: str
    quantity: int


class PurchaseCreate(BaseModel):
    items: List[PurchaseCreateItemModel]
    total_price: float
    status: str = "pending"
    contact: str
    address: str


class PurchaseUpdateItemModel(BaseModel):
    product_id: Optional[str] = None
    quantity: Optional[int] = None


class PurchaseUpdate(BaseModel):
    items: List[PurchaseUpdateItemModel] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
