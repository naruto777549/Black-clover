from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["BlackGameBot"]
users = db["users"]
users["collection"]
Banned = []
guilds = DB["GUILDS"]
Pre_Users = DB["PRE REGISTERED USERS"]
battle_col = DB["BATTLES"]
enemy_database = DB["ENEMY DATABASE"]