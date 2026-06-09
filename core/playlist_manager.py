import sqlite3
from contextlib import closing

DB_PATH = "database/playlists.db"


def init_playlist_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS playlist_songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            video_id TEXT NOT NULL,
            duration INTEGER DEFAULT 0,
            thumbnail TEXT,
            webpage_url TEXT,
            query TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()


def create_playlist(user_id: int, name: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM playlists WHERE user_id=? AND name=?",
            (user_id, name)
        )

        if cursor.fetchone():
            return False

        cursor.execute(
            "INSERT INTO playlists (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )

        conn.commit()
        return True


def get_playlists(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name
            FROM playlists
            WHERE user_id=?
            ORDER BY name
            """,
            (user_id,)
        )

        return cursor.fetchall()


def delete_playlist(user_id: int, name: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM playlists
            WHERE user_id=? AND name=?
            """,
            (user_id, name)
        )

        playlist = cursor.fetchone()

        if not playlist:
            return False

        playlist_id = playlist[0]

        cursor.execute(
            "DELETE FROM playlist_songs WHERE playlist_id=?",
            (playlist_id,)
        )

        cursor.execute(
            """
            DELETE FROM playlists
            WHERE id=?
            """,
            (playlist_id,)
        )

        conn.commit()
        return True
    
liked_songs = {}


def add_liked_song(user_id, song):

    user_id = str(user_id)

    if user_id not in liked_songs:
        liked_songs[user_id] = []

    if song not in liked_songs[user_id]:
        liked_songs[user_id].append(song)
        return True

    return False


def get_liked_songs(user_id):

    user_id = str(user_id)

    return liked_songs.get(user_id, [])


def remove_liked_song(user_id, song):

    user_id = str(user_id)

    if user_id not in liked_songs:
        return False

    if song in liked_songs[user_id]:
        liked_songs[user_id].remove(song)
        return True

    return False    

def add_song_to_playlist(
    user_id,
    playlist_name,
    song
):

    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM playlists
            WHERE user_id=? AND name=?
            """,
            (user_id, playlist_name)
        )

        playlist = cursor.fetchone()

        if not playlist:
            return False

        playlist_id = playlist[0]

        cursor.execute(
            """
            INSERT INTO playlist_songs (
                playlist_id,
                title,
                video_id,
                duration,
                thumbnail,
                webpage_url,
                query
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                playlist_id,
                song.get("title", "Unknown"),
                song.get("video_id", ""),
                song.get("duration", 0),
                song.get("thumbnail", ""),
                song.get("webpage_url", ""),
                song.get("webpage_url", "")
            )
        )

        conn.commit()

        return True
    

def get_playlist_songs(
    user_id,
    playlist_name
):

    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM playlists
            WHERE user_id=? AND name=?
            """,
            (user_id, playlist_name)
        )

        playlist = cursor.fetchone()

        if not playlist:
            return None

        playlist_id = playlist[0]

        cursor.execute(
            """
            SELECT title
            FROM playlist_songs
            WHERE playlist_id=?
            ORDER BY id
            """,
            (playlist_id,)
        )

        return cursor.fetchall()    
    
def get_playlist_song_data(
    user_id,
    playlist_name
):

    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM playlists
            WHERE user_id=? AND name=?
            """,
            (user_id, playlist_name)
        )

        playlist = cursor.fetchone()

        if not playlist:
            return None

        playlist_id = playlist[0]

        cursor.execute(
            """
            SELECT
                title,
                video_id,
                duration,
                thumbnail,
                webpage_url,
                query
            FROM playlist_songs
            WHERE playlist_id=?
            ORDER BY id
            """,
            (playlist_id,)
        )

        return cursor.fetchall()
    
def remove_song_from_playlist(
    user_id,
    playlist_name,
    position
):

    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM playlists
            WHERE user_id=? AND name=?
            """,
            (user_id, playlist_name)
        )

        playlist = cursor.fetchone()

        if not playlist:
            return False

        playlist_id = playlist[0]

        cursor.execute(
            """
            SELECT id, title
            FROM playlist_songs
            WHERE playlist_id=?
            ORDER BY id
            """,
            (playlist_id,)
        )

        songs = cursor.fetchall()

        if (
            position < 1
            or
            position > len(songs)
        ):
            return None

        song_id = songs[
            position - 1
        ][0]

        title = songs[
            position - 1
        ][1]

        cursor.execute(
            """
            DELETE FROM playlist_songs
            WHERE id=?
            """,
            (song_id,)
        )

        conn.commit()

        return title    