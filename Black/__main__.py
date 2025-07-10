import os
import importlib

from Black import bot
from pyrogram import idle

MODULES_PATH = "Black/Modules"

# Auto-import all .py files from Modules
for filename in os.listdir(MODULES_PATH):
    if filename.endswith(".py") and not filename.startswith("__"):
        importlib.import_module(f"Black.Modules.{filename[:-3]}")

if __name__ == "__main__":
    bot.start()
    bot.send_message(7576729648, "✅ Bot is Online")
    idle()
    bot.stop()