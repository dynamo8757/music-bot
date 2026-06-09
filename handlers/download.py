import os

from pyrogram import filters

from core.client import app

from core.player_state import (
    current_songs
)

from core.downloader import (
    download_song
)


@app.on_message(
    filters.command("download")
)
async def download_handler(
    client,
    message
):

    try:

        chat_id = message.chat.id

        if chat_id not in current_songs:

            return await message.reply(
                "❌ No song playing."
            )

        status = await message.reply(
            "📥 Downloading..."
        )

        song = current_songs[
            chat_id
        ]["song"]

        file_path, title = download_song(
            song["webpage_url"]
        )

        await app.send_audio(
            chat_id=message.from_user.id,
            audio=file_path,
            title=title,
            performer=song.get(
        "uploader",
        "Unknown"),
        )

        await status.edit_text(
            "✅ Check your DM."
        )

        try:

            os.remove(
                file_path
            )

        except Exception:
            pass

    except Exception as e:

        print(
            f"[DOWNLOAD ERROR] {e}"
        )

        try:

            await message.reply(
                "❌ Download failed."
            )

        except Exception:
            pass

