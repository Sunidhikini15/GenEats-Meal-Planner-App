# from langchain.chains import RetrievalQA
# from langchain_openai import ChatOpenAI
# from langchain_community.vectorstores import FAISS  # or Chroma
# from langchain.embeddings.openai import OpenAIEmbeddings

# # Load LLM
# llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, openai_api_key="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")

# # Example initialization
# embedding = OpenAIEmbeddings(openai_api_key="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")
# vectorstore = FAISS.load_local("faiss_index", embeddings=embedding)
# # Create RetrievalQA Chain
# qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# # Ask a question
# question = "What is the best cheese for a low-fat diet?"
# answer = qa_chain.run(question)

# print("🧠 AI Answer:", answer)
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load the stored vector database
vectorstore = Chroma(
    persist_directory="./vector-food-db",
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
)

def retrieve_food_info(query, top_k=5):
    """Retrieve top_k most relevant food items based on the query."""
    results = vectorstore.similarity_search(query, k=top_k)
    
    if not results:
        print("No relevant food data found.")
        return []
    
    for i, doc in enumerate(results, 1):
        print(f"Result {i}:")
        print(doc.page_content)
        print("-" * 40)
    
    return results

# Example query
query = "high protein foods"
retrieve_food_info(query)