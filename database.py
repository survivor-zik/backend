import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = f"""mongodb+srv://{os.getenv("ID")}:{os.getenv("PASSWORD")}@cluster0.3kp8bag.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"""

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, uuidRepresentation='standard')

database = client.Ecom

user_collection = database.get_collection("User")
product_collection = database.get_collection("Products")
purchase_collection = database.get_collection("Purchases")
