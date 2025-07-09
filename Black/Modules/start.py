from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from Black import bot
from config import BOT_USER
from Black.db import users
from Black.character.character import Asta, Magna, Luck  # import all characters
import random

# Character dict for easy access
all_characters = {
    "asta": Asta,
    "magna": Magna,
    "luck": Luck
}

# GROUP START
@bot.on_message(filters.command("start") & filters.group)
async def group_start(_, message: Message):
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🚀 Start in DM", url=f"https://t.me/{BOT_USER}?start=start")]]
    )
    await message.reply_text("⚠️ Please start the bot in private chat (DM) to begin your journey!", reply_markup=buttons)

# DM START
@bot.on_message(filters.command("start") & filters.private)
async def private_start(_, message: Message):
    user_id = message.from_user.id
    user = await users.find_one({"_id": user_id})
    
    if user:
        await message.reply_text("🛑 You’ve already started the bot!")
        return

    # Show character selection
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Asta", callback_data="char_asta")],
        [InlineKeyboardButton("🔥 Magna", callback_data="char_magna")],
        [InlineKeyboardButton("⚡ Luck", callback_data="char_luck")]
    ])
    
    await message.reply_photo(
        photo="https://files.catbox.moe/4sdthu.jpg",  # replace with your welcome image
        caption="👋 Welcome to the world of Magic Knights!\n\nChoose your starting character to begin your journey:",
        reply_markup=buttons
    )

# CHARACTER SELECT HANDLER
@bot.on_callback_query(filters.regex(r"char_(asta|magna|luck)"))
async def select_character(_, query: CallbackQuery):
    user_id = query.from_user.id
    char_key = query.data.split("_")[1]

    user = await users.find_one({"_id": user_id})
    if user:
        await query.answer("You’ve already started!", show_alert=True)
        return

    character = all_characters[char_key]
    await users.insert_one({
        "_id": user_id,
        "character": character["Name"],
        "data": character,
        "mana": 10000,  # 🧠 Add this line
        "collection": [
            {
                "Name": character["Name"],
                "Attribute": character["Attribute"],
                "Rarity": character["Rarity"]
            }
        ]
    })

    desc = f"""
🎉 <b>Congratulations {query.from_user.first_name}!</b>

You’ve chosen: <b>{character['Name']}</b>

👥 Squad: {character['Squad']}
⚔️ Role: {character['Role']}
🌪️ Attribute: {character['Attribute']}
❤️ HP: {character['HP']}
💥 ATK: {character['ATK']}
🛡️ DEF: {character['DEF']}
⚡ SPEED: {character['SPEED']}
🎯 Accuracy: {int(character['ACCURACY'] * 100)}%
🌟 Rarity: {character['Rarity']}

🧠 Trait: {character['Trait']}
🧿 Mana Points: <b>10,000</b>
📝 Description: {character['Description']}
"""
    await query.message.delete()
    await bot.send_photo(
        chat_id=query.message.chat.id,
        photo=character["Pic"],
        caption=desc,
        parse_mode=None
    )