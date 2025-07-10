from pyrogram import filters
from pyrogram.types import Message
from Black import bot
from Black.db import users, Banned
from config import DEVS  # Add your developer IDs here

@bot.on_message(filters.command("add") & filters.user(DEVS))
async def add_mana_and_magic(_, message: Message):
    args = message.command
    reply = message.reply_to_message

    # 📌 Case 1: Used on reply -> /add <mana> <magic>
    if reply and len(args) == 3:
        try:
            target_id = reply.from_user.id
            mana = int(args[1])
            magic = int(args[2])
        except:
            return await message.reply("⚠️ Invalid values. Use: /add <mana> <magic> on a replied user.")

    # 📌 Case 2: Used directly -> /add <user_id> <mana> <magic>
    elif len(args) == 4:
        try:
            target_id = int(args[1])
            mana = int(args[2])
            magic = int(args[3])
        except:
            return await message.reply("⚠️ Invalid format. Use: /add <user_id> <mana> <magic>")
    else:
        return await message.reply("⚠️ Usage:\n• /add <user_id> <mana> <magic>\n• Or reply with /add <mana> <magic>")

    # 🚫 Check banned users
    if target_id in Banned:
        return await message.reply("🚫 This user is banned from using the bot.")

    # ✅ Add mana & magic
    await users.update_one(
        {"_id": target_id},
        {"$inc": {"mana": mana, "magic": magic}},
        upsert=True
    )

    await message.reply(
        f"✅ Mana & Magic Points added:\n\n👤 User ID: {target_id}\n🔹 Mana: {mana}\n🔸 Magic: {magic}"
    )