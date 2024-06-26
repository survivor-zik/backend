import uuid
from model.purchase import PurchaseModel
from schemas.purchase import PurchaseCreate, PurchaseUpdate
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from model.user import UserModel
from auth import get_current_user, get_current_active_admin_user
from database import purchase_collection
from typing import List
from utils import send_email
from crud.product import get_product

purchase_router = APIRouter()


@purchase_router.post("/", response_model=PurchaseModel)
async def create_purchase(purchase: PurchaseCreate, current_user: UserModel = Depends(get_current_user)):
    try:
        products = []
        purchase_dict = purchase.dict()
        purchase_dict["user_id"] = current_user.email
        # print(current_user.email)
        purchase_dict["_id"] = str(uuid.uuid4())
        result = await purchase_collection.insert_one(purchase_dict)
        created_purchase = await purchase_collection.find_one({"_id": result.inserted_id})
        for item in created_purchase['items']:
            i = await get_product(item['product_id'])
            products.append(i.name)
            # print(i)
        subject = "Purchase Confirmation"
        body = "Thank you for your purchase! You have bought the following items:\n" + "\n".join(products)
        send_email(subject, body, current_user.email)

        return PurchaseModel(**created_purchase)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create purchase: {str(e)}")


@purchase_router.get("/{purchase_id}", response_model=PurchaseModel)
async def get_purchase(purchase_id: str, current_user: UserModel = Depends(get_current_user)):
    try:
        purchase = await purchase_collection.find_one({"_id": purchase_id})
        if purchase:
            return PurchaseModel(**purchase)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to get purchase: {str(e)}")


@purchase_router.get("/", response_model=List[PurchaseModel])
async def get_purchase_all(current_user: UserModel = Depends(get_current_active_admin_user)):
    try:
        purchases = []
        async for purchase in purchase_collection.find():
            purchases.append(PurchaseModel(**purchase))
        if purchases:
            return purchases
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No purchases found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to get purchases: {str(e)}")


@purchase_router.get("/user", response_model=List[PurchaseModel])
async def get_user_purchases(current_user: UserModel = Depends(get_current_user)):
    try:
        print(current_user.email)
        user_purchases = await purchase_collection.find({"user_id": current_user.email}).to_list(length=None)
        return [PurchaseModel(**purchase) for purchase in user_purchases]
    except Exception as e:
        print(e,"error")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to get user purchases: {str(e)}")


@purchase_router.put("/{purchase_id}", response_model=PurchaseModel)
async def update_purchase(purchase_id: str, purchase: PurchaseCreate,
                          current_user: UserModel = Depends(get_current_active_admin_user)):
    try:
        purchase_dict = purchase.dict(by_alias=True, exclude_unset=True)
        result = await purchase_collection.update_one({"_id": purchase_id}, {"$set": purchase_dict})
        if result.modified_count == 1:
            updated_purchase = await purchase_collection.find_one({"_id": purchase_id})
            return PurchaseModel(**updated_purchase)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found or no changes made")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to update purchase: {str(e)}")


@purchase_router.delete("/{purchase_id}", response_model=PurchaseModel)
async def delete_purchase(purchase_id: str, current_user: UserModel = Depends(get_current_active_admin_user)):
    try:
        result = await purchase_collection.find_one_and_delete({"_id": purchase_id})
        if result:
            return PurchaseModel(**result)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to delete purchase: {str(e)}")


@purchase_router.patch("/{purchase_id}", response_model=PurchaseModel)
async def patch_purchase(purchase_id: str, purchase: PurchaseUpdate,
                         current_user: UserModel = Depends(get_current_active_admin_user)):
    try:
        existing_purchase = await purchase_collection.find_one({"_id": purchase_id})

        if not existing_purchase:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")

        update_data = purchase.dict(exclude_unset=True)

        updated_purchase = {**existing_purchase, **update_data}

        result = await purchase_collection.replace_one({"_id": purchase_id}, updated_purchase)

        if result.modified_count == 1:
            updated_purchase = await purchase_collection.find_one({"_id": purchase_id})
            return PurchaseModel(**updated_purchase)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update purchase")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to update purchase: {str(e)}")
