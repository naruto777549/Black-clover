from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from Black import bot
from Black.character import asta, magna, luck

@bot.on_message(filters.command("stats"))
async def show_character(_, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage: `/stats Asta`", parse_mode=None)

    name = args[1].strip().lower()
    char = characters.get(name.title())

    if not char:
        return await message.reply("⚠️ Character not found.")

    photo = char["Pic"]
    caption = f"🌟 **{char['Name']}**\n🏅 Squad: `{char['Squad']}`\n🎖 Role: `{char['Role']}`\n⚔ Series: `{char['Series']}`\n✨ Rarity: `{char['Rarity']}`"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌀 Move Set", callback_data=f"moves_{char['Name']}")],
        [InlineKeyboardButton("📊 Stats", callback_data=f"stats_{char['Name']}")]
    ])

    await message.reply_photo(photo=photo, caption=caption, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

@bot.on_callback_query(filters.regex("^moves_(.+)"))
async def move_set(_, query: CallbackQuery):
    name = query.matches[0].group(1)
    char = characters.get(name)
    if not char:
        return await query.answer("Character not found.", show_alert=True)

    norm = "\n".join(f"• {move}" for move in char['Normal Moves'])
    spec = "\n".join(f"⭐ {move}" for move in char['Special Moves'])

    text = f"🎯 **{name}'s Move Set**\n\n🗡️ Normal Moves:\n{norm}\n\n💥 Special Moves:\n{spec}"
    await query.message.edit_caption(text, parse_mode=ParseMode.MARKDOWN)


@bot.on_callback_query(filters.regex("^stats_(.+)"))
async def stats_view(_, query: CallbackQuery):
    name = query.matches[0].group(1)
    char = characters.get(name)
    if not char:
        return await query.answer("Character not found.", show_alert=True)

    text = f"""
📊 **{name}'s Stats**

❤️ HP: `{char['HP']}`
⚔️ ATK: `{char['ATK']}`
🛡 DEF: `{char['DEF']}`
⚡ SPEED: `{char['SPEED']}`
🎯 ACCURACY: `{char['ACCURACY'] * 100}%`
💢 DAMAGE: `{char['DAMAGE']}`
🔰 Trait: `{char['Trait']}`
"""
    await query.message.edit_caption(text, parse_mode=ParseMode.MARKDOWN)