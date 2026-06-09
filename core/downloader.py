import os
import uuid

from yt_dlp import YoutubeDL


DOWNLOAD_DIR = "downloads"

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


def download_song(
    url
):

    filename = str(
        uuid.uuid4()
    )

    output = (
        f"{DOWNLOAD_DIR}/"
        f"{filename}.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output,
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],
        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        }
    }

    with YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            url,
            download=True
        )

        file_path = ydl.prepare_filename(
            info
        )
        base = os.path.splitext(
            file_path
        )[0]

        file_path = f"{base}.mp3"

        return (
            file_path,
            info.get(
                "title",
                "Unknown"
            )
        )