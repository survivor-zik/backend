from typing import List, Union
from fastapi import HTTPException, UploadFile
from model.product import ProductModel
from schemas.product import ProductCreate, ProductUpdate
from database import product_collection
import uuid
import base64


async def get_product(product_id: str) -> Union[ProductModel, None]:
    product = await product_collection.find_one({"id": product_id})
    if product:
        return ProductModel(**product)
    return None


async def get_products() -> List[ProductModel]:
    products = []
    async for product in product_collection.find():
        # Ensure ID is converted to a string for the model
        product['id'] = str(product['_id'])
        products.append(ProductModel(**product))
    return products


async def create_product(product: ProductCreate, image: UploadFile) -> ProductModel:
    image_data = await image.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    product_dict = product.dict()
    product_dict["image"] = encoded_image
    product_dict["id"] = str(uuid.uuid4())  # Generate UUID as string
    print(product_dict["id"])
    new_product = await product_collection.insert_one(product_dict)
    created_product = await product_collection.find_one({"_id": new_product.inserted_id})
    return ProductModel(**created_product)


async def update_product(product_id: str, product: ProductUpdate, image: UploadFile = None) -> Union[
    ProductModel, None]:
    product_dict = {k: v for k, v in product.dict().items() if v is not None}
    if image:
        image_data = await image.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        product_dict["image"] = encoded_image

    if len(product_dict) >= 1:
        updated_product = await product_collection.update_one(
            {"id": product_id}, {"$set": product_dict}
        )
        if updated_product.modified_count == 1:
            updated_product = await product_collection.find_one({"id": product_id})
            return ProductModel(**updated_product)
    return None


async def delete_product(product_id: str) -> bool:
    deleted_product = await product_collection.delete_one({"id": product_id})
    return deleted_product.deleted_count == 1
