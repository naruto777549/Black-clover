from Black import bot
from pyrogram import idle
from Black.Modules import start
from Black.Modules import reset

if __name__ == "__main__":
    bot.start()
    print("✅ BlackGameBot is online.")
    idle()
    bot.stop()
