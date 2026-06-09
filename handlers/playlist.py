from pyrogram import filters

from core.client import app
from core.playlist_manager import (
    create_playlist,
    get_playlists,
    delete_playlist,
    add_song_to_playlist,
    get_playlist_songs,
    get_playlist_song_data,
    remove_song_from_playlist

)

from core.checks import (
    is_assistant_in_chat,
    get_assistant_username,
    is_voice_chat_active
)

from core.ui import (
    assistant_missing_text,
    VOICE_CHAT_MISSING
)

from core.player_state import (
    current_songs
)
from core.youtube import search_song

from core.queue import (
    add_to_queue
)

from core.vc_player import (
    play_song,
    is_playing
)

@app.on_message(filters.command("createplaylist"))
async def create_playlist_handler(client, message):

    try:

        if len(message.command) < 2:
            return await message.reply(
                "Usage:\n/createplaylist PlaylistName"
            )

        playlist_name = " ".join(
            message.command[1:]
        ).strip()

        created = create_playlist(
            message.from_user.id,
            playlist_name
        )

        if created:

            await message.reply(
                f"✅ Playlist '{playlist_name}' created."
            )

        else:

            await message.reply(
                "❌ Playlist already exists."
            )

    except Exception as e:

        print(
            f"[CREATE PLAYLIST ERROR] {e}"
        )

        try:
            await message.reply(
                "❌ Failed to create playlist."
            )
        except Exception:
            pass

@app.on_message(filters.command("playlists"))
async def playlists_handler(client, message):

    try:

        playlists = get_playlists(
            message.from_user.id
        )

        if not playlists:
            return await message.reply(
                "📂 You don't have any playlists."
            )

        text = "📂 Your Playlists\n\n"

        for index, playlist in enumerate(playlists, start=1):

            text += f"{index}. {playlist[1]}\n"

        await message.reply(text)

    except Exception as e:

        print(
            f"[PLAYLIST LIST ERROR] {e}"
        )

        await message.reply(
            "❌ Failed to fetch playlists."
        )

@app.on_message(filters.command("deleteplaylist"))
async def delete_playlist_handler(client, message):

    try:

        if len(message.command) < 2:
            return await message.reply(
                "Usage:\n/deleteplaylist PlaylistName"
            )

        playlist_name = " ".join(
            message.command[1:]
        ).strip()

        deleted = delete_playlist(
            message.from_user.id,
            playlist_name
        )

        if deleted:

            await message.reply(
                f"🗑 Playlist '{playlist_name}' deleted."
            )

        else:

            await message.reply(
                "❌ Playlist not found."
            )

    except Exception as e:

        print(
            f"[DELETE PLAYLIST ERROR] {e}"
        )

        try:
            await message.reply(
                "❌ Failed to delete playlist."
            )
        except Exception:
            pass

@app.on_message(filters.command("save"))
async def save_song_handler(client, message):

    try:

        if len(message.command) < 2:

            return await message.reply(
                "Usage:\n/save PlaylistName"
            )

        playlist_name = " ".join(
            message.command[1:]
        ).strip()

        assistant_ok = await is_assistant_in_chat(
            message.chat.id
        )

        if not assistant_ok:

            username = await get_assistant_username()

            return await message.reply_text(
                assistant_missing_text(
                    username
                )
            )

        voice_chat_ok = await is_voice_chat_active(
            message.chat.id
        )

        if not voice_chat_ok:

            return await message.reply_text(
                VOICE_CHAT_MISSING
            )

        chat_id = message.chat.id

        if chat_id not in current_songs:

            return await message.reply(
                "❌ No song is currently playing."
            )

        song = current_songs[
            chat_id
        ]["song"]

        saved = add_song_to_playlist(
            message.from_user.id,
            playlist_name,
            song
        )

        if saved:

            await message.reply(
                f"✅ Saved to '{playlist_name}'"
            )

        else:

            await message.reply(
                "❌ Playlist not found."
            )

    except Exception as e:

        print(
            f"[SAVE SONG ERROR] {e}"
        )

        try:

            await message.reply(
                "❌ Failed to save song."
            )

        except Exception:
            pass        

@app.on_message(filters.command("playlist"))
async def playlist_view_handler(client, message):

    try:

        if len(message.command) < 2:

            return await message.reply(
                "Usage:\n/playlist PlaylistName"
            )

        playlist_name = " ".join(
            message.command[1:]
        ).strip()

        songs = get_playlist_songs(
            message.from_user.id,
            playlist_name
        )

        if songs is None:

            return await message.reply(
                "❌ Playlist not found."
            )

        if not songs:

            return await message.reply(
                f"📂 {playlist_name}\n\nNo songs yet."
            )

        text = f"📂 {playlist_name}\n\n"

        for index, song in enumerate(
            songs,
            start=1
        ):

            text += (
                f"{index}. {song[0]}\n"
            )

        text += (
            f"\n🎵 Songs: {len(songs)}"
        )

        await message.reply(text)

    except Exception as e:

        print(
            f"[PLAYLIST VIEW ERROR] {e}"
        )

        try:

            await message.reply(
                "❌ Failed to load playlist."
            )

        except Exception:
            pass

@app.on_message(filters.command("playplaylist"))
async def play_playlist_handler(
    client,
    message
):

    try:

        if len(message.command) < 2:

            return await message.reply(
                "Usage:\n/playplaylist PlaylistName"
            )

        playlist_name = " ".join(
            message.command[1:]
        ).strip()

        songs = get_playlist_song_data(
            message.from_user.id,
            playlist_name
        )

        if songs is None:

            return await message.reply(
                "❌ Playlist not found."
            )

        if not songs:

            return await message.reply(
                "❌ Playlist is empty."
            )

        chat_id = message.chat.id

        first_song = songs[0]

        if not is_playing(chat_id):
            print(f"CHAT ID: {chat_id}")

            result = await play_song(
                chat_id,
                first_song[0],
                requested_by=message.from_user.first_name
            )

            print(first_song)
            print(result)

            songs = songs[1:]

        for song in songs:

            full_song = search_song(song[0])

            if not full_song:
                continue

            add_to_queue(
                chat_id,
                {
                    "query": song[0],
                    "song": full_song,
                    "chat_id": chat_id,
                    "requested_by": message.from_user.first_name
                }
            )

        await message.reply(
            f"▶ Playlist '{playlist_name}' loaded.\n"
            f"🎵 Songs: {len(songs)+1}"
        )

    except Exception as e:

        print(
            f"[PLAY PLAYLIST ERROR] {e}"
        )

        try:

            await message.reply(
                "❌ Failed to load playlist."
            )

        except Exception:
            pass        

@app.on_message(
    filters.command(
        "removefromplaylist"
    )
)
async def remove_song_handler(
    client,
    message
):

    try:

        if len(message.command) < 3:

            return await message.reply(
                "Usage:\n"
                "/removefromplaylist "
                "PlaylistName Position"
            )

        playlist_name = message.command[1]

        try:

            position = int(
                message.command[2]
            )

        except Exception:

            return await message.reply(
                "❌ Invalid position."
            )

        removed = remove_song_from_playlist(
            message.from_user.id,
            playlist_name,
            position
        )

        if removed is False:

            return await message.reply(
                "❌ Playlist not found."
            )

        if removed is None:

            return await message.reply(
                "❌ Invalid song number."
            )

        await message.reply(
            f"🗑 Removed:\n{removed}"
        )

    except Exception as e:

        print(
            f"[REMOVE SONG ERROR] {e}"
        )

        try:

            await message.reply(
                "❌ Failed to remove song."
            )

        except Exception:
            pass        