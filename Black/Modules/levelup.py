from pyrogram import filters
from pyrogram.types import Message
from Black import bot
from Black.db import users
from config import ADMINS

# XP required for next level
def get_xp_required(level: int) -> int:
    return 100 * level

# 🆙 Level up handler function
async def check_and_level_up(user_id: int, message: Message = None):
    user = await users.find_one({"_id": user_id})

    if not user:
        return  # User not found

    current_xp = user.get("xp", 0)
    current_level = user.get("level", 1)
    xp_needed = get_xp_required(current_level)

    # Loop in case user has enough XP for multiple level-ups
    leveled_up = False
    while current_xp >= xp_needed:
        current_level += 1
        current_xp -= xp_needed
        xp_needed = get_xp_required(current_level)
        leveled_up = True

    if leveled_up:
        mana_gain = 10 * current_level
        magic_gain = 5 * current_level

        await users.update_one(
            {"_id": user_id},
            {
                "$set": {"xp": current_xp, "level": current_level},
                "$inc": {"mana": mana_gain, "magic": magic_gain}
            }
        )

        if message:
            await message.reply(
                f"🎉 **Level Up!**\n\n"
                f"🆙 New Level: `{current_level}`\n"
                f"🔹 Mana +{mana_gain}\n"
                f"🔸 Magic +{magic_gain}"
            )

# ✅ Admin command to manually add XP
@bot.on_message(filters.command("addxp") & filters.user(ADMINS))
async def add_xp(_, message: Message):
    args = message.command
    reply = message.reply_to_message

    if reply and len(args) == 2:
        try:
            xp_amount = int(args[1])
            user_id = reply.from_user.id
        except:
            return await message.reply("❌ Usage: `/addxp <amount>` on a replied user.")
    elif len(args) == 3:
        try:
            user_id = int(args[1])
            xp_amount = int(args[2])
        except:
            return await message.reply("❌ Usage: `/addxp <user_id> <amount>`")
    else:
        return await message.reply("❌ Usage:\n• `/addxp <amount>` (reply to user)\n• `/addxp <user_id> <amount>`")

    await users.update_one(
        {"_id": user_id},
        {"$inc": {"xp": xp_amount}},
        upsert=True
    )

    dummy = await message.reply(f"✅ Added `{xp_amount}` XP to `{user_id}`.")
    await check_and_level_up(user_id, dummy)

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Black import bot
from Black.db import users  # Assuming users = Mongo collection

@bot.on_message(filters.command("levelup") & filters.private)
async def levelup_menu(_, message: Message):
    user_id = message.from_user.id
    user = await users.find_one({"_id": user_id})

    if not user:
        return await message.reply("⚠️ You're not registered!")

    characters = user.get("characters", [])
    if not characters:
        return await message.reply("😕 You don't have any characters to level up.")

    buttons = [
        [InlineKeyboardButton(f"{char['name']} (Lvl {char['level']})", callback_data=f"lvl_char_{char['id']}")]
        for char in characters
    ]
    await message.reply(
        "🧙 **Choose a character to level up:**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

from pyrogram.types import CallbackQuery
from pyrogram.enums import ParseMode

@bot.on_callback_query(filters.regex(r"lvl_char_(\d+)"))
async def levelup_character(_, query: CallbackQuery):
    user_id = query.from_user.id
    char_id = int(query.matches[0].group(1))

    user = await users.find_one({"_id": user_id})
    if not user:
        return await query.answer("User not found.", show_alert=True)

    xp = user.get("xp", 0)
    mana = user.get("mana", 0)

    characters = user.get("characters", [])
    character = next((c for c in characters if c["id"] == char_id), None)
    if not character:
        return await query.answer("Character not found.", show_alert=True)

    level = character.get("level", 1)
    if level >= 100:
        return await query.answer("🔝 Max Level Reached!", show_alert=True)

    xp_cost = level * 100
    mana_cost = level * 50

    if xp < xp_cost or mana < mana_cost:
        return await query.answer(f"❌ Need {xp_cost} XP and {mana_cost} Mana to level up.", show_alert=True)

    # Deduct XP and Mana and increase level
    character["level"] += 1
    await users.update_one(
        {"_id": user_id},
        {
            "$set": {"characters": characters},
            "$inc": {"xp": -xp_cost, "mana": -mana_cost}
        }
    )

    await query.message.edit_text(
        f"🎉 **{character['name']} leveled up to Level {character['level']}!**\n\n"
        f"🧪 XP Used: `{xp_cost}`\n🔮 Mana Used: `{mana_cost}`",
        parse_mode=ParseMode.MARKDOWN
    )
    await query.answer("✅ Level Up Successful!", show_alert=True)