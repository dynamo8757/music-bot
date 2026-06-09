from pyrogram.types import (
    InputMediaPhoto
)

from core.youtube import (
    format_duration
)

from core.ui import (
    player_keyboard
)

from core.card_generator import (
    generate_card
)

from core.progress import (
    build_progress_bar
)

from core.player_state import (
    player_messages,
    playback_status,
    volume_levels,
    autoplay_modes,
    play_modes,
    controls_expanded
)

from core.client import app

from core.queue import (
    queue_length
)


def build_player_caption(
    song,
    requested_by="Unknown",
    status="▶ Playing"
):
    if isinstance(
        requested_by,
        dict
    ):
        requested_by = requested_by.get(
            "name",
            "Unknown"
        )
    volume = volume_levels.get(
        song.get("_chat_id", 0),
        100
    )
    queue_count = 0

    progress = build_progress_bar(
        song["_chat_id"],
        song["duration"]
    )

    return f"""🎵 **{song['title']}**

👤 Requested By: **{requested_by}**
⏱ Duration: **{format_duration(song['duration'])}**

{status}
{progress}

✨ Mizuki🖤
"""

def get_player_keyboard(chat_id):

    status = playback_status.get(
        chat_id,
        "playing"
    )

    autoplay = autoplay_modes.get(
        chat_id,
        True
    )

    mode = play_modes.get(
        chat_id,
        "queue"
    )
    return player_keyboard(
        status,
        autoplay,
        mode,
        controls_expanded.get(
            chat_id,
            False
        )
    )



async def refresh_player_card(
    chat_id,
    song,
    requested_by="Unknown",
    status="▶ Playing"
):

    try:

        if chat_id not in player_messages:
            return

        song["_chat_id"] = chat_id

        caption = build_player_caption(
            song,
            requested_by,
            ( "⏸ Paused"
        if playback_status.get(chat_id) == "paused"
        else "▶ Playing")
        )
        

        await app.edit_message_caption(
            chat_id=chat_id,
            message_id=player_messages[chat_id],
            caption=caption,
            reply_markup=get_player_keyboard(
                chat_id
            )
        )

    except Exception as e:

        if "MESSAGE_NOT_MODIFIED" not in str(e):

            print(
                f"Refresh Card Error: {e}"
            )

async def send_or_update_player_card(
    chat_id,
    song,
    requested_by="Unknown",
    status="▶ Playing"
):
    song["_chat_id"] = chat_id
    caption = build_player_caption(
    song,
    requested_by,
    status)

    try:
        # Delete old card
        old_msg = player_messages.get(chat_id)

        if old_msg:
            try:
                await app.delete_messages(chat_id, old_msg)
            except Exception:
                pass
        card_path = generate_card(
            song,
            requested_by,
            chat_id
        )

        msg = await app.send_photo(
            chat_id,
            photo=card_path,
            caption=caption,
            reply_markup=get_player_keyboard(chat_id)
        )

        player_messages[chat_id] = msg.id
    except Exception as e:
        print(f"Player Card Error: {e}")
        try:
            card_path = generate_card(
                song,
                requested_by,
                chat_id
            )

            msg = await app.send_photo(
                chat_id,
                photo=card_path,
                caption=caption,
                reply_markup=get_player_keyboard(chat_id)
            )

            player_messages[chat_id] = msg.id
        except Exception as ex:
            print(f"Fallback Card Error: {ex}")