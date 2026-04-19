"""
Knowledge Base Builder — Ingests PDFs and Markdown files into ChromaDB.

Supports both PDF reports and curated markdown knowledge base files.
All paths are dynamically resolved — no hardcoded paths.
"""

import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Resolve paths relative to project root
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PDF_DIR = os.path.join(_PROJECT_ROOT, "data", "raw_reports")
_KB_DIR = os.path.join(_PROJECT_ROOT, "data", "knowledge_base")
_PERSIST_DIR = os.path.join(_PROJECT_ROOT, "data", "vector_store")


def build_real_estate_knowledge_base(force_rebuild: bool = False):
    """
    Builds or rebuilds the ChromaDB vector store from PDFs and markdown files.

    Args:
        force_rebuild: If True, rebuilds even if vector store exists
    """
    # Check if vector store already exists
    if not force_rebuild and os.path.exists(os.path.join(_PERSIST_DIR, "chroma.sqlite3")):
        print("✅ Vector store already exists. Use force_rebuild=True to rebuild.")
        return

    print("🚀 Initializing Market Intelligence Ingestion...")

    documents = []

    # ── Load PDFs ──
    if os.path.exists(_PDF_DIR):
        for file in os.listdir(_PDF_DIR):
            if file.endswith(".pdf"):
                filepath = os.path.join(_PDF_DIR, file)
                print(f"  📄 Loading PDF: {file}...")
                try:
                    loader = PyPDFLoader(filepath)
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"  ⚠️ Failed to load {file}: {e}")
    else:
        print(f"  ⚠️ PDF directory not found: {_PDF_DIR}")

    # ── Load Markdown Knowledge Base ──
    if os.path.exists(_KB_DIR):
        for file in os.listdir(_KB_DIR):
            if file.endswith(".md"):
                filepath = os.path.join(_KB_DIR, file)
                print(f"  📝 Loading Knowledge Base: {file}...")
                try:
                    loader = TextLoader(filepath, encoding='utf-8')
                    docs = loader.load()
                    # Add source metadata
                    for doc in docs:
                        doc.metadata['source'] = file
                        doc.metadata['type'] = 'knowledge_base'
                    documents.extend(docs)
                except Exception as e:
                    print(f"  ⚠️ Failed to load {file}: {e}")
    else:
        print(f"  ⚠️ Knowledge base directory not found: {_KB_DIR}")

    if not documents:
        print("❌ No documents found to ingest!")
        return

    print(f"\n📊 Total documents loaded: {len(documents)}")

    # ── Smart Chunking ──
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"📦 Split into {len(chunks)} searchable chunks")

    # ── Local Embeddings (No API Key Required) ──
    print("🧠 Generating embeddings (this may take a few minutes)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

    # ── Create and Persist Vector Store ──
    os.makedirs(_PERSIST_DIR, exist_ok=True)
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=_PERSIST_DIR
    )

    print(f"\n✅ Knowledge Base built successfully at {_PERSIST_DIR}")
    print(f"   Total chunks indexed: {len(chunks)}")


if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    build_real_estate_knowledge_base(force_rebuild=force)