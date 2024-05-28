from typing import List, Union
from fastapi import UploadFile
from model.product import ProductModel
from schemas.product import ProductCreate, ProductUpdate
from database import product_collection
from utils import generate_unique_id
import shutil
from pathlib import Path
import os

IMAGES_PATH = Path("static")
IMAGES_PATH.mkdir(parents=True, exist_ok=True)


async def get_product(product_id: str) -> Union[ProductModel, None]:
    product = await product_collection.find_one({"iden": product_id})
    if product:
        return ProductModel(**product)
    return None


async def get_products() -> List[ProductModel]:
    products = []
    async for product in product_collection.find():
        products.append(ProductModel(**product))
    return products


async def create_product(product: ProductCreate, image: UploadFile) -> ProductModel:
    product_dict = product.dict()
    new_product = await product_collection.insert_one(product_dict)
    created_product = await product_collection.find_one({"_id": new_product.inserted_id})
    prod = ProductModel(**created_product)
    with open(os.path.join(IMAGES_PATH, f"{prod.iden}.jpg"), "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
    return prod


async def update_product(product_id: str, product: ProductUpdate, image: UploadFile = None) -> Union[
    ProductModel, None]:
    product_dict = {k: v for k, v in product.dict().items() if v is not None}
    if image:
        with open(os.path.join(IMAGES_PATH, f"{product_id}.jpg"), "wb+") as file_object:
            shutil.copyfileobj(image.file, file_object)
    if len(product_dict) >= 1:
        updated_product = await product_collection.update_one(
            {"id": product_id}, {"$set": product_dict}
        )
        if updated_product.modified_count == 1:
            updated_product = await product_collection.find_one({"id": product_id})
            return ProductModel(**updated_product)
    return None


async def delete_product(product_id: str) -> bool:
    deleted_product = await product_collection.delete_one({"iden": product_id})
    # os.remove(os.path.join(IMAGES_PATH, f"{product_id}.jpg"))
    return deleted_product.deleted_count == 1
