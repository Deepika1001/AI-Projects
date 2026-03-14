from rag_service import ask_rag, debug_retrieval

if __name__ == "__main__":
    question = "What is the return policy?"

    print("\nRetrieved chunks:\n")
    chunks = debug_retrieval(question, top_k=3)
    for c in chunks:
        print("Chunk ID:", c.get("chunk_id"))
        print("Title:", c.get("title"))
        print("Category:", c.get("category"))
        print("Text:", c.get("text"))
        print("-" * 40)

    print("\nGemini answer:\n")
    answer = ask_rag(question, top_k=3)
    print(answer)