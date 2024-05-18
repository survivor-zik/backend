from typing import List
from model.purchase import PurchaseModel
from schemas.purchase import PurchaseCreate
from database import purchase_collection
from bson import ObjectId
from datetime import datetime


async def get_purchase(purchase_id: str) -> PurchaseModel:
    purchase = await purchase_collection.find_one({"_id": ObjectId(purchase_id)})
    if purchase:
        return PurchaseModel(**purchase)


async def get_purchases() -> List[PurchaseModel]:
    purchases = []
    async for purchase in purchase_collection.find():
        purchases.append(PurchaseModel(**purchase))
    return purchases


async def create_purchase(purchase: PurchaseCreate) -> PurchaseModel:
    purchase_dict = purchase.dict()
    purchase_dict["user_id"] = ObjectId(purchase_dict["user_id"])
    purchase_dict["product_id"] = ObjectId(purchase_dict["product_id"])
    purchase_dict["date"] = datetime.utcnow()
    new_purchase = await purchase_collection.insert_one(purchase_dict)
    created_purchase = await purchase_collection.find_one({"_id": new_purchase.inserted_id})
    return PurchaseModel(**created_purchase)


async def delete_purchase(purchase_id: str) -> bool:
    deleted_purchase = await purchase_collection.delete_one({"_id": ObjectId(purchase_id)})
    return deleted_purchase.deleted_count == 1
