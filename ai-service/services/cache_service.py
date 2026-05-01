import hashlib
import time

# -----------------------------------
# Simple in-memory cache
# -----------------------------------
cache_store = {}

# Cache TTL = 15 minutes
CACHE_TTL = 60 * 15

# Cache stats
cache_stats = {
    "hits": 0,
    "misses": 0
}


# -----------------------------------
# Create SHA256 cache key
# -----------------------------------
def create_cache_key(question: str):

    return hashlib.sha256(
        question.encode()
    ).hexdigest()


# -----------------------------------
# Get cache
# -----------------------------------
def get_cache(question: str):

    key = create_cache_key(question)

    cached = cache_store.get(key)

    if not cached:
        cache_stats["misses"] += 1
        return None

    # Check expiry
    if time.time() > cached["expiry"]:
        del cache_store[key]
        cache_stats["misses"] += 1
        return None

    cache_stats["hits"] += 1

    return cached["data"]


# -----------------------------------
# Set cache
# -----------------------------------
def set_cache(question: str, data):

    key = create_cache_key(question)

    cache_store[key] = {
        "data": data,
        "expiry": time.time() + CACHE_TTL
    }


# -----------------------------------
# Skip cache logic
# -----------------------------------
def should_skip_cache(question: str):

    return question.lower().startswith("no-cache:")