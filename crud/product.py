from typing import List, Union
from model.product import ProductModel
from schemas.product import ProductCreate, ProductUpdate
from database import product_collection
from bson import ObjectId


async def get_product(product_id: str) -> Union[ProductModel, None]:
    product = await product_collection.find_one({"_id": ObjectId(product_id)})
    if product:
        return ProductModel(**product)


async def get_products() -> List[ProductModel]:
    products = []
    async for product in product_collection.find():
        products.append(ProductModel(**product))
    return products


async def create_product(product: ProductCreate) -> ProductModel:
    product_dict = product.dict()
    new_product = await product_collection.insert_one(product_dict)
    created_product = await product_collection.find_one({"_id": new_product.inserted_id})
    return ProductModel(**created_product)


async def update_product(product_id: str, product: ProductUpdate) -> Union[ProductModel, None]:
    product_dict = {k: v for k, v in product.dict().items() if v is not None}
    if len(product_dict) >= 1:
        updated_product = await product_collection.update_one(
            {"_id": ObjectId(product_id)}, {"$set": product_dict}
        )
        if updated_product.modified_count == 1:
            if (
                    updated_product := await product_collection.find_one(
                        {"_id": ObjectId(product_id)}
                    )
            ) is not None:
                return ProductModel(**updated_product)
    return None


async def delete_product(product_id: str) -> bool:
    deleted_product = await product_collection.delete_one({"_id": ObjectId(product_id)})
    return deleted_product.deleted_count == 1
