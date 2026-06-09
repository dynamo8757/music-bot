
from collections import OrderedDict

MAX_CACHE_SIZE = 1000

audio_cache = OrderedDict()
search_cache = OrderedDict()


def cache_set(cache, key, value):
    cache[key] = value

    if len(cache) > MAX_CACHE_SIZE:
        cache.popitem(last=False)