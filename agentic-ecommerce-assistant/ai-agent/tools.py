import re

import requests


ORDER_SERVICE_BASE_URL = "http://localhost:8081"
COUPON_SERVICE_BASE_URL = "http://localhost:8083"
USER_SERVICE_BASE_URL = "http://localhost:8082"


def is_rag_question(user_query: str) -> bool:
    """
    Determine whether the query should be answered using RAG.

    Args:
        user_query (str): The user's question.

    Returns:
        bool: True if query is informational (RAG), False if it requires backend action.
    """

    rag_keywords = [
        "how", "what", "guide", "help", "policy",
        "return policy", "payment methods",
        "how to use", "platform", "faq"
    ]

    query = user_query.lower()

    for keyword in rag_keywords:
        if keyword in query:
            return True

    return False

def ask_rag(user_query: str) -> str:
    """
    Query the knowledge base using RAG.

    Args:
        user_query (str): User question.

    Returns:
        str: Response generated from retrieved documents.
    """

    # Simulated knowledge base answers
    knowledge_base = {
        "return policy": "You can return items within 30 days of purchase.",
        "payment methods": "We support credit card, debit card, and UPI.",
        "how to track order": "You can track orders from the 'My Orders' section."
    }

    query = user_query.lower()

    for key in knowledge_base:
        if key in query:
            return knowledge_base[key]

    return "I couldn't find an answer in the knowledge base."


def call_tool(user_query: str) -> str:
    """
    Route the user request to backend tools/APIs.

    Args:
        user_query (str): The user's request.

    Returns:
        str: Tool execution result.
    """

    query = user_query.lower()
    order_id_match = re.search(r"\border\s+(\d+)\b", query)
    user_id_match = re.search(r"\buser\s+(\d+)\b", query)
    coupon_code_match = re.search(r"\bcoupon\s+([a-zA-Z0-9_-]+)\b", user_query)

    if order_id_match and any(
        phrase in query
        for phrase in ["where is my order", "order status", "track order", "status of order"]
    ):
        order_id = order_id_match.group(1)
        response = requests.get(
            f"{ORDER_SERVICE_BASE_URL}/orders/{order_id}/status",
            timeout=10,
        )
        if response.status_code == 200:
            return f"Order {order_id} status: {response.text}"
        return f"Order {order_id} not found."

    elif order_id_match and any(
        phrase in query
        for phrase in ["order details", "show order", "get order", "order info"]
    ):
        order_id = order_id_match.group(1)
        response = requests.get(
            f"{ORDER_SERVICE_BASE_URL}/orders/{order_id}",
            timeout=10,
        )
        if response.status_code == 200:
            return response.text
        return f"Order {order_id} not found."

    elif coupon_code_match:
        coupon_code = coupon_code_match.group(1)
        response = requests.get(
            f"{COUPON_SERVICE_BASE_URL}/coupons/{coupon_code}",
            timeout=10,
        )
        if response.status_code == 200:
            return response.text
        return f"Coupon {coupon_code} not found."

    elif "register user" in query:
        return "User successfully registered."

    elif "update order" in query:
        return "Order updated successfully."

    elif user_id_match and any(
        phrase in query
        for phrase in ["user details", "show user", "get user", "user info"]
    ):
        user_id = user_id_match.group(1)
        response = requests.get(
            f"{USER_SERVICE_BASE_URL}/users/{user_id}",
            timeout=10,
        )
        if response.status_code == 200:
            return response.text
        return f"User {user_id} not found."

    return "Sorry, I couldn't understand the request."
