import requests
import json

def get_user(user_id: int) -> str:
    url = f"http://localhost:8082/users/{user_id}"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return json.dumps(response.json())
    return f"User {user_id} not found"