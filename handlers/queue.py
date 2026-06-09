from pyrogram import filters

from core.client import app

from core.queue import get_queue

from core.player_state import (
    current_songs
)


@app.on_message(filters.command("queue"))
async def queue_command(
    client,
    message
):

    queue = get_queue(
        message.chat.id
    )

    if not queue:

        return await message.reply_text(
            "📭 Queue is empty."
        )

    text = "📜 **Current Queue**\n\n"

    if message.chat.id in current_songs:

        now_playing = current_songs[
            message.chat.id
        ]["song"]["title"]

        text += (
            f"▶ **Now Playing**\n"
            f"{now_playing}\n\n"
            f"━━━━━━━━━━━━━━━\n\n"
        )

    text += (
        f"━━━━━━━━━━━━━━━\n\n"
        f"🎵 Songs In Queue: {len(queue)}\n\n"
    )

    for i, item in enumerate(
        queue,
        start=1
    ):

        title = item["song"]["title"]

        if len(title) > 50:
            title = title[:50] + "..."

        requester = item.get(
            "requested_by",
            "Unknown"
        )

        if isinstance(
            requester,
            dict
        ):
            requester = requester.get(
                "name",
                "Unknown"
            )

        text += (
            f"🎶 {i}. {title}\n"
            f"👤 Requested By: {requester}\n\n"
        )

    await message.reply_text(
        text
    )