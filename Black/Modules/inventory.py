from pyrogram import filters
from pyrogram.types import Message
from Black import bot
from Black.db import users

@bot.on_message(filters.command("inventory"))
async def inventory(_, message: Message):
    user_id = message.from_user.id
    user = await users.find_one({"_id": user_id})

    if not user:
        return await message.reply_text("❌ Please start the bot first using /start.")

    name = message.from_user.first_name
    mana = user.get("mana", 0)
    magic = user.get("magic", 0)
    permit = user.get("tournament_permit", 0)
    travel = user.get("travel_cards", 0)

    text = f"""
╭── ❰ 🎮 𝗜𝗡𝗩𝗘𝗡𝗧𝗢𝗥𝗬 𝗣𝗔𝗡𝗘𝗟 ❱ ──╮
│ 👤 𝗡𝗮𝗺𝗲: {name}
│ 💰 𝗠𝗮𝗻𝗮-𝗣𝗼𝗶𝗻𝘁𝘀: {mana}
│ 🔮 𝗠𝗮𝗴𝗶𝗰-𝗣𝗼𝗶𝗻𝘁𝘀: {magic}
│ 📄 𝗧𝗼𝘂𝗿𝗻𝗮𝗺𝗲𝗻𝘁-𝗣𝗲𝗿𝗺𝗶𝘁: {permit}
│ 💳 𝗧𝗿𝗮𝘃𝗲𝗹-𝗖𝗮𝗿𝗱𝘀: {travel}
╰────────────────────────╯
"""
    await message.reply_text(text)