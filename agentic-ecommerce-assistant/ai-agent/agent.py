from tools import ask_rag as ask_rag_local
from tools import call_tool, is_rag_question

def ask_agent(user_query):
    """Route the user query to RAG retrieval or task tooling.

    Args:
        user_query (str): The customer inquiry text.

    Returns:
        str: The assistant answer from RAG or tool output.
    """

    if is_rag_question(user_query):
        try:
            # Import lazily so the chat UI can still run if cloud RAG is not configured.
            from rag_service import ask_rag as ask_rag_cloud

            return ask_rag_cloud(user_query)
        except Exception:
            return ask_rag_local(user_query)

    return call_tool(user_query)
