#__main__.py
from pyrogram import Client, filters
from Black import bot
from Black.Modules import *

if __name__=="__main__":
    bot.run()
    with bot:
        bot.send_message(chat_id=7576729648,
                               text="BOT IS STARTED")