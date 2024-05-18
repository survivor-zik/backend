from pydantic import BaseModel, Field
from typing import Optional, Any
from bson import ObjectId
from datetime import datetime


class PurchaseModel(BaseModel):
    date: datetime
