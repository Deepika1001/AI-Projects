import requests

def get_order_status(order_id: int) -> str:
    url = f"http://localhost:8081/orders/{order_id}/status"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.text
    return f"Order {order_id} not found"