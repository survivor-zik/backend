from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PurchaseCreateItemModel(BaseModel):
    product_id: str
    quantity: int


class PurchaseCreate(BaseModel):
    items: List[PurchaseCreateItemModel]
    total_price: float
    status: str = "pending"
    address: str
    contact: str
    purchase_date: str = datetime.now()


class PurchaseUpdateItemModel(BaseModel):
    product_id: Optional[str] = None
    quantity: Optional[int] = None


class PurchaseUpdate(BaseModel):
    items: Optional[List[PurchaseUpdateItemModel]] = List[None]
    total_price: Optional[float] = None
    status: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
