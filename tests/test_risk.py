"""
Test Suite: Risk Simulator — Multi-factor risk assessment.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.risk_simulator import run_risk_simulation


def test_basic_risk_assessment():
    """Test risk assessment returns valid structure."""
    print("🧪 Test 1: Basic Risk Assessment")
    result = run_risk_simulation(
        predicted_price=85.0, city="Mumbai",
        property_type="Apartment", size_sqft=1500,
        market_context="Strong growth in Mumbai real estate. Demand is rising. Infrastructure development."
    )

    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    assert "risk_factors" in result
    assert "overall_risk_score" in result
    assert "overall_risk_level" in result
    assert "recommendation" in result
    assert "emi_scenarios" in result
    print(f"   ✅ Risk Level: {result['overall_risk_level']} (Score: {result['overall_risk_score']}/100)")
    print(f"   ✅ Recommendation: {result['recommendation']}")


def test_risk_factors_count():
    """Test all 4 risk factors are present."""
    print("\n🧪 Test 2: Risk Factors Count")
    result = run_risk_simulation(
        predicted_price=50.0, city="Pune",
        property_type="Villa", size_sqft=2500,
        market_context="Market is stable with moderate growth."
    )

    factors = result['risk_factors']
    assert len(factors) == 4, f"Expected 4 risk factors, got {len(factors)}"

    expected_names = ["Interest Rate Sensitivity", "Market Cycle Position", "Valuation Benchmark", "Liquidity Risk"]
    actual_names = [f['factor'] for f in factors]
    for name in expected_names:
        assert name in actual_names, f"Missing factor: {name}"
        print(f"   ✅ {name}: present")


def test_emi_scenarios():
    """Test EMI calculation at different interest rates."""
    print("\n🧪 Test 3: EMI Scenarios")
    result = run_risk_simulation(
        predicted_price=100.0, city="Delhi",
        property_type="Apartment", size_sqft=1800,
        market_context="Stable market conditions."
    )

    emi = result['emi_scenarios']
    assert "7.5%" in emi, "Missing 7.5% EMI scenario"
    assert "10.5%" in emi, "Missing 10.5% EMI scenario"
    assert emi["10.5%"] > emi["7.5%"], "Higher rate should have higher EMI"

    for rate, amount in emi.items():
        print(f"   ✅ {rate} → ₹{amount}K/month")


def test_bearish_market_higher_risk():
    """Test that bearish market context increases risk score."""
    print("\n🧪 Test 4: Market Sentiment Impact on Risk")
    bullish_result = run_risk_simulation(
        predicted_price=80.0, city="Hyderabad",
        property_type="Apartment", size_sqft=1500,
        market_context="Strong growth, rising demand, appreciation, boom, surge"
    )

    bearish_result = run_risk_simulation(
        predicted_price=80.0, city="Hyderabad",
        property_type="Apartment", size_sqft=1500,
        market_context="Decline, correction, slowdown, oversupply, stagnation"
    )

    print(f"   Bullish risk score: {bullish_result['overall_risk_score']}")
    print(f"   Bearish risk score: {bearish_result['overall_risk_score']}")
    assert bearish_result['overall_risk_score'] >= bullish_result['overall_risk_score'], \
        "Bearish market should have higher risk"
    print(f"   ✅ Bearish market correctly scores higher risk")


def test_villa_higher_liquidity_risk():
    """Test that villas have higher liquidity risk than apartments."""
    print("\n🧪 Test 5: Liquidity Risk by Property Type")
    apt_result = run_risk_simulation(
        predicted_price=80.0, city="Pune",
        property_type="Apartment", size_sqft=1500,
        market_context="Stable market."
    )
    villa_result = run_risk_simulation(
        predicted_price=80.0, city="Pune",
        property_type="Villa", size_sqft=1500,
        market_context="Stable market."
    )

    apt_liq = next(f for f in apt_result['risk_factors'] if f['factor'] == "Liquidity Risk")
    villa_liq = next(f for f in villa_result['risk_factors'] if f['factor'] == "Liquidity Risk")

    print(f"   Apartment liquidity: {apt_liq['severity']}")
    print(f"   Villa liquidity: {villa_liq['severity']}")
    assert apt_liq['severity'] == "LOW", "Apartments should have LOW liquidity risk"
    assert villa_liq['severity'] == "MEDIUM", "Villas should have MEDIUM liquidity risk"
    print(f"   ✅ Liquidity risk correctly varies by property type")


if __name__ == "__main__":
    print("=" * 50)
    print("  RISK SIMULATOR TEST SUITE")
    print("=" * 50)
    test_basic_risk_assessment()
    test_risk_factors_count()
    test_emi_scenarios()
    test_bearish_market_higher_risk()
    test_villa_higher_liquidity_risk()
    print("\n" + "=" * 50)
    print("  🎉 ALL RISK TESTS PASSED!")
    print("=" * 50)
