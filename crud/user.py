from typing import List, Union
from model.user import UserModel
from schemas.auth import UserCreate
from database import user_collection
from bson import ObjectId
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(user_id: str) -> Union[UserModel, None]:
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return UserModel(**user)


async def get_user_by_email(email: str) -> Union[UserModel, None]:
    user = await user_collection.find_one({"email": email})
    if user:
        return UserModel(**user)


async def get_users() -> List[UserModel]:
    users = []
    async for user in user_collection.find():
        users.append(UserModel(**user))
    return users


async def create_user(user: UserCreate) -> UserModel:
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    new_user = await user_collection.insert_one(user_dict)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return UserModel(**created_user)
