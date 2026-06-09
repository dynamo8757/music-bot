from pyrogram import filters

from core.client import app

from core.queue import (
    clear_queue
)

from core.admins import (
    is_admin
)


@app.on_message(
    filters.command("clearqueue")
)
async def clearqueue_command(
    client,
    message
):

    admin = await is_admin(
        message.chat.id,
        message.from_user.id
    )

    if not admin:

        return await message.reply_text(
            "❌ Only group admins can clear the queue."
        )

    clear_queue(
        message.chat.id
    )

    await message.reply_text(
        "🗑 Queue Cleared."
    )