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