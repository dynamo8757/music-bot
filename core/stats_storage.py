import json
import os

STATS_FILE = "stats.json"


def load_stats():

    if not os.path.exists(
        STATS_FILE
    ):
        return {
            "songs_played": 0,
            "searches": 0,
            "cache_hits": 0
        }

    try:

        with open(
            STATS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {
            "songs_played": 0,
            "searches": 0,
            "cache_hits": 0
        }


def save_stats(stats):

    try:

        with open(
            STATS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                stats,
                f,
                indent=4
            )

    except Exception as e:

        print(
            f"Stats Save Error: {e}"
        )