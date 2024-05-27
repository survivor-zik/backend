from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from schemas.product import ProductCreate, ProductUpdate
from model.product import ProductModel
from crud.product import create_product, get_product, get_products, update_product, delete_product
from auth import get_current_active_admin_user

product_router = APIRouter()


@product_router.post("/", response_model=ProductModel)
async def create_product_endpoint(
        name: str,
        price: float,
        description: str,
        colors: str,
        categories: str,
        image: UploadFile = File(...),
        current_user=Depends(get_current_active_admin_user)
):
    product = ProductCreate(name=name, price=price, description=description, colors=colors, categories=categories)
    return await create_product(product, image)


@product_router.get("/{product_id}", response_model=ProductModel)
async def get_product_endpoint(product_id: str):
    product = await get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@product_router.get("/", response_model=List[ProductModel])
async def get_products_endpoint():
    try:
        return await get_products()
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})


@product_router.put("/{product_id}", response_model=ProductModel)
async def update_product_endpoint(
        product_id: str,
        name: str = None,
        price: float = None,
        description: str = None,
        colors: str = None,
        categories: str = None,
        image: UploadFile = File(None),
        current_user=Depends(get_current_active_admin_user)
):
    product = ProductUpdate(name=name, price=price, description=description, colors=colors, categories=categories)
    updated_product = await update_product(product_id, product, image)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found or no changes made")
    return updated_product


@product_router.delete("/{product_id}", response_model=dict)
async def delete_product_endpoint(product_id: str, current_user=Depends(get_current_active_admin_user)):
    success = await delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
