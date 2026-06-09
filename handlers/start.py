from pyrogram import filters

from core.client import app
from core.ui import start_keyboard


# Replace with your Telegram banner file_id
BANNER_FILE_ID = "assets/mizuki banner.png"


@app.on_message(filters.command("start"))
async def start_command(
    client,
    message
):

    me = await app.get_me()

    text = """
🌙 <b>Welcome to Mizuki</b>

Not just another music bot.

━━━━━━━━━━━━━━━

⚡ <b>Quick Start</b>

1. Add Mizuki to your group
2. Give Admin permissions
3. Start a Voice Chat
4. Use <code>/play song name</code>

━━━━━━━━━━━━━━━

🎵 High Quality Music
📂 Smart Playlists
⬇️ Instant Downloads

━━━━━━━━━━━━━━━

Made with ❤️ by Shivam
"""

    await message.reply_photo(
        photo=BANNER_FILE_ID,
        caption=text,
        reply_markup=start_keyboard(
            me.username
        )
    )