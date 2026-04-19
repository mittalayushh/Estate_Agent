"""
Test Suite: Market Sentiment Analyzer.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tools.market_sentiment import analyze_market_sentiment

def test_bullish_sentiment():
    print("🧪 Test 1: Bullish Sentiment Detection")
    ctx = "Mumbai shows strong growth. Demand surging, rising appreciation. Metro infrastructure development. Robust recovery. Positive outlook."
    r = analyze_market_sentiment(ctx, "Mumbai")
    assert r['sentiment_score'] > 0
    assert r['sentiment_label'] in ["BULLISH", "MODERATELY POSITIVE"]
    print(f"   ✅ {r['sentiment_label']} (score: {r['sentiment_score']})")

def test_bearish_sentiment():
    print("\n🧪 Test 2: Bearish Sentiment Detection")
    ctx = "Market decline and correction. Oversupply causing stagnation. Sluggish falling demand. Uncertainty risk. Negative bearish."
    r = analyze_market_sentiment(ctx, "City")
    assert r['sentiment_score'] < 0
    assert r['sentiment_label'] in ["BEARISH", "MODERATELY NEGATIVE"]
    print(f"   ✅ {r['sentiment_label']} (score: {r['sentiment_score']})")

def test_infrastructure_detection():
    print("\n🧪 Test 3: Infrastructure Catalysts")
    r = analyze_market_sentiment("metro connectivity, new airport, highway access, SEZ development", "Bangalore")
    assert len(r['infrastructure_catalysts']) > 0
    print(f"   ✅ Found: {r['infrastructure_catalysts']}")

def test_output_structure():
    print("\n🧪 Test 4: Output Structure")
    r = analyze_market_sentiment("Some context.", "Mumbai")
    for f in ['sentiment_label','sentiment_score','positive_signals','negative_signals','outlook','data_quality']:
        assert f in r, f"Missing: {f}"
    print(f"   ✅ All fields present")

if __name__ == "__main__":
    print("=" * 50)
    print("  MARKET SENTIMENT TEST SUITE")
    print("=" * 50)
    test_bullish_sentiment()
    test_bearish_sentiment()
    test_infrastructure_detection()
    test_output_structure()
    print("\n  🎉 ALL SENTIMENT TESTS PASSED!")
