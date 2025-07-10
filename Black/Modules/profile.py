from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Black import bot
from Black.db import users
from PIL import Image, ImageDraw
import os

@bot.on_message(filters.command("profile"))
async def profile(_, message: Message):
    user_id = message.from_user.id
    user = await users.find_one({"_id": user_id})

    if not user:
        return await message.reply_text("❌ You haven't started the game yet. Use /start first!")

    name = message.from_user.first_name

    # Download user profile photo if available
    pfp_path = None
    if message.from_user.photo:
        photo = await bot.download_media(message.from_user.photo.big_file_id)
        pfp_path = photo

    # Load local background image
    bg_image = Image.open("Black/assets/profile_bg.jpg").convert("RGBA")

    # Add circular PFP
    if pfp_path:
        pfp_img = Image.open(pfp_path).resize((270, 270)).convert("RGBA")  # Bigger size
        mask = Image.new("L", (270, 270), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 270, 270), fill=255)
        pfp_img.putalpha(mask)

        # ✅ Center-left placement (tweak X, Y as needed)
        pfp_x = 30
        pfp_y = 30
        bg_image.paste(pfp_img, (pfp_x, pfp_y), pfp_img)

    # Save final image
    final_path = f"/tmp/{user_id}_profile.png"
    bg_image.save(final_path)

    # Profile Text
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

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 More Stats", callback_data="more_stats")]
    ])

    await message.reply_photo(
        photo=final_path,
        caption=profile_text,
        reply_markup=buttons
    )

# More Stats
@bot.on_callback_query(filters.regex("more_stats"))
async def advanced_stats(_, query):
    user_id = query.from_user.id
    user = await users.find_one({"_id": user_id})
    if not user:
        return await query.answer("❌ No data found!", show_alert=True)

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

    await query.message.edit_caption(stats, reply_markup=back_btn, parse_mode=None)

# Back to Profile
@bot.on_callback_query(filters.regex("back_profile"))
async def back_to_profile(_, query):
    fake_msg = query.message
    fake_msg.from_user = query.from_user
    await profile(bot, fake_msg)  