from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Black import bot
from Black.db import users
from Black.character.character import Magna, Luck

@bot.on_message(filters.command("shop"))
async def open_shop(_, message: Message):
    photo = "https://files.catbox.moe/mtzne0.jpg"  # use your shop image URL

    caption = "🛍️ Welcome to the Official BlackXdevil Shop!\n\nSelect a category below to begin shopping:"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧝‍♂️ Character", callback_data="shop_character")],
        [InlineKeyboardButton("🎁 Item", callback_data="shop_item")]
    ])
    await message.reply_photo(photo=photo, caption=caption, reply_markup=buttons)

@bot.on_callback_query(filters.regex("shop_"))
async def handle_shop_buttons(_, query: CallbackQuery):
    data = query.data

    if data == "shop_item":
        return await query.answer("🎁 Coming soon...", show_alert=True)

    elif data == "shop_character":
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🔥 {Magna['Name']} - 10,000 MP", callback_data="buy_magna")],
            [InlineKeyboardButton(f"⚡ {Luck['Name']} - 15,000 MP", callback_data="buy_luck")]
        ])
        await query.message.edit_text("🧝‍♂️ Select a character to purchase:", reply_markup=buttons)

@bot.on_callback_query(filters.regex("buy_"))
async def handle_buy(_, query: CallbackQuery):
    user_id = query.from_user.id
    user = await users.find_one({"_id": user_id})

    if not user:
        return await query.answer("❌ Please start the bot first using /start.", show_alert=True)

    char = Magna if query.data == "buy_magna" else Luck
    price = 10000 if query.data == "buy_magna" else 15000

    mana = user.get("mana", 0)
    collection = user.get("collection", [])

    # Check already owned
    if any(c["Name"] == char["Name"] for c in collection):
        return await query.answer(f"✅ You already own {char['Name']}.", show_alert=True)

    if mana < price:
        return await query.answer("⚠️ Not enough mana points.", show_alert=True)

    # Deduct mana & add character
    collection.append({
        "Name": char["Name"],
        "Attribute": char["Attribute"],
        "Rarity": char["Rarity"]
    })

    await users.update_one(
        {"_id": user_id},
        {"$set": {"collection": collection, "mana": mana - price}}
    )

    caption = f"🎉 Congratulations! You've successfully purchased {char['Name']}!\n\n🧝‍♂️ Attribute: {char['Attribute']}\n🧪 Rarity: {char['Rarity']}"
    
    await query.message.delete()
    await bot.send_photo(
        chat_id=query.message.chat.id,
        photo=char["Pic"],
        caption=caption
    )