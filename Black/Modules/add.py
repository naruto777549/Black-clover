from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from Black import bot
from Black.db import users, Banned
from Black.config import DEVS  # Ensure you have DEVS defined in config

@bot.on_message(filters.command("add") & filters.user(DEVS), group=32)
async def add_mana_magic(_, msg: Message):
    args = msg.command
    reply = msg.reply_to_message

    # ✅ Format 1: /add <mana> <magic> [used on reply]
    if reply and len(args) >= 3:
        target_id = reply.from_user.id
        try:
            mana = int(args[1])
            magic = int(args[2])
        except:
            return await msg.reply("⚠️ Usage: `/add <mana> <magic>` (while replying)", parse_mode=ParseMode.MARKDOWN)

    # ✅ Format 2: /add <user_id> <mana> <magic>
    elif len(args) >= 4:
        try:
            target_id = int(args[1])
            mana = int(args[2])
            magic = int(args[3])
        except:
            return await msg.reply("⚠️ Usage: `/add <user_id> <mana> <magic>`", parse_mode=ParseMode.MARKDOWN)
    else:
        return await msg.reply("⚠️ Invalid format.\nUse:\n• `/add <user_id> <mana> <magic>`\n• Or reply with `/add <mana> <magic>`", parse_mode=ParseMode.MARKDOWN)

    # ❌ Banned check
    if target_id in Banned:
        return await msg.reply("🚫 This user is banned. Cannot add rewards.")

    # ✅ Update mana and magic points
    await users.update_one(
        {"_id": target_id},
        {"$inc": {"mana": mana, "magic": magic}},
        upsert=True
    )

    await msg.reply(
        f"✅ Successfully added:\n🔹 Mana: `{mana}`\n🔸 Magic Points: `{magic}`\n👤 To: `{target_id}`",
        parse_mode=ParseMode.MARKDOWN
    )