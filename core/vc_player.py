from pytgcalls import PyTgCalls
from pytgcalls.types.stream import StreamEnded
from pytgcalls.types import MediaStream
import asyncio
import time

from core.client import (
    assistant,
    app
)

from core.youtube import (
    search_song,
    get_audio_url
)

from core.queue import (
    add_to_queue,
    get_next_song,
    has_queue,
    clear_queue,
    add_front_queue,
    shuffle_queue
)

from core.player_state import (
    song_start_times,
    paused_duration,
    paused_at
)

from core.player_state import (
    queue_messages,
    current_songs,
    playback_status,
    volume_levels,
    autoplay_modes,
    play_modes,
    stats,
    player_messages
)

from core.player_card import (
    send_or_update_player_card
)

pytgcalls = PyTgCalls(assistant)

active_chats = {}


@pytgcalls.on_update()
async def stream_end_handler(_, update):

    try:

        if not isinstance(update, StreamEnded):
            return

        chat_id = update.chat_id
        print(
            f"Mode: {play_modes.get(chat_id, 'queue')}"
        )
        mode = play_modes.get(chat_id, "queue")

        print(
            f"🎵 Stream Ended: {chat_id}"
        )
        if mode == "repeat" and chat_id in current_songs:
            add_front_queue(chat_id, current_songs[chat_id])

        if not has_queue(chat_id):

            print(
                f"📴 Queue Empty: {chat_id}"
            )

            if chat_id in active_chats:
                del active_chats[chat_id]

            current_songs.pop(
                chat_id,
                None
            )

            try:
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

                await pytgcalls.leave_call(
                    chat_id
                )
            except Exception:
                pass

            return
        
        if mode == "shuffle":
            shuffle_queue(chat_id)

        next_song = get_next_song(
            chat_id
        )
        if not next_song:
            print(
                f"❌ next_song is None | {chat_id}"
            )
            return

        try:

            if (
                chat_id in queue_messages
                and
                next_song["song"]["title"]
                in queue_messages[chat_id]
            ):

                msg_id = queue_messages[
                    chat_id
                ].pop(
                    next_song["song"]["title"]
                )

                await app.delete_messages(
                    chat_id,
                    msg_id
                )
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                print(
                    f"Now Playing Card Error: {e}"
                )

        audio_url = await asyncio.to_thread(
            get_audio_url,
            next_song["song"]["webpage_url"]
        )

        if not audio_url:
            print(
                "❌ Failed To Get Audio URL"
            )
            return

        from core.recovery import safe_execute

        result = await safe_execute(
            pytgcalls.play(
                chat_id,
                MediaStream(
                    audio_url,
                    audio_flags=MediaStream.Flags.REQUIRED,
                    video_flags=MediaStream.Flags.IGNORE
                )
            ),
            "Stream Switch"
        )

        if not result:

            print(
                "❌ Stream switch failed"
            )

            return

        current_songs[chat_id] = next_song
        playback_status[chat_id] = "playing"
        song_start_times[chat_id] = time.time()

        paused_duration[chat_id] = 0
        paused_at.pop(
            chat_id,
            None
        )

        print(
            f"▶ Playing Next: {next_song['song']['title']}"
        )

        try:
            await send_or_update_player_card(
                chat_id=chat_id,
                song=next_song["song"],
                requested_by=next_song.get(
                    "requested_by",
                    "Unknown"
                )
            )
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                print(
                    f"Now Playing Card Error: {e}"
                )
    except Exception as e:
        print(f"Stream End Handler Error: {e}")
        return


async def start_pytgcalls():

    try:

        await pytgcalls.start()

        print(
            "✅ PyTgCalls Started"
        )

        return True

    except Exception as e:

        print(
            f"❌ PyTgCalls Error: {e}"
        )

        return False


async def play_song(
    chat_id,
    query,
    requested_by="Unknown"
):

    try:

        import asyncio

        song = await asyncio.to_thread(
            search_song,
            query
        )

        if not song:

            return {
                "success": False,
                "message": "Song not found."
            }

        audio_url = await asyncio.to_thread(
            get_audio_url,
            song["webpage_url"]
        )

        if not audio_url:

            return {
                "success": False,
                "message": "Failed to fetch audio."
            }

        if chat_id in active_chats:

            position = add_to_queue(
                chat_id,
                {
                    "query": query,
                    "song": song,
                    "chat_id": chat_id,
                    "requested_by": requested_by
                }
            )

            return {
                "success": True,
                "queued": True,
                "position": position,
                "song": song
            }

        from core.recovery import safe_execute

        result = await safe_execute(
            pytgcalls.play(
                chat_id,
                MediaStream(
                    audio_url,
                    audio_flags=MediaStream.Flags.REQUIRED,
                    video_flags=MediaStream.Flags.IGNORE
                )
            ),
            "Stream Switch"
        )

        if not result:

            return {
                "success": False,
                "message": "Playback failed."
            }

        current_songs[chat_id] = {
            "query": query,
            "song": song,
            "requested_by": requested_by
        }
        song_start_times[chat_id] = time.time()
        playback_status[chat_id] = "playing"

        autoplay_modes.setdefault(
            chat_id,
            True
        )

        play_modes.setdefault(
            chat_id,
            "queue"
        )

        volume_levels.setdefault(
            chat_id,
            100
        )

        active_chats[chat_id] = True
        stats["songs_played"] += 1

        return {
            "success": True,
            "queued": False,
            "song": song
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


async def pause_music(chat_id):

    try:

        await pytgcalls.pause(
            chat_id
        )

        playback_status[chat_id] = "paused"

        return True

    except Exception as e:

        print(
            f"Pause Error: {e}"
        )

        return False


async def resume_music(chat_id):

    try:

        await pytgcalls.resume(
            chat_id
        )
        playback_status[chat_id] = "playing"

        return True

    except Exception as e:

        print(
            f"Resume Error: {e}"
        )

        return False


async def stop_music(chat_id):

    try:
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

        await pytgcalls.leave_call(
            chat_id
        )

    except Exception as e:

        print(
            f"Stop Error: {e}"
        )

    finally:

        if chat_id in active_chats:
            del active_chats[chat_id]

        current_songs.pop(
            chat_id,
            None
        )

        playback_status.pop(
            chat_id,
            None
        )

        clear_queue(chat_id)
        volume_levels.pop(
            chat_id,
            None
        )

        autoplay_modes.pop(
            chat_id,
            None
        )

        play_modes.pop(
            chat_id,
            None
        )

        queue_messages.pop(
            chat_id,
            None
        )

        song_start_times.pop(
            chat_id,
            None
        )

        paused_duration.pop(
            chat_id,
            None
        )

        paused_at.pop(
            chat_id,
            None
        )


async def skip_music(chat_id):

    try:

        mode = play_modes.get(
            chat_id,
            "queue"
        )

        # Repeat mode
        if (
            mode == "repeat"
            and
            chat_id in current_songs
        ):

            next_song = current_songs[
                chat_id
            ]

        else:

            if not has_queue(chat_id):

                await stop_music(
                    chat_id
                )

                return None

            if mode == "shuffle":
                shuffle_queue(
                    chat_id
                )

            next_song = get_next_song(
                chat_id
            )
            if not next_song:

                print(
                    f"❌ next_song is None | {chat_id}"
                )

                return None

        try:

            if (
                chat_id in queue_messages
                and
                next_song["song"]["title"]
                in queue_messages[chat_id]
            ):

                msg_id = queue_messages[
                    chat_id
                ].pop(
                    next_song["song"]["title"]
                )

                await app.delete_messages(
                    chat_id,
                    msg_id
                )

        except Exception as e:

            print(
                f"Queue Delete Error: {e}"
            )

        audio_url = await asyncio.to_thread(
            get_audio_url,
            next_song["song"]["webpage_url"]
        )
        if not audio_url:
            return None

        from core.recovery import safe_execute

        result = await safe_execute(
            pytgcalls.play(
                chat_id,
                MediaStream(
                    audio_url,
                    audio_flags=MediaStream.Flags.REQUIRED,
                    video_flags=MediaStream.Flags.IGNORE
                )
            ),
            "Stream Switch"
        )

        if not result:
            return {
                "success": False,
                "message": "Playback failed."
            }

        current_songs[chat_id] = next_song
        playback_status[chat_id] = "playing"
        song_start_times[chat_id] = time.time()

        paused_duration[chat_id] = 0

        paused_at.pop(
            chat_id,
            None
        )

        try:

            await send_or_update_player_card(
                chat_id=chat_id,
                song=next_song["song"],
                requested_by=next_song.get(
                    "requested_by",
                    "Unknown"
                )
            )

        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                print(
                    f"Now Playing Card Error: {e}"
                )

        return next_song

    except Exception as e:

        print(
            f"Skip Error: {e}"
        )

        return None


def is_playing(chat_id):

    return chat_id in active_chats