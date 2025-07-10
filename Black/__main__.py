#__main__.py
from pyrogram import Client, filters
from BEY import bot
from BEY.Modules import *

if __name__=="__main__":
    bot.run()
    with bot:
        bot.send_message(chat_id=7576729648,
                               text="BOT IS STARTED")