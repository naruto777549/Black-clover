import os
import sys
import io
import traceback
from datetime import datetime
from subprocess import getoutput as run
from pyrogram.enums import ChatAction
from pyrogram import Client, filters
from pyrogram.types import Message

from Black import bot as app  # Your app instance

# Command prefix and bot owner
prefix = [".", "!", "?", "*", "$", "#", "/"]
BOT_OWNER_ID = [7576729648]

# ───────────── Shell Command ─────────────
@bot.on_message(filters.command("sh", prefix) & filters.user(BOT_OWNER_ID), group=11)
async def shell_command(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("🚫 No input provided!")

    code = " ".join(message.command[1:])
    try:
        output = run(code)
        result = f"**📎 Input:**\n```bash\n{code}```\n\n**📒 Output:**\n```bash\n{output}```"
        await message.reply_text(result)
    except Exception as e:
        with io.BytesIO(str(e).encode()) as out_file:
            out_file.name = "shell_error.txt"
            await message.reply_document(document=out_file, caption="❌ Shell Command Error")


# ───────────── Async Python Eval ─────────────
async def aexec(code: str, client: Client, message: Message):
    exec(
        "async def __aexec(client, message):"
        + "".join(f"\n {line}" for line in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@bot.on_message(filters.command("eval", prefix) & filters.user(BOT_OWNER_ID), group=10)
async def evaluate_code(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("🚫 No Python code provided!")

    code = message.text.split(" ", 1)[1]
    status = await message.reply_text("⏳ Processing...")

    start_time = datetime.now()

    # Redirect stdout/stderr
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        await aexec(code, client, message)
    except Exception:
        result = traceback.format_exc()
    else:
        result = sys.stdout.getvalue() or sys.stderr.getvalue() or "✅ Success"
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    duration = (datetime.now() - start_time).microseconds // 1000
    output_text = (
        f"📎 **Input:**\n```python\n{code}```\n\n"
        f"📒 **Output:**\n```python\n{result.strip()}```\n\n"
        f"⚡ **Time:** `{duration}ms`"
    )

    if len(output_text) > 4096:
        with io.BytesIO(output_text.encode()) as f:
            f.name = "eval_output.txt"
            await message.reply_document(document=f, caption="📄 Eval Result")
        await status.delete()
    else:
        await status.edit_text(output_text)


# ───────────── Recent Logs ─────────────
@bot.on_message(filters.command(["log", "logs"], prefix) & filters.user(BOT_OWNER_ID), group=9)
async def latest_logs(_, message: Message):
    try:
        log_output = run("tail -n 20 logs.txt")
        await message.reply_text(f"📒 **Latest Logs:**\n```python\n{log_output}```")
    except Exception as e:
        await message.reply_text(f"❌ Error fetching logs:\n```{e}```")


# ───────────── Full Logs ─────────────
@bot.on_message(filters.command(["flog", "flogs"], prefix) & filters.user(BOT_OWNER_ID), group=8)
async def full_logs(_, message: Message):
    try:
        logs = run("cat logs.txt")
        notice = await message.reply_text("📤 Sending full logs...")
        await app.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
        with io.BytesIO(logs.encode()) as doc:
            doc.name = "full_logs.txt"
            await message.reply_document(document=doc, caption="📄 Full Log File")
        await notice.delete()
    except Exception as e:
        await message.reply_text(f"❌ Error fetching full logs:\n```{e}```")