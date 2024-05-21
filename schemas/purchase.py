from pydantic import BaseModel
from typing import List


class PurchaseCreateItemModel(BaseModel):
    product_id: str
    quantity: int


class PurchaseCreate(BaseModel):
    items: List[PurchaseCreateItemModel]
    total_price: float
    status: str = "pending"