from pyrogram import filters

from core.client import app
from core.cache import (
    audio_cache,
    search_cache
)
from core.vc_player import (
    active_chats
)


@app.on_message(
    filters.command("health")
)
async def health_command(
    client,
    message
):

    await message.reply_text(
        f"🩺 Mahi Health\n\n"
        f"🎙 Active Chats: {len(active_chats)}\n"
        f"🎵 Audio Cache: {len(audio_cache)}\n"
        f"🔎 Search Cache: {len(search_cache)}"
    )