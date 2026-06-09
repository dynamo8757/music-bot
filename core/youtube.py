from yt_dlp import YoutubeDL

from core.player_state import stats

from core.cache import (
    audio_cache,
    search_cache,
    cache_set
)


SEARCH_OPTIONS = {
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "extractor_args": {
        "youtube": {
            "player_client": ["android"]
        }
    }
}


def search_song(query: str):
    if "youtube.com/watch" in query or "youtu.be/" in query:
        try:
            with YoutubeDL(SEARCH_OPTIONS) as ydl:
                video = ydl.extract_info(
                    query,
                    download=False
                )

                return {
                    "title": video.get(
                        "title",
                        "Unknown"
                    ),
                    "duration": video.get(
                        "duration",
                        0
                    ),
                    "thumbnail": video.get(
                        "thumbnail"
                    ),
                    "webpage_url": video.get(
                        "webpage_url"
                    ),
                    "video_id": video.get(
                        "id"
                    ),
                    "uploader": video.get(
                        "uploader",
                        "Unknown"
                    )
                }

        except Exception as e:
            print(
                f"URL Search Error: {e}"
            )

            return None

    cached = search_cache.get(query.lower())
    if cached:
        return cached

    try:
        stats["searches"] += 1
        with YoutubeDL(SEARCH_OPTIONS) as ydl:
            results = ydl.extract_info(
                f"ytsearch1:{query}",
                download=False
            )

            if not results:
                return None

            entries = results.get("entries", [])
            if not entries:
                return None

            video = entries[0]
            result = {
                "title": video.get("title", "Unknown"),
                "duration": video.get("duration", 0),
                "thumbnail": video.get("thumbnail"),
                "webpage_url": video.get("webpage_url"),
                "video_id": video.get("id"),
                "uploader": video.get("uploader", "Unknown")
            }
            # Cache and return the found result
            cache_set(search_cache, query.lower(), result)
            return result

    except Exception as e:
        print(f"YouTube Search Error: {e}")
        return None


def get_audio_url(video_url: str):
    cached = audio_cache.get(video_url)

    if cached:
        stats["cache_hits"] += 1
        return cached

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"]
                }
            }
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                video_url,
                download=False
            )

            if not info:
                return None

            url = info.get("url")
            if url:
                cache_set(audio_cache, video_url, url)
                return url

            formats = info.get("formats", [])

            # Prefer audio-only formats
            for fmt in reversed(formats):
                if (
                    fmt.get("url")
                    and
                    fmt.get("vcodec") == "none"
                ):
                    cache_set(audio_cache,video_url,fmt["url"])
                    return fmt["url"]

            # Fallback
            for fmt in reversed(formats):
                if fmt.get("url"):
                    cache_set(audio_cache, video_url, fmt["url"])
                    return fmt["url"]

            return None

    except Exception as e:
        print(
            f"Audio URL Error: {e}"
        )

        return None


def format_duration(seconds):

    try:

        if not seconds:
            return "Unknown"

        minutes = seconds // 60
        seconds = seconds % 60

        return f"{minutes}:{seconds:02d}"

    except Exception:

        return "Unknown"
    
def get_related_query(song):

    try:

        title = song.get(
            "title",
            ""
        )

        artist = song.get(
            "uploader",
            ""
        )

        return f"{title} {artist}"

    except Exception:

        return None