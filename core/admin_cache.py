from time import time

admin_cache = {}

CACHE_TIME = 300  # 5 minutes


def get_cached_admins(chat_id):

    data = admin_cache.get(chat_id)

    if not data:
        return None

    admins, timestamp = data

    if time() - timestamp > CACHE_TIME:

        admin_cache.pop(
            chat_id,
            None
        )

        return None

    return admins


def set_cached_admins(
    chat_id,
    admins
):

    admin_cache[chat_id] = (
        admins,
        time()
    )