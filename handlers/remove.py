from pyrogram import filters

from core.client import app

from core.queue import (
    remove_from_queue,
    get_queue_song
)

from core.admins import (
    is_admin
)


@app.on_message(
    filters.command("remove")
)
async def remove_command(
    client,
    message
):
    try:
        if len(message.command) < 2:
            return await message.reply_text(
                "❌ Usage:\n\n/remove queue_number"
            )

        position = int(message.command[1])
        song = get_queue_song(message.chat.id, position)

        if not song:
            return await message.reply_text(
                "❌ Invalid queue position."
            )

        admin = await is_admin(
            message.chat.id,
            message.from_user.id
        )

        requester = False
        requested_by = song.get("requested_by")

        if isinstance(requested_by, dict) and requested_by.get("id") == message.from_user.id:
            requester = True

        if not admin and not requester:
            return await message.reply_text(
                "❌ You can only remove your own songs."
            )

        removed = remove_from_queue(message.chat.id, position)


        await message.reply_text(
            f"🗑 Removed\n\n"
            f"🎵 {removed['song']['title']}"
        )

    except ValueError:
        await message.reply_text(
            "❌ Queue position must be a number."
        )

    except Exception as e:
        await message.reply_text(
            f"❌ {e}"
        )