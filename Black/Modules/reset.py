from pyrogram import filters
from pyrogram.types import Message
from Black import bot
from Black.db import users
from config import ADMINS


@bot.on_message(filters.command("reset") & filters.user(ADMINS))
async def reset_command(_, message: Message):
    args = message.text.split()
    user_id = None

    # Case 1: By reply
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id

    # Case 2: By /reset <user_id or @username>
    elif len(args) > 1:
        target = args[1]
        if target.startswith("@"):
            try:
                user = await bot.get_users(target)
                user_id = user.id
            except:
                return await message.reply_text("❌ Invalid username.")
        else:
            if target.isdigit():
                user_id = int(target)
            else:
                return await message.reply_text("❌ Invalid user ID.")

    else:
        return await message.reply_text("ℹ️ Use: `/reset <user_id | @username>` or reply to user.", quote=True)

    # Try delete user from DB
    result = await users.delete_one({"_id": user_id})

    if result.deleted_count == 1:
        await message.reply_text(f"✅ Successfully reset user with ID: <code>{user_id}</code>", quote=True)
    else:
        await message.reply_text("⚠️ No user found in database.", quote=True)