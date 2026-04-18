import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def build_real_estate_knowledge_base():
    # 1. Setup paths
    pdf_dir = 'data/raw_reports/' 
    persist_dir = 'data/vector_store'
    
    print("🚀 Initializing Market Intelligence Ingestion...")

    # 2. Load all PDFs
    if not os.path.exists(pdf_dir) or not os.listdir(pdf_dir):
        print(f"Error: Place your PDFs in {pdf_dir} first!")
        return

    documents = []
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            print(f"Loading {file}...")
            loader = PyPDFLoader(os.path.join(pdf_dir, file))
            documents.extend(loader.load())

    # 3. Smart Chunking (Optimized for Legal/Technical Text)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split data into {len(chunks)} searchable chunks.")

    # 4. Local Embeddings (No API Key Required)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 5. Create and Persist Vector Store
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    
    print(f"SUCCESS: Knowledge Base built at {persist_dir}")

if __name__ == "__main__":
    build_real_estate_knowledge_base()