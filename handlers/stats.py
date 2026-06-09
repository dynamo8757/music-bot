from pyrogram import filters

from core.client import app
from core.player_state import (
    stats
)

from core.vc_player import (
    active_chats
)


@app.on_message(
    filters.command("stats")
)
async def stats_command(
    client,
    message
):

    await message.reply_text(
        f"📊 Mahi Stats\n\n"
        f"🎵 Songs Played: {stats['songs_played']}\n"
        f"🔎 Searches: {stats['searches']}\n"
        f"⚡ Cache Hits: {stats['cache_hits']}\n"
        f"🎙 Active Chats: {len(active_chats)}"
    )