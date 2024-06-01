from bson import ObjectId
from typing import List, Union
from fastapi import UploadFile, HTTPException
from model.product import ProductModel
from schemas.product import ProductCreate, ProductUpdate, ProductPatch
from database import product_collection, fs
from PIL import Image
from io import BytesIO
import motor.motor_asyncio


async def get_product(product_id: str) -> Union[ProductModel, None]:
    product = await product_collection.find_one({"iden": product_id})
    if product:
        return ProductModel(**product)
    raise HTTPException(status_code=404, detail="Product not found")


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

    grid_in = fs.open_upload_stream(f"{prod.iden}.jpg")
    await grid_in.write(image.file.read())
    await grid_in.close()

    return prod


async def update_product(product_id: str, product: ProductUpdate, image: UploadFile = None) -> Union[
    ProductModel, None, str]:
    product_dict = {k: v for k, v in product.dict().items() if v is not None}

    if image:
        async for grid_out in fs.find({"filename": f"{product_id}.jpg"}, limit=1):
            await fs.delete(grid_out._id)
        img = Image.open(image.file)
        img_buffer = BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        try:
            async with fs.open_upload_stream_with_id(product_id, f"{product_id}.jpg") as grid_out:
                await grid_out.write(img_buffer.getvalue())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating image: {e}")

    if len(product_dict) >= 1 and image is None:
        updated_product = await product_collection.update_one(
            {"iden": product_id}, {"$set": product_dict}
        )
        if updated_product.modified_count == 1:
            updated_product = await product_collection.find_one({"iden": product_id})
            updated_product['id'] = str(updated_product['_id'])
            return ProductModel(**updated_product)
    if image and len(product_dict) < 1:
        return f"Image changed for {product_id}"
    if image and len(product_dict) >= 1:
        updated_product = await product_collection.update_one(
            {"iden": product_id}, {"$set": product_dict}
        )
        if updated_product.modified_count == 1:
            updated_product = await product_collection.find_one({"iden": product_id})
            updated_product['id'] = str(updated_product['_id'])
            return ProductModel(**updated_product)


async def delete_product(product_id: str) -> bool:
    deleted_product = await product_collection.delete_one({"iden": product_id})
    if deleted_product.deleted_count == 1:
        # Search for associated image
        async for grid_out in fs.find({"filename": f"{product_id}.jpg"}, limit=1):
            # Delete image if found
            await fs.delete(grid_out._id)

        return True
    return deleted_product.deleted_count == 1


async def patch_product(product_id: str, product_patch: ProductPatch, image: UploadFile = None) -> Union[
    ProductModel, None]:
    patch_dict = {k: v for k, v in product_patch.dict().items() if v is not None}

    if image:
        await fs.delete(await fs.find_one({"filename": f"{product_id}.jpg"}))

        grid_in = fs.open_upload_stream(f"{product_id}.jpg")
        await grid_in.write(image.file.read())
        await grid_in.close()

    if len(patch_dict) >= 1:
        updated_product = await product_collection.update_one({"id": product_id}, {"$set": patch_dict})
        if updated_product.modified_count == 1:
            updated_product = await product_collection.find_one({"id": product_id})
            return ProductModel(**updated_product)
    return None
