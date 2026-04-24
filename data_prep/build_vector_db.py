import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

def build_db():
    print("Initializing ChromaDB Cloud for RAG...")
    
    # Initialize Cloud ChromaDB
    chroma_client = chromadb.HttpClient(
        host="api.trychroma.com",
        ssl=True,
        tenant="60c0eb23-c9fc-4c46-bc8c-6805273c5af5",
        database="College_admission_db",
        headers={
            "x-chroma-token": os.getenv("CHROMA_TOKEN")        
        }
    )
    
    # Use default embedding function (all-MiniLM-L6-v2)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = chroma_client.get_or_create_collection(
        name="college_admission_data",
        embedding_function=sentence_transformer_ef
    )
    
    # Read data from Excel file
    # Ensure you have installed required libraries: pip install pandas openpyxl
    try:
        import pandas as pd
    except ImportError:
        print("Error: pandas is not installed. Please run: pip install pandas openpyxl")
        return

    excel_file_path = r"C:\Users\RAbishek\.gemini\antigravity\scratch\college_admission_assistant\college_dataset_350.csv"
    
    if not os.path.exists(excel_file_path):
        print(f"Error: Could not find Excel file at {excel_file_path}")
        print("Please place your Excel file (admission_data.xlsx) there or update the path.")
        return

    print(f"Reading data from {excel_file_path}...")
    df = pd.read_csv(excel_file_path)
    
    # Customize this based on your Excel file's structure.
    # Option 1: If you have a specific column with the text (e.g., 'Content'):
    # documents = df['Content'].dropna().astype(str).tolist()
    
    # Option 2: Combine all columns in each row into a single string document
    documents = df.astype(str).agg(' | '.join, axis=1).tolist()
    
    if not documents:
        print("Warning: No data found in the Excel file.")
        return

    ids = [f"doc_{i}" for i in range(len(documents))]
    
    # Upsert to avoid duplicates if run multiple times
    collection.upsert(
        documents=documents,
        ids=ids
    )
    
    print(f"Added {len(documents)} documents to the vector database successfully!")
    print(f"Vector DB is ready in: {db_path}")

if __name__ == "__main__":
    build_db()
