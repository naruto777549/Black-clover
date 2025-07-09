from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["BlackGameBot"]
users = db["users"]

{
  "_id": 12345678,
  "character": "Asta",
  "data": { ... },  // first selected character
  "collection": [
    {
      "Name": "Asta",
      "Attribute": "Anti-Magic",
      "Rarity": "Legendary"
    },
    {
      "Name": "Magna",
      "Attribute": "Fire",
      "Rarity": "Rare"
    }
  ]
}