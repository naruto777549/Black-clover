from pyrogram import filters
from pyrogram.types import Message
from Black import bot
from Black.db import users

@bot.on_message(filters.command("mychar"))
async def mychar(_, message: Message):
    user_id = message.from_user.id
    user = await users.find_one({"_id": user_id})
    
    if not user:
        return await message.reply_text("❌ You haven't started the bot yet. Use /start to begin.")
    
    collection = user.get("collection", [])
    
    if not collection:
        return await message.reply_text("😢 You don't have any Magic Knights yet.")
    
    text = "🔰 <b>Your Magic Knights Collection:</b>\n\n"
    for i, char in enumerate(collection, start=1):
        text += f"[{i}] ➤ ❤‍🔥<b>{char['Name']}</b> | 🔰<b>{char['Attribute']}</b> | 🧪<b>{char['Rarity']}</b>\n"
    
    await message.reply_text(text, parse_mode="None")