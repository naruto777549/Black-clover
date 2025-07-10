from pyrogram import filters
from pyrogram.types import Message
from Black import bot
from config import ADMINS, LOGS_CHANNEL
from Black.db import Users, Banned

# Runtime in-memory Banned List
BANNED = Banned  # Pre-loaded from DB or empty list


async def block_user(user_id: int):
    if user_id not in BANNED:
        BANNED.append(user_id)
        print(f"[BANNED] User {user_id}")
    else:
        print(f"[SKIP] Already banned: {user_id}")


async def unblock_user(user_id: int):
    try:
        BANNED.remove(user_id)
        print(f"[UNBANNED] User {user_id}")
    except ValueError:
        print(f"[SKIP] User {user_id} not found in banned list")


async def is_banned(user_id: int) -> bool:
    return user_id in BANNED


# ───────────── Ban Command ─────────────
@bot.on_message(filters.command("hardban") & filters.user(ADMINS), group=13)
async def hardban_user(client, message: Message):
    args = message.text.split(maxsplit=2)

    if len(args) < 2:
        return await message.reply("❌ Usage: /hardban <user_id> <reason>")

    try:
        user_id = int(args[1])
    except ValueError:
        return await message.reply("⚠️ Invalid user ID. Must be numeric.")

    reason = args[2] if len(args) > 2 else "No reason provided"

    if user_id in ADMINS:
        return await message.reply("🚫 Cannot ban a bot admin.")

    if user_id in BANNED:
        return await message.reply("⚠️ User already banned.")

    await Users.delete_one({"_id": user_id})
    await block_user(user_id)

    msg = f"""
🔒 **BAN ALERT**

👤 User ID: `{user_id}`
🔗 Mention: [User](tg://user?id={user_id})
🛡️ Banned By: [{message.from_user.first_name}](tg://user?id={message.from_user.id})
📌 Reason: `{reason}`
"""

    await message.reply(msg, parse_mode=None)
    if LOGS_CHANNEL:
        await client.send_message(LOGS_CHANNEL, msg, parse_mode=None)


# ───────────── Unban Command ─────────────
@bot.on_message(filters.command("unhardban") & filters.user(ADMINS), group=13)
async def unban_user(client, message: Message):
    args = message.text.split()

    if len(args) < 2:
        return await message.reply("❌ Usage: /unhardban <user_id>")

    try:
        user_id = int(args[1])
    except ValueError:
        return await message.reply("⚠️ Invalid user ID. Must be numeric.")

    if user_id not in BANNED:
        return await message.reply("✅ This user is not banned.")

    await unblock_user(user_id)

    msg = f"""
🔓 **UNBAN ALERT**

👤 User ID: `{user_id}`
🔗 Mention: [User](tg://user?id={user_id})
✅ Unbanned By: [{message.from_user.first_name}](tg://user?id={message.from_user.id})
"""

    await message.reply(msg, parse_mode=None)
    if LOGS_CHANNEL:
        await client.send_message(LOGS_CHANNEL, msg, parse_mode=None)