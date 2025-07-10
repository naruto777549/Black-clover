from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["BlackGameBot"]

Users = db["users"] 
Users = Users 
Banned = []          

guilds = db["GUILDS"]
Pre_Users = db["PRE REGISTERED USERS"]
battle_col = db["BATTLES"]
enemy_database = db["ENEMY DATABASE"]