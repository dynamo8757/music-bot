from pyrogram import filters

from core.client import app

from core.player_state import (
    current_songs
)


@app.on_message(
    filters.command("nowplaying")
)
async def nowplaying_command(
    client,
    message
):

    chat_id = message.chat.id

    if chat_id not in current_songs:

        return await message.reply_text(
            "📭 Nothing is playing."
        )

    song = current_songs[
        chat_id
    ]["song"]

    requested_by = current_songs[
        chat_id
    ].get(
        "requested_by",
        "Unknown"
    )

    if isinstance(
        requested_by,
        dict
    ):

        requested_by = requested_by.get(
            "name",
            "Unknown"
        )

    await message.reply_text(
        f"🎵 **NOW PLAYING**\n\n"
        f"🎧 **{song['title']}**\n\n"
        f"👤 Requested By: "
        f"{requested_by}\n"
    )