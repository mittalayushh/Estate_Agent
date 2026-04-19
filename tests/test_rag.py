"""
Test Suite: RAG Retrieval — Market research, RERA, and knowledge base.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.search_rag import market_researcher, rera_researcher


def test_vector_store_exists():
    """Test that the ChromaDB vector store is built."""
    print("🧪 Test 1: Vector Store Existence")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vs_path = os.path.join(project_root, "data", "vector_store", "chroma.sqlite3")
    assert os.path.exists(vs_path), f"Vector store not found: {vs_path}"
    size_mb = os.path.getsize(vs_path) / (1024 * 1024)
    print(f"   ✅ ChromaDB exists ({size_mb:.1f} MB)")


def test_market_research_retrieval():
    """Test that market research returns relevant content."""
    print("\n🧪 Test 2: Market Research Retrieval")
    query = "Real estate market trends for Mumbai 2024"
    result = market_researcher.run(query)

    assert isinstance(result, str), f"Expected string, got {type(result)}"
    assert len(result) > 100, f"Result too short ({len(result)} chars)"
    print(f"   ✅ Retrieved {len(result)} chars for Mumbai market query")
    print(f"   Preview: {result[:150]}...")


def test_rera_retrieval():
    """Test RERA-specific retrieval."""
    print("\n🧪 Test 3: RERA Retrieval")
    query = "RERA project registration requirements"
    result = rera_researcher.run(query)

    assert isinstance(result, str), f"Expected string, got {type(result)}"
    assert len(result) > 50, f"Result too short ({len(result)} chars)"
    print(f"   ✅ Retrieved {len(result)} chars for RERA query")
    print(f"   Preview: {result[:150]}...")


def test_source_attribution():
    """Test that results include source file references."""
    print("\n🧪 Test 4: Source Attribution")
    result = market_researcher.run("Investment guidelines for real estate in India")
    assert "[Source:" in result, "Source attribution missing!"
    # Count sources
    source_count = result.count("[Source:")
    print(f"   ✅ Found {source_count} source citations in results")


def test_knowledge_base_files():
    """Test that knowledge base markdown files exist."""
    print("\n🧪 Test 5: Knowledge Base Files")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kb_dir = os.path.join(project_root, "data", "knowledge_base")

    expected_files = [
        "india_market_overview_2024.md",
        "rera_compliance_guide.md",
        "investment_guidelines.md"
    ]

    for f in expected_files:
        path = os.path.join(kb_dir, f)
        assert os.path.exists(path), f"Missing: {path}"
        size = os.path.getsize(path)
        print(f"   ✅ {f} ({size} bytes)")


def test_pdf_reports_exist():
    """Test that PDF reports exist in raw_reports."""
    print("\n🧪 Test 6: PDF Reports")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_dir = os.path.join(project_root, "data", "raw_reports")

    assert os.path.isdir(pdf_dir), f"PDF dir missing: {pdf_dir}"
    pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    assert len(pdfs) >= 3, f"Expected 3+ PDFs, found {len(pdfs)}"
    for pdf in pdfs:
        print(f"   ✅ {pdf}")


def test_city_specific_retrieval():
    """Test retrieval returns city-relevant data."""
    print("\n🧪 Test 7: City-Specific Relevance")
    cities = ["Bangalore", "Hyderabad", "Delhi"]

    for city in cities:
        result = market_researcher.run(f"Real estate market in {city}")
        assert len(result) > 50, f"No data for {city}"
        print(f"   ✅ {city}: {len(result)} chars retrieved")


if __name__ == "__main__":
    print("=" * 50)
    print("  RAG RETRIEVAL TEST SUITE")
    print("=" * 50)
    test_vector_store_exists()
    test_knowledge_base_files()
    test_pdf_reports_exist()
    test_market_research_retrieval()
    test_rera_retrieval()
    test_source_attribution()
    test_city_specific_retrieval()
    print("\n" + "=" * 50)
    print("  🎉 ALL RAG TESTS PASSED!")
    print("=" * 50)