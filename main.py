from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = {
    "tim": {
        "username": "tim",
        "full_name": "Tim Ruscica",
        "email": "tim@gmail.com",
        "hashed_password": "$2b$12$HxWHkvMuL7WrZad6lcCfluNFj1/Zp63lvP5aUrKlSTYtoFzPXHOtu",
        "disabled": False
    }
}
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

products_db = {
    1: {
        "id": 1,
        "name": "TechPro Ultrabook",
        "description": "Powerful and sleek ultrabook for professionals.",
        "price": 1299.99
    },
    2: {
        "id": 2,
        "name": "SmartHome Hub",
        "description": "Control your home devices with ease.",
        "price": 79.95
    }
}

purchases_db = {
    1: {
        "user_id": "tim",  # Assuming "tim" is the username
        "product_id": 1,
        "purchase_date": "2024-05-10T15:32:05Z"  # ISO 8601 format
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float


class Purchase(BaseModel):
    user_id: int
    product_id: int
    purchase_date: datetime = datetime.utcnow()


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]


@app.post("/products/", response_model=Product)
async def create_product(product: Product, current_user: User = Depends(get_current_active_user)):
    product.id = len(products_db) + 1
    products_db[product.id] = product
    return product


@app.get("/products/", response_model=list[Product])
async def read_products():
    return list(products_db.values())


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product, current_user: User = Depends(get_current_active_user)):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db[product_id] = product
    return product


@app.delete("/products/{product_id}")
async def delete_product(product_id: int, current_user: User = Depends(get_current_active_user)):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
    return {"message": "Product deleted"}


@app.post("/products/{product_id}/purchase", response_model=Purchase)
async def purchase_product(product_id: int, current_user: User = Depends(get_current_active_user)):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    purchase = Purchase(user_id=current_user.id, product_id=product_id)
    purchases_db.append(purchase)
    return purchase


@app.get("/products/{product_id}/buyers", response_model=list[User])
async def get_product_buyers(product_id: int, current_user: User = Depends(get_current_active_user)):
    buyers = []
    for purchase in purchases_db:
        if purchase.product_id == product_id:
            buyer = get_user(db, purchase.user_id)
            if buyer:
                buyers.append(buyer)
    return buyers


@app.delete("/purchases/{purchase_id}")
async def delete_purchase(purchase_id: int, current_user: User = Depends(get_current_active_user)):
    """Deletes a purchase by its ID, if the current user is authorized."""

    purchase = purchases_db[purchase_id]

    # Authorization check
    if purchase is None or purchase["user_id"] != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this purchase")

    result = purchase

    # result = purchases_collection.delete_one({"id": purchase_id})
    del purchases_db[purchase_id]
    if purchase_id not in purchases_db:
        return {"message": "Purchase deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete purchase")

@app.get("/admin/purchases/")
async def get_purchases_with_buyers(current_user: User = Depends(get_current_active_user)):
    """Retrieves all purchases with buyer information for the admin panel."""

    # Authorization check (ensure the current user is an admin)
    if not current_user.is_admin:  # Replace 'is_admin' with your actual admin check logic
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    purchases_with_buyers = []

    for purchase_id, purchase in purchases_db.items():
        buyer_info = db.get(purchase["user_id"])  # Get buyer info from the user db
        if buyer_info:
            product_info = products_db.get(purchase["product_id"])
            purchases_with_buyers.append({
                "purchase_id": purchase_id,
                "buyer": buyer_info,
                "product": product_info,
                "purchase_date": purchase["purchase_date"]
            })

    return purchases_with_buyers