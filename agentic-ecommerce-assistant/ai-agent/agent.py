from rag_service import ask_rag
from tools import call_tool

def ask_agent(user_query):
    """Route the user query to RAG retrieval or task tooling.

    Args:
        user_query (str): The customer inquiry text.

    Returns:
        str: The assistant answer from RAG or tool output.
    """

    if is_rag_question(user_query):
        return ask_rag(user_query)

    return call_tool(user_query)