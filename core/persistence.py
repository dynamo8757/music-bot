import json
import os

QUEUE_FILE = "queue_data.json"


def save_queue(data):

    try:

        with open(
            QUEUE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False
            )

    except Exception as e:

        print(
            f"Save Queue Error: {e}"
        )


def load_queue():

    try:

        if not os.path.exists(
            QUEUE_FILE
        ):
            return {}

        with open(
            QUEUE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception as e:

        print(
            f"Load Queue Error: {e}"
        )

        return {}