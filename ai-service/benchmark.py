import time
import statistics
import requests

BASE_URL = "http://127.0.0.1:8000"

times = []

print("Testing /health endpoint...")

for _ in range(50):

    start = time.time()

    requests.get(f"{BASE_URL}/health")

    duration = (time.time() - start) * 1000

    times.append(duration)


times.sort()

p50 = round(times[25], 2)
p95 = round(times[47], 2)
p99 = round(times[49], 2)

print(f"p50 = {p50} ms")
print(f"p95 = {p95} ms")
print(f"p99 = {p99} ms")
print(f"average = {round(statistics.mean(times), 2)} ms")