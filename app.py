from fastapi import FastAPI, HTTPException, Depends, status
from typing import List
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
from auth import authenticate_user, create_access_token, get_current_user
from datetime import timedelta

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: UserSignIn):
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=UserModel)
async def create_user_endpoint(user: UserCreate):
    return await create_user(user)


@app.get("/users/", response_model=List[UserModel])
async def get_users_endpoint():
    return await get_users()


@app.get("/users/{user_id}", response_model=UserModel)
async def get_user_endpoint(user_id: str):
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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
