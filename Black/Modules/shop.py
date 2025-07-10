from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.enums import ParseMode
from Black import bot
from Black.db import users, Banned

import random

# Shop items
shop_items = {
    "Magna": {
        "price": 1200,
        "data": {
            "id": "magna_01",
            "name": "Magna Swing",
            "rarity": "Rare",
            "atk": 150,
            "def": 100,
            "hp": 500,
        }
    },
    "Luck": {
        "price": 2000,
        "data": {
            "id": "luck_01",
            "name": "Luck Voltia",
            "rarity": "Epic",
            "atk": 220,
            "def": 120,
            "hp": 600,
        }
    }
}

shop_image = "https://files.catbox.moe/mtzne0.jpg"


# 🛒 /shop command
@bot.on_message(filters.command("shop") & ~filters.user(Banned))
async def show_shop(_, message: Message):
    caption = "**🛍️ Welcome to the Black Clover Shop!**\n\nChoose a character to recruit:"
    keyboard = [
        [InlineKeyboardButton(f"🧙‍♂️ Buy Magna", callback_data="buy_Magna")],
        [InlineKeyboardButton(f"⚡ Buy Luck", callback_data="buy_Luck")]
    ]
    await message.reply_photo(
        photo=shop_image,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 💸 Purchase character
@bot.on_callback_query(filters.regex(r"buy_(Magna|Luck)"))
async def purchase_character(_, query: CallbackQuery):
    user_id = query.from_user.id
    char_name = query.matches[0].group(1)
    item = shop_items.get(char_name)

    if not item:
        return await query.answer("❌ Item not found!", show_alert=True)

    user = await users.find_one({"_id": user_id})
    if not user:
        return await query.answer("❌ You're not registered. Use /start first.", show_alert=True)

    # Currency check
    if user.get("mana", 0) < item["price"]:
        return await query.answer("🚫 Not enough mana to recruit this character.", show_alert=True)

    # Add to DB
    await users.update_one(
        {"_id": user_id},
        {
            "$inc": {"mana": -item["price"]},
            "$push": {"characters": item["data"]}
        }
    )

    await query.message.edit_caption(
        caption=f"✅ You recruited **{item['data']['name']}** for **{item['price']} mana**!\nCheck your `/inventory` to view.",
        parse_mode=None
    )
    await query.answer("🎉 Character recruited!")