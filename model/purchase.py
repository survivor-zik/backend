from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import uuid


class PurchaseItemModel(BaseModel):
    product_id: uuid.UUID
    quantity: int


class PurchaseModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    items: List[PurchaseItemModel]
    total_price: float
    purchase_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"

    model_config = {"populate_by_name": True, "json_encoders": {uuid.UUID: str}}