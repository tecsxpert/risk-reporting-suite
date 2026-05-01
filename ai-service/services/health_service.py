import time
from collections import deque
from chromadb import PersistentClient

# -----------------------------
# System start time
# -----------------------------
START_TIME = time.time()

# -----------------------------
# Response time tracking (last 10)
# -----------------------------
response_times = deque(maxlen=10)

# -----------------------------
# Cache stats
# -----------------------------
cache_stats = {
    "hits": 0,
    "misses": 0
}

# -----------------------------
# Model name
# -----------------------------
MODEL_NAME = "llama3-8b-8192"

# -----------------------------
# ChromaDB setup
# -----------------------------
client = PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documents")


# -----------------------------
# Metrics helpers
# -----------------------------
def add_response_time(response_time):
    response_times.append(response_time)


def get_average_response_time():
    if not response_times:
        return 0
    return round(sum(response_times) / len(response_times), 2)


def get_uptime():
    return int(time.time() - START_TIME)


def get_chromadb_doc_count():
    return collection.count()


# -----------------------------
# Cache tracking functions
# -----------------------------
def cache_hit():
    cache_stats["hits"] += 1


def cache_miss():
    cache_stats["misses"] += 1


# -----------------------------
# Final health output
# -----------------------------
def get_health_data():
    return {
        "model_name": MODEL_NAME,
        "avg_response_time_ms": get_average_response_time(),
        "chromadb_doc_count": get_chromadb_doc_count(),
        "uptime_seconds": get_uptime(),
        "cache_stats": cache_stats
    }