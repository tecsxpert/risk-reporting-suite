import requests, json

queries = ["gold price volatility", "system outage risk", "cybersecurity threats in trading"]

for q in queries:
    print(f"Testing query: {q}")
    response = requests.post(
        "http://127.0.0.1:5000/generate-report/",
        json={"query": q}
    )
    print(json.dumps(response.json(), indent=2))
    print("\n")
