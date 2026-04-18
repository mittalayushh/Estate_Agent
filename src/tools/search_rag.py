from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool

# Initialize Embeddings once
persist_dir = 'data/vector_store'
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load existing database
db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

@tool
def market_researcher(query: str):
    """
    Searches the Real Estate market database (Knight Frank, JLL, RERA) for 
    trends, interest rates, and legal regulations in India. 
    Use this to justify property valuations or investment advice.
    """
    docs = db.similarity_search(query, k=3)
    context = "\n---\n".join([doc.page_content for doc in docs])
    return context