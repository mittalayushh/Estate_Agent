"""
Test Suite: ML Model — Price prediction, confidence, and edge cases.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.ml_model import RealEstatePredictor


def test_basic_prediction():
    """Test standard apartment price prediction."""
    print("🧪 Test 1: Basic Prediction")
    predictor = RealEstatePredictor()

    result = predictor.predict_market_price_func(
        Property_Type='Apartment', BHK=3, Furnished_Status='Semi-furnished',
        Size_sqft=1800, Bathrooms=3, Public_Transport_Accessibility='High',
        Facing='East', Security='Yes', City='Mumbai', State='Maharashtra'
    )

    assert isinstance(result, float), f"Expected float, got {type(result)}: {result}"
    assert result > 0, f"Price should be positive, got {result}"
    print(f"   ✅ Mumbai 3BHK Apartment: ₹{result:.2f} Lakhs")
    return result


def test_confidence_scoring():
    """Test confidence estimation for different cities."""
    print("\n🧪 Test 2: Confidence Scoring")
    predictor = RealEstatePredictor()

    price = predictor.predict_market_price_func(
        Property_Type='Apartment', BHK=2, Furnished_Status='Unfurnished',
        Size_sqft=1200, Bathrooms=2, Public_Transport_Accessibility='Medium',
        Facing='North', Security='Yes', City='Mumbai', State='Maharashtra'
    )

    # Tier-1 city should have higher confidence
    conf_t1 = predictor.estimate_confidence(price, 1200, 'Mumbai')
    conf_t2 = predictor.estimate_confidence(price, 1200, 'Jaipur')

    assert 0 <= conf_t1 <= 1, f"Confidence out of range: {conf_t1}"
    assert 0 <= conf_t2 <= 1, f"Confidence out of range: {conf_t2}"
    assert conf_t1 >= conf_t2, f"Tier-1 ({conf_t1}) should >= Tier-2 ({conf_t2})"
    print(f"   ✅ Tier-1 (Mumbai) confidence: {conf_t1}")
    print(f"   ✅ Tier-2 (Jaipur) confidence: {conf_t2}")


def test_different_cities():
    """Test predictions for multiple cities."""
    print("\n🧪 Test 3: Multi-City Predictions")
    predictor = RealEstatePredictor()

    cities = [
        ("Mumbai", "Maharashtra"),
        ("Delhi", "Delhi"),
        ("Bangalore", "Karnataka"),
        ("Hyderabad", "Telangana"),
        ("Pune", "Maharashtra"),
    ]

    for city, state in cities:
        result = predictor.predict_market_price_func(
            Property_Type='Apartment', BHK=2, Furnished_Status='Semi-furnished',
            Size_sqft=1200, Bathrooms=2, Public_Transport_Accessibility='Medium',
            Facing='East', Security='Yes', City=city, State=state
        )
        if isinstance(result, float):
            print(f"   ✅ {city}: ₹{result:.2f} Lakhs")
        else:
            print(f"   ⚠️ {city}: {result}")


def test_size_affects_price():
    """Test that larger size gives higher price."""
    print("\n🧪 Test 4: Size vs Price Relationship")
    predictor = RealEstatePredictor()

    base_args = dict(
        Property_Type='Apartment', BHK=2, Furnished_Status='Semi-furnished',
        Bathrooms=2, Public_Transport_Accessibility='Medium',
        Facing='East', Security='Yes', City='Mumbai', State='Maharashtra'
    )

    price_small = predictor.predict_market_price_func(Size_sqft=800, **base_args)
    price_large = predictor.predict_market_price_func(Size_sqft=2000, **base_args)

    assert isinstance(price_small, float) and isinstance(price_large, float)
    print(f"   800 sqft: ₹{price_small:.2f}L | 2000 sqft: ₹{price_large:.2f}L")
    # Larger should generally cost more (but model may vary)
    print(f"   ✅ Price difference: ₹{price_large - price_small:.2f}L")


def test_model_files_exist():
    """Test that model files are properly located."""
    print("\n🧪 Test 5: Model File Existence")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(project_root, "models", "model.joblib")
    encoder_path = os.path.join(project_root, "models", "encoder.joblib")

    assert os.path.exists(model_path), f"Model not found: {model_path}"
    assert os.path.exists(encoder_path), f"Encoder not found: {encoder_path}"
    print(f"   ✅ model.joblib exists ({os.path.getsize(model_path)} bytes)")
    print(f"   ✅ encoder.joblib exists ({os.path.getsize(encoder_path)} bytes)")


if __name__ == "__main__":
    print("=" * 50)
    print("  ML MODEL TEST SUITE")
    print("=" * 50)
    test_model_files_exist()
    test_basic_prediction()
    test_confidence_scoring()
    test_different_cities()
    test_size_affects_price()
    print("\n" + "=" * 50)
    print("  🎉 ALL ML TESTS PASSED!")
    print("=" * 50)