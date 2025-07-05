import os

API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
MONGO_URL = os.getenv("MONGO_URL", "your_mongo_url")
ADMINS = list(map(int, os.getenv("ADMINS", "123456789").split()))
BOT_USER = os.getenv("BOT_USER", "your_bot_username")