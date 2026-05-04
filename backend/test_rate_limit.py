import requests

url = "http://127.0.0.1:5000/analyze"
payload = {"input": "fraud transaction"}

for i in range(35):
    response = requests.post(url, json=payload)
    print(f"Request {i+1}: {response.status_code}")
    if response.status_code == 429:
        print("✅ Rate limit working!")
        break