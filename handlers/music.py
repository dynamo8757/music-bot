from pyrogram import filters

from core.client import app

from core.ui import (
    SEARCHING,
    DOWNLOADING,
    assistant_missing_text,
    VOICE_CHAT_MISSING,
    added_to_queue
)

from core.checks import (
    is_assistant_in_chat,
    get_assistant_username,
    is_voice_chat_active,
    auto_join_assistant
)

from core.vc_player import (
    play_song
)

from core.player_card import (
    send_or_update_player_card
)

from core.player_state import (
    queue_messages
)

from core.progress import (
    build_progress_bar
)

from core.player_state import (
    progress_messages
)

@app.on_message(filters.command("play"))
async def play_command(client, message):
    try:
        if len(message.command) < 2:
            return await message.reply_text(
                "❌ Usage:\n\n/play song name"
            )

        chat_id = message.chat.id
        query = " ".join(message.command[1:])

        assistant_ok = await is_assistant_in_chat(chat_id)

        if not assistant_ok:
            status = await message.reply_text(
                "🤖 Adding assistant..."
            )

            joined = await auto_join_assistant(chat_id)

            if not joined:
                username = await get_assistant_username()
                return await status.edit_text(
                    assistant_missing_text(username)
                )

            await status.edit_text(
                "✅ Assistant joined."
            )

        voice_chat_ok = await is_voice_chat_active(chat_id)

        if not voice_chat_ok:
            return await message.reply_text(
                VOICE_CHAT_MISSING
            )

        status = await message.reply_text(SEARCHING)
        await status.edit_text(DOWNLOADING)

        result = await play_song(
            chat_id,
            query,
            {
                "name": message.from_user.first_name,
                "id": message.from_user.id
            }
        )

        if not result["success"]:
            return await status.edit_text(
                f"❌ {result['message']}"
            )

        if result.get("queued"):
            await status.edit_text(
                added_to_queue(
                    result["song"]["title"],
                    result["position"]
                )
            )

            if chat_id not in queue_messages:
                queue_messages[chat_id] = {}

            queue_messages[chat_id][result["song"]["title"]] = status.id
            return

        await status.delete()

        await send_or_update_player_card(
            chat_id=chat_id,
            song=result["song"],
            requested_by=result.get(
                "requested_by",
                message.from_user.first_name
            )
        )


    except Exception as e:

        await message.reply_text(
            f"❌ Error\n\n{e}"
        )