import re
import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
os.environ['HUGGING_FACE_API_KEY'] = 'Your_API_KEY'
# Function to trim numbers, spaces, and colons from start and end
def trim_start_end(input_string):
    return re.sub(r'^[0-9\s:.]+|[0-9\s:.]+$', '', input_string)

def get_metadata(record: dict, metadata: dict):
    print(record,metadata)
    print(metadata)

data_file = r"C:\Users\HP\Documents\meal-planner-backend\processed_food_data1.jsonl"  # Update the path accordingly

with open(data_file, "r") as f:
    food_data = [json.loads(line) for line in f]  # Read each line as a JSON object

# Convert food data into LangChain Document format
docs = []
for item in food_data:
    food_name = item.get("food", "unknown")
    caloric_value = item.get("Caloric Value", "unknown")

    # Create text content using relevant fields
    content = f"Food: {food_name}\nCaloric Value: {caloric_value}\n"
    content += "\n".join([f"{key}: {value}" for key, value in item.items() if key not in ["Unnamed: 0.1", "Unnamed: 0"]])

    docs.append(Document(page_content=content, metadata={"food_name": food_name}))

# Split text into chunks for efficient retrieval
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

# Create and persist vector database
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    persist_directory="./vector-food-db"
)
vectorstore.persist()

print(f"Stored {len(splits)} document chunks in ChromaDB.")