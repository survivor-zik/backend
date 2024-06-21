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
    purchase_date: datetime = datetime.now()  # Change to datetime


class PurchaseUpdateItemModel(BaseModel):
    product_id: Optional[str] = None
    quantity: Optional[int] = None


class PurchaseUpdate(BaseModel):
    items: Optional[List[PurchaseUpdateItemModel]] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
