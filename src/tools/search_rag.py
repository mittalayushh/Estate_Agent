"""
RAG Search Tool — ChromaDB Market Intelligence Retriever.

Lazy-loads the vector store to prevent segfaults on import.
All paths are dynamically resolved.
"""

import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool


# Resolve paths relative to project root
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PERSIST_DIR = os.path.join(_PROJECT_ROOT, "data", "vector_store")

# Lazy-loaded singleton
_db = None


def _get_db():
    """Lazy-loads the ChromaDB vector store only when first called."""
    global _db
    if _db is None:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        _db = Chroma(
            persist_directory=_PERSIST_DIR,
            embedding_function=embeddings
        )
    return _db


@tool
def market_researcher(query: str) -> str:
    """
    Searches the Real Estate market database (Knight Frank, JLL, RERA) for
    trends, interest rates, regulations, and investment insights in India.
    Use this to find market data for specific cities or legal guidelines.
    Returns relevant document excerpts with source attribution.
    """
    db = _get_db()
    docs = db.similarity_search(query, k=5)

    # Add source metadata to each chunk
    context_parts = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get('source', 'Unknown')
        # Extract just the filename from the full path
        source_name = os.path.basename(source) if source != 'Unknown' else source
        context_parts.append(f"[Source: {source_name}]\n{doc.page_content}")

    return "\n---\n".join(context_parts)


@tool
def rera_researcher(query: str) -> str:
    """
    Specifically searches for RERA (Real Estate Regulation and Development Act)
    guidelines, legal requirements, and compliance rules.
    Use this when the analysis needs legal/regulatory context.
    """
    db = _get_db()
    # Augment query with RERA-specific terms
    augmented_query = f"RERA regulation compliance legal {query}"
    docs = db.similarity_search(augmented_query, k=3)

    context_parts = []
    for doc in docs:
        source = doc.metadata.get('source', 'Unknown')
        source_name = os.path.basename(source) if source != 'Unknown' else source
        context_parts.append(f"[Source: {source_name}]\n{doc.page_content}")

    return "\n---\n".join(context_parts)