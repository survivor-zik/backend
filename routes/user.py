from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from model.user import UserModel
from schemas.user import UserCreate, UserUpdate
from database import user_collection
from passlib.context import CryptContext
from auth import get_current_active_admin_user, get_current_user, get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_router = APIRouter()


@user_router.post("/", response_model=UserModel)
async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    new_user = await user_collection.insert_one(user_dict)
    created_user = await user_collection.find_one({"email": user.email})
    return UserModel(**created_user)


@user_router.get("/", response_model=List[UserModel])
async def read_users(current_user: UserModel = Depends(get_current_active_admin_user)):
    users = []
    async for user in user_collection.find():
        users.append(UserModel(**user))
    return users


@user_router.get("/{email}", response_model=UserModel)
async def read_user(email: str, current_user: UserModel = Depends(get_current_user)):
    user = await user_collection.find_one({"email": email})
    if user:
        return UserModel(**user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.put("/{email}", response_model=UserModel)
async def update_user(email: str, user: UserUpdate, current_user: UserModel = Depends(get_current_active_admin_user)):
    user_dict = user.dict(exclude_unset=True)
    if user_dict.get("password"):
        user_dict["hashed_password"] = get_password_hash(user_dict["password"])
        del user_dict["password"]
    result = await user_collection.update_one({"email": email}, {"$set": user_dict})
    if result.modified_count == 1:
        updated_user = await user_collection.find_one({"email": email})
        return UserModel(**updated_user)
    else:
        raise HTTPException(status_code=404, detail="User not found or no changes made")


@user_router.delete("/{email}", response_model=UserModel)
async def delete_user(email: str, current_user: UserModel = Depends(get_current_active_admin_user)):
    result = await user_collection.find_one_and_delete({"email": email})
    if result:
        return UserModel(**result)
    else:
        raise HTTPException(status_code=404, detail="User not found")
