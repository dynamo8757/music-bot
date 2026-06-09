from collections import defaultdict
import random

music_queue = defaultdict(list)


def add_to_queue(chat_id, song):

    music_queue[chat_id].append(song)

    # +1 because one song is already playing
    return len(
        music_queue[chat_id]
    ) + 1


def get_queue(chat_id):

    return music_queue.get(
        chat_id,
        []
    )


def get_next_song(chat_id):

    queue = music_queue.get(
        chat_id,
        []
    )

    if not queue:
        return None

    return queue.pop(0)


def clear_queue(chat_id):

    if chat_id in music_queue:

        music_queue[chat_id].clear()


def queue_length(chat_id):

    return len(
        music_queue.get(
            chat_id,
            []
        )
    )


def has_queue(chat_id):

    return queue_length(
        chat_id
    ) > 0

def remove_from_queue(
    chat_id,
    position
):

    queue = music_queue.get(
        chat_id,
        []
    )

    if (
        position < 1
        or
        position > len(queue)
    ):
        return None

    return queue.pop(
        position - 1
    )

def get_queue_song(
    chat_id,
    position
):

    queue = music_queue.get(
        chat_id,
        []
    )

    if (
        position < 1
        or
        position > len(queue)
    ):
        return None

    return queue[
        position - 1
    ]

def add_front_queue(
    chat_id,
    song
):

    music_queue[chat_id].insert(
        0,
        song
    )


def shuffle_queue(
    chat_id
):

    queue = music_queue.get(
        chat_id,
        []
    )

    if len(queue) < 2:
        return False

    random.shuffle(queue)

    return True