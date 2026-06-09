from pyrogram import filters

from core.client import app

from core.vc_player import active_chats

from core.cache import (
    audio_cache,
    search_cache
)

from core.player_state import (
    current_songs,
    playback_status,
    volume_levels,
    autoplay_modes,
    play_modes
)


@app.on_message(
    filters.command("debug")
)
async def debug_command(
    client,
    message
):

    await message.reply_text(
        f"🛠 Debug Info\n\n"
        f"🎙 Active Chats: {len(active_chats)}\n"
        f"🎵 Current Songs: {len(current_songs)}\n"
        f"▶ Playback States: {len(playback_status)}\n"
        f"🔊 Volume States: {len(volume_levels)}\n"
        f"♾ AutoPlay States: {len(autoplay_modes)}\n"
        f"🔀 Mode States: {len(play_modes)}\n\n"
        f"🎧 Audio Cache: {len(audio_cache)}\n"
        f"🔎 Search Cache: {len(search_cache)}"
    )