from Black import bot
from pyrogram import idle

# Import all command handlers
from Black.Modules import start, reset, char, shop, inventory, profile

print("🚀 Starting the bot...")

if __name__ == "__main__":
    bot.start()
    print("✅ Bot is running...")
    idle()
    print("⛔ Bot stopped.")
    bot.stop()