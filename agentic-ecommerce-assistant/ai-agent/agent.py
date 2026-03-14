from rag_service import ask_rag
from tools import call_tool

def ask_agent(user_query):

    if is_rag_question(user_query):
        return ask_rag(user_query)

    return call_tool(user_query)