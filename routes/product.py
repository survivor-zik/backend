from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
from typing import List
from schemas.product import ProductCreate, ProductUpdate
from model.product import ProductModel
from crud.product import create_product, get_product, get_products, update_product, delete_product
from auth import get_current_active_admin_user
from pathlib import Path
import os
from utils import generate_unique_id
import base64

product_router = APIRouter()

IMAGES_PATH = Path("static")
IMAGES_PATH.mkdir(parents=True, exist_ok=True)


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
    product = ProductCreate(iden=generate_unique_id(), name=name, price=price, description=description, colors=colors,
                            categories=categories)
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


@product_router.get("/image/{product_id}")
async def get_image(product_id: str):
    if f"{product_id}.jpg" in os.listdir(IMAGES_PATH):
        with open(os.path.join(IMAGES_PATH, f"{product_id}.jpg"), "rb") as f:
            image_bytes = f.read()

        return Response(content=image_bytes, media_type="image/jpeg")


@product_router.get("/images/")
async def get_images():
    responses = []
    for image_file in os.listdir(IMAGES_PATH):
        image_path = os.path.join(IMAGES_PATH, image_file)
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            responses.append({
                "image_name": image_file,
                "image_data": image_base64
            })
    return JSONResponse(content=responses)
