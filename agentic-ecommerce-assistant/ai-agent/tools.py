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

    if "order status" in query:
        return "Order #12345 is currently shipped."

    elif "order details" in query:
        return "Order #12345 contains 2 items and was placed on March 10."

    elif "coupon" in query:
        return "Coupon SAVE10 gives 10% discount on orders above $50."

    elif "register user" in query:
        return "User successfully registered."

    elif "update order" in query:
        return "Order updated successfully."

    return "Sorry, I couldn't understand the request."