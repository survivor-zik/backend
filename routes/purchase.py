import uuid

from model.purchase import PurchaseModel
from schemas.purchase import PurchaseCreate
from fastapi import APIRouter, HTTPException, Depends, status
from model.user import UserModel
from auth import get_current_user, get_current_active_admin_user
from database import purchase_collection
from typing import List
from bson import ObjectId

purchase_router = APIRouter()


@purchase_router.post("/", response_model=PurchaseModel)
async def create_purchase(purchase: PurchaseCreate, current_user: UserModel = Depends(get_current_user)):
    try:
        purchase.user_id = current_user.email
        purchase_dict = purchase.dict(by_alias=True)
        purchase_dict["_id"] = str(uuid.uuid4())
        print(purchase_dict)
        result = await purchase_collection.insert_one(purchase_dict)
        created_purchase = await purchase_collection.find_one({"_id": result.inserted_id})
        return PurchaseModel(**created_purchase)

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create purchase")


@purchase_router.get("/{purchase_id}", response_model=PurchaseModel)
async def get_purchase(purchase_id: str, current_user: UserModel = Depends(get_current_user)):
    purchase = await purchase_collection.find_one({"_id": purchase_id})
    if purchase:
        return PurchaseModel(**purchase)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")


@purchase_router.get("/", response_model=List[PurchaseModel])
async def get_purchase_all(current_user: UserModel = Depends(get_current_active_admin_user)):
    purchases = []
    async for purchase in purchase_collection.find():
        purchases.append(PurchaseModel(**purchase))
    if purchases:
        return purchases
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No purchases found")


@purchase_router.get("/user", response_model=List[PurchaseModel])
async def get_user_purchases(current_user: UserModel = Depends(get_current_user)):
    user_purchases = await purchase_collection.find({"user_id": current_user.email}).to_list(length=None)
    return user_purchases


@purchase_router.put("/{purchase_id}", response_model=PurchaseModel)
async def update_purchase(purchase_id: str, purchase: PurchaseModel,
                          current_user: UserModel = Depends(get_current_active_admin_user)):
    purchase_dict = purchase.dict(by_alias=True, exclude_unset=True)
    purchase_dict["_id"] = purchase_dict.pop("id")
    result = await purchase_collection.update_one({"_id": uuid.UUID(purchase_id)}, {"$set": purchase_dict})
    if result.modified_count == 1:
        updated_purchase = await purchase_collection.find_one({"_id": uuid.UUID(purchase_id)})
        return PurchaseModel(**updated_purchase)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found or no changes made")


@purchase_router.delete("/{purchase_id}", response_model=PurchaseModel)
async def delete_purchase(purchase_id: str, current_user: UserModel = Depends(get_current_active_admin_user)):
    result = await purchase_collection.find_one_and_delete({"_id": uuid.UUID(purchase_id)})
    if result:
        return PurchaseModel(**result)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
