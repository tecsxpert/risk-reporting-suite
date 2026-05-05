import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/describe/"

@pytest.mark.parametrize("input_text", [
    "Liquidity risk in forex trading",
    "Credit risk in lending",
    "Gold price volatility due to Fed policy",
    "Operational risk from system outages",
    "Cybersecurity threats in online trading"
])
def test_describe_endpoint(input_text):
    response = requests.post(BASE_URL, json={"text": input_text})
    assert response.status_code == 200
    data = response.json()
    description = data.get("description", "")
    # ✅ Check both Risk and Impact are present
    assert "Risk:" in description
    assert "Impact:" in description
