import requests
import json

def get_coupon(code: str) -> str:
    url = f"http://localhost:8083/coupons/{code}"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return json.dumps(response.json())
    return f"Coupon {code} not found"