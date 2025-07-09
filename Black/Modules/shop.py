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