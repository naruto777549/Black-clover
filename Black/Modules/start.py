from pyrogram import filters
from Black import bot

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text("👋 Welcome to Black Game Bot! Use /play to begin your journey!")