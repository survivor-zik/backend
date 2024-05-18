from fastapi import FastAPI, HTTPException, Depends, status
from typing import List

from fastapi.security import OAuth2PasswordRequestForm

from model.user import UserModel
from fastapi.middleware.cors import CORSMiddleware
from model.product import ProductModel
from model.purchase import PurchaseModel
from schemas.auth import UserCreate, UserSignIn, Token
from schemas.product import ProductCreate, ProductUpdate
from schemas.purchase import PurchaseCreate
from crud.user import get_user, get_users, create_user
from crud.product import get_product, get_products, create_product, update_product, delete_product
from crud.purchase import get_purchase, get_purchases, create_purchase, delete_purchase
from auth import *
from datetime import timedelta
from schemas.auth import TokenResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}


@app.post("/users", response_model=UserModel)
async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    new_user = await user_collection.insert_one(user_dict)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return UserModel(**created_user)


@app.post("/users", response_model=UserModel)
async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    new_user = await user_collection.insert_one(user_dict)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return UserModel(**created_user)


@app.get("/users/me", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@app.get("/admin", response_model=UserModel)
async def read_admin(current_user: UserModel = Depends(get_current_active_admin_user)):
    return current_user


@app.get("/users/", response_model=List[UserModel])
async def get_users_endpoint():
    return await get_users()


@app.post("/products/", response_model=ProductModel)
async def create_product_endpoint(product: ProductCreate, current_user: UserModel = Depends(get_current_user)):
    return await create_product(product)


@app.get("/products/", response_model=List[ProductModel])
async def get_products_endpoint():
    return await get_products()


@app.get("/products/{product_id}", response_model=ProductModel)
async def get_product_endpoint(product_id: str):
    product = await get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=ProductModel)
async def update_product_endpoint(product_id: str, product: ProductUpdate,
                                  current_user: UserModel = Depends(get_current_user)):
    updated_product = await update_product(product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@app.delete("/products/{product_id}")
async def delete_product_endpoint(product_id: str, current_user: UserModel = Depends(get_current_user)):
    if not await delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


@app.post("/purchases/", response_model=PurchaseModel)
async def create_purchase_endpoint(purchase: PurchaseCreate, current_user: UserModel = Depends(get_current_user)):
    return await create_purchase(purchase)


@app.get("/purchases/", response_model=List[PurchaseModel])
async def get_purchases_endpoint():
    return await get_purchases()


@app.get("/purchases/{purchase_id}", response_model=PurchaseModel)
async def get_purchase_endpoint(purchase_id: str):
    purchase = await get_purchase(purchase_id)
    if purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase


@app.delete("/purchases/{purchase_id}")
async def delete_purchase_endpoint(purchase_id: str, current_user: UserModel = Depends(get_current_user)):
    if not await delete_purchase(purchase_id):
        raise HTTPException(status_code=404, detail="Purchase not found")
    return {"message": "Purchase deleted successfully"}
