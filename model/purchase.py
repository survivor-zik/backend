from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import uuid


class PurchaseItemModel(BaseModel):
    product_id: str
    quantity: int


class PurchaseModel(BaseModel):
    id: str
    user_id: str
    items: List[PurchaseItemModel]
    total_price: float
    purchase_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"
