from pydantic import BaseModel
from typing import Optional


class PurchaseCreate(BaseModel):
    user_id: str
    product_id: str
