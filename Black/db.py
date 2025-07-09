from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["BlackGameBot"]
users = db["users"]

# Example document structure:
# {
#   "_id": 12345678,
#   "character": "Asta",
#   "data": { ... },  # Asta's full character data from character.py
#   "collection": [...]
# }
    {
      "Name": "Asta",
      "Attribute": "Anti-Magic",
      "Rarity": "Legendary"
    },
    {
      "Name": "Magna",
      "Attribute": "Fire",
      "Rarity": "Rare"
    },
    {
      "Name": "Luck",
      "Attribute": "Lightning",
      "Rarity": "Epic"
    }
  ]
}