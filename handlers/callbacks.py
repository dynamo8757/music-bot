from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram import filters

from core.client import app

from core.vc_player import (
    pause_music,
    resume_music,
    stop_music,
    skip_music,
    pytgcalls
)
import time

from core.queue import (
    get_queue
)

from core.admins import (
    is_admin
)

from core.playlist_manager import (
    add_liked_song,
    get_playlists,
    add_song_to_playlist
)

from core.player_state import (
    current_songs,
    playback_status,
    player_messages,
    volume_levels,
    play_modes,
    autoplay_modes,
    controls_expanded,
    paused_at,
    paused_duration,
    song_start_times
)

from core.player_card import (
    refresh_player_card,
    send_or_update_player_card
)


@app.on_callback_query()
async def callback_handler(
    client,
    callback
):

    print(
        f"CALLBACK RECEIVED: {callback.data}"
    )
    try:

        chat_id = callback.message.chat.id

        user_id = callback.from_user.id

        data = callback.data
        if data == "show_controls":
            controls_expanded[
                chat_id
            ] = True

            if chat_id in current_songs:
                await refresh_player_card(
                    chat_id=chat_id,
                    song=current_songs[chat_id]["song"],
                    requested_by=current_songs[chat_id].get(
                        "requested_by",
                        "Unknown"
                    )
                )

            await callback.answer()
            return

        if data == "hide_controls":
            controls_expanded[
                chat_id
            ] = False

            if chat_id in current_songs:
                await refresh_player_card(
                    chat_id=chat_id,
                    song=current_songs[chat_id]["song"],
                    requested_by=current_songs[chat_id].get(
                        "requested_by",
                        "Unknown"
                    )
                )

            await callback.answer()
            return

        if data == "like":
            print("LIKE CLICKED")

            if chat_id not in current_songs:
                return await callback.answer(
                    "❌ No song playing",
                    show_alert=True
                )

            song = current_songs[
                chat_id
            ]["song"]["title"]

            added = add_liked_song(
                callback.from_user.id,
                song
            )

            if added:
                await callback.answer(
                    "❤️ Added to Liked Songs"
                )
            else:
                await callback.answer(
                    "❤️ Already Liked"
                )

            return

        if data in (
            "pause",
            "resume",
            "skip",
            "stop",
            "vol_down",
            "vol_up",
            "queue",
            "autoplay",
            "mode"
        ):
            admin = await is_admin(
                chat_id,
                user_id
            )

            requester = False

            if chat_id in current_songs:
                requested_by = current_songs[
                    chat_id
                ].get(
                    "requested_by"
                )

                if (
                    isinstance(
                        requested_by,
                        dict
                    )
                    and
                    requested_by.get(
                        "id"
                    ) == user_id
                ):
                    requester = True

            if not admin and not requester:
                return await callback.answer(
                    "❌ Only admins or the song requester can control music.",
                    show_alert=True
                )
            
        if data == "save_song":
            playlists = get_playlists(
                callback.from_user.id
            )

            if not playlists:
                await callback.answer(
                    "❌ Create a playlist first.",
                    show_alert=True
                )
                return

            buttons = []

            for playlist in playlists:
                buttons.append(
                    [
                        InlineKeyboardButton(
                            f"📂 {playlist[1]}",
                            callback_data=f"save_to:{playlist[1]}"
                        )
                    ]
                )

            await callback.message.reply_text(
                "📂 Select Playlist",
                reply_markup=InlineKeyboardMarkup(
                    buttons
                )
            )

            await callback.answer()
            return
        
        if data.startswith("save_to:"):
            playlist_name = data.split(
                ":",
                1
            )[1]

            if chat_id not in current_songs:

                await callback.answer(
                    "❌ No song playing",
                    show_alert=True
                )

                return

            song = current_songs[
                chat_id
            ]["song"]

            saved = add_song_to_playlist(
                callback.from_user.id,
                playlist_name,
                song
            )

            if saved:

                await callback.answer(
                    f"✅ Saved to {playlist_name}",
                    show_alert=True
                )

            else:

                await callback.answer(
                    "❌ Save failed",
                    show_alert=True
                )

            return

        if data == "pause":

            ok = await pause_music(chat_id)
            if ok:
                playback_status[chat_id] = "paused"
                paused_at[chat_id] = time.time()
                if chat_id in current_songs:
                    await refresh_player_card(
                        chat_id=chat_id,
                        song=current_songs[chat_id]["song"],
                        requested_by=current_songs[chat_id]["requested_by"],
                        status="⏸ Paused"
                    )
                await callback.answer("⏸ Music Paused")
            else:
                await callback.answer("❌ Failed")

        elif data == "resume":
            ok = await resume_music(chat_id)
            if ok:
                playback_status[chat_id] = "playing"
                # update paused duration
                if chat_id in paused_at:
                    pause_time = time.time() - paused_at[chat_id]
                    paused_duration[chat_id] = paused_duration.get(chat_id, 0) + pause_time
                    paused_at.pop(chat_id, None)
                if chat_id in current_songs:
                    await refresh_player_card(
                        chat_id=chat_id,
                        song=current_songs[chat_id]["song"],
                        requested_by=current_songs[chat_id]["requested_by"],
                        status="▶ Playing"
                    )
                await callback.answer("▶ Music Resumed")
            else:
                await callback.answer("❌ Failed")

        elif data == "skip":
            ok = await skip_music(chat_id)
            if ok:
                if chat_id in current_songs:
                    await send_or_update_player_card(
                        chat_id=chat_id,
                        song=current_songs[chat_id]["song"],
                        requested_by=current_songs[chat_id]["requested_by"],
                        status="⏭ Skipped"
                    )
                await callback.answer("⏭ Music Skipped")
            else:
                await callback.answer("❌ Failed")

        elif data == "stop":
            if chat_id in player_messages:
                try:
                    await app.delete_messages(
                        chat_id,
                        player_messages[chat_id]
                    )
                except Exception:
                    pass

                player_messages.pop(
                    chat_id,
                    None
                )
            await stop_music(chat_id)
            playback_status.pop(chat_id, None)
            current_songs.pop(chat_id, None)
            await callback.answer("⏹ Music Stopped")

        elif data == "vol_down":
            current = volume_levels.get(
                chat_id,
                100
            )

            current = max(
                0,
                current - 10
            )

            volume_levels[chat_id] = current
            if chat_id in current_songs:
                await refresh_player_card(
                    chat_id=chat_id,
                    song=current_songs[chat_id]["song"],
                    requested_by=current_songs[chat_id].get(
                        "requested_by",
                        "Unknown"
                    )
                )
            try:
                await pytgcalls.change_volume_call(
                    chat_id,
                    current
                )
            except Exception as e:
                print(f"Volume Error: {e}")

            await callback.answer(
                f"🔉 Volume: {current}%"
            )

        elif data == "vol_up":
            current = volume_levels.get(
                chat_id,
                100
            )

            current = min(
                200,
                current + 10
            )

            volume_levels[chat_id] = current
            if chat_id in current_songs:
                await refresh_player_card(
                    chat_id=chat_id,
                    song=current_songs[chat_id]["song"],
                    requested_by=current_songs[chat_id].get(
                        "requested_by",
                        "Unknown"
                    )
                )
            try:
                await pytgcalls.change_volume_call(
                    chat_id,
                    current
                )
            except Exception as e:
                print(f"Volume Error: {e}")

            await callback.answer(
                f"🔊 Volume: {current}%"
            )

        elif data == "autoplay":
            current = autoplay_modes.get(
                chat_id,
                True
            )

            autoplay_modes[chat_id] = (
                not current
            )

            if chat_id in current_songs:
                await refresh_player_card(
                    chat_id=chat_id,
                    song=current_songs[chat_id]["song"],
                    requested_by=current_songs[
                        chat_id
                    ].get(
                        "requested_by",
                        "Unknown"
                    )
                )

            await callback.answer(
                f"♾️ AutoPlay {'ON' if autoplay_modes[chat_id] else 'OFF'}"
            )

        elif data == "mode":
            current = play_modes.get(
                chat_id,
                "queue"
            )

            if current == "queue":
                play_modes[chat_id] = "shuffle"
            elif current == "shuffle":
                play_modes[chat_id] = "repeat"
            else:
                play_modes[chat_id] = "queue"

            if chat_id in current_songs:
                await refresh_player_card(
                    chat_id=chat_id,
                    song=current_songs[chat_id]["song"],
                    requested_by=current_songs[
                        chat_id
                    ].get(
                        "requested_by",
                        "Unknown"
                    )
                )

            await callback.answer(
                f"Mode: {play_modes[chat_id].title()}"
            )

        elif data == "queue":
            queue = get_queue(
                chat_id
            )

            if not queue:
                await callback.answer(
                    "📭 Queue Empty"
                )
                return

            text = (
                f"📜 **Current Queue**\n"
                f"🎵 Songs In Queue: {len(queue)}\n\n"
            )

            for i, song in enumerate(
                queue,
                start=1
            ):
                title = song["song"]["title"]

                if len(title) > 50:
                    title = title[:50] + "..."

                text += (
                    f"{i}. {title}\n"
                )

            await callback.message.reply_text(
                text
            )

            await callback.answer()

        if data == "help":

            await callback.message.reply_text(
                """
🎵 Music Commands

/play song_name or url
/pause -Pause the music
/resume -Resume the music
/skip -Skip the current song and play the next one in the queue
/stop -Stop playback and clear the queue
/queue -Show the queue list
/download -Download the current playing song
/nowplaying -Show current playing song

━━━━━━━━━━━━━━━

ℹ️ Information Commands

/stats - Show bot usage stats
/health - Show bot health status
/debug - Show debug information

━━━━━━━━━━━━━━━

📂 Playlist Commands

/createplaylist Name
/playlists
/playlist Name
/playplaylist Name
/deleteplaylist Name
/removefromplaylist Name song_position

━━━━━━━━━━━━━━━

❤️ Quick Save

Use the ➕ button on the player card.
"""
            )

            await callback.answer()

            return
        
        if data == "features":

            await callback.message.reply_text(
                """
⚡ Mizuki Features

🎵 High Quality Audio
📂 Smart Playlists
❤️ One-Tap Save
⬇️ Instant Downloads
🔗 YouTube URL Support
🤖 Auto Assistant Join
🎛 Volume Controls
📜 Smart Queue System
🌐 Multi Group Support

━━━━━━━━━━━━━━━

Many More features coming soon...
"""
            )

            await callback.answer()

            return

    except Exception as e:

        print(
            f"Callback Error: {e}"
        )

        await callback.answer(
            "❌ Error"
        )
    