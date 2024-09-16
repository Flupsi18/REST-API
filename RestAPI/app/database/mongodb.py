from motor.motor_asyncio import AsyncIOMotorClient
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

from ..core.config import Settings
from ..core.security import verify_password


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()
PyObjectId = Annotated[str, BeforeValidator(str)]


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongodb():
    db.client = AsyncIOMotorClient(str(Settings.MONGODB_URL))


async def close_mongodb_connection():
    db.client.close()


class DataService:

    @staticmethod
    async def get_customer_by_name(name: str):
        db = await get_database()
        customer = await db.get_collection("customers").find_one({"name": name})
        return customer

    @staticmethod
    async def authenticate_customer(name: str, password: str):
        customer = await DataService.get_customer_by_name(name)

        # print(get_password_hash(password))
        if not customer:
            return None
        if not verify_password(customer.get("password"), password):
            return None
        return customer
