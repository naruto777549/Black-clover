from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Black import bot
from Black.db import users
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

@bot.on_message(filters.command("profile"))
async def profile(_, message: Message):
    user_id = message.from_user.id
    user = await users.find_one({"_id": user_id})

    if not user:
        return await message.reply_text("❌ You haven't started the game yet. Use /start first!")

    name = message.from_user.first_name
    pfp = await bot.download_media(message.from_user.photo.big_file_id) if message.from_user.photo else None

    # Load background image (Asta or anyone based on character)
    bg_url = user["data"]["Pic"]  # already stored in character data
    bg_response = requests.get(bg_url)
    bg_image = Image.open(BytesIO(bg_response.content)).convert("RGBA")

    # Add circular PFP if available
    if pfp:
        pfp_img = Image.open(pfp).resize((200, 200)).convert("RGBA")
        mask = Image.new("L", (200, 200), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 200, 200), fill=255)
        pfp_img.putalpha(mask)
        bg_image.paste(pfp_img, (30, 30), pfp_img)

    # Save final image
    final_path = f"/tmp/{user_id}_profile.png"
    bg_image.save(final_path)

    # Build Profile Text
    profile_text = f"""
╭── ❰ 🧾 𝗣𝗥𝗢𝗙𝗜𝗟𝗘 ❱ ──╮
│ 👤 Name: {name}
│ 🆔 ID: {user_id}
│ 🧪 Level: {user.get('level', 1)}
│ 📈 EXP: {user.get('exp', 0)}
│ 🧿 Mana: {user.get('mana', 0)}
│ 💦 Magic Points: {user.get('magic', 0)}
│ 🏰 Guild: {user.get('guild', 'None')}
│ 🎖️ Role: {user.get('role', 'None')}
╰────────────────────╯
    """

    # Inline Buttons
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 More Stats", callback_data="more_stats")],
    ])

    await message.reply_photo(
        photo=final_path,
        caption=profile_text,
        reply_markup=buttons
    )

@bot.on_callback_query(filters.regex("more_stats"))
async def advanced_stats(_, query):
    user_id = query.from_user.id
    user = await users.find_one({"_id": user_id})
    if not user:
        return await query.answer("❌ No data found!", show_alert=True)

    # Build Stats
    stats = f"""
📊 <b>Advanced Stats</b>:
• 🗡️ Explores: {user.get("explores", 0)}
• ⚜️ Challenges: {user.get("challenges", 0)}
• 🥇 Wins: {user.get("wins", 0)}
• ❌ Losses: {user.get("losses", 0)}
• 📈 Win %: {user.get("winrate", 0.0)}%
• ✨ Characters: {len(user.get('collection', []))}
• 📆 Joined: {user.get("joined", "N/A")}
    """

    back_btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back_profile")]
    ])

    await query.message.edit_caption(stats, reply_markup=back_btn, parse_mode=None

@bot.on_callback_query(filters.regex("back_profile"))
async def back_to_profile(_, query):
    # Just re-trigger /profile logic
    fake_msg = query.message
    fake_msg.from_user = query.from_user
    await profile(bot, fake_msg)