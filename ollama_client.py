from ollama import chat

def get_ollama_response(user_query, retrieved_data):
    """Pass user input and retrieved RAG data to Ollama and return response."""
    try:
        context = "\n".join(retrieved_data)
        response = chat(model="llama3.2", messages=[
            {"role": "system", "content": "You are an AI nutrition assistant."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {user_query}"}
        ])
        return response.get("message", {}).get("content", "⚠️ No response from AI.")
    except Exception as e:
        return f"⚠️ AI system error: {str(e)}"
