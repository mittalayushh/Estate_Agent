import sys
import os

# Add project root to Python path so we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.ml_model import RealEstatePredictor

def test_ml_tool():
    print("🚀 Initializing ML Tool Test...")
    predictor = RealEstatePredictor()

    # Sample data matching your notebook's requirements
    test_property = {
            'Property_Type': 'Apartment',
            'BHK': 3,
            'Furnished_Status': 'Semi-furnished',
            'Size_in_SqFt': 1800,
            'Bathrooms': 3,
            'Public_Transport_Accessibility': 'High',
            'Facing': 'East',
            'Security': 'Yes',
            'City': 'Mumbai', # Use a city from your dataset
            'State': 'Maharashtra'
    }

    result = predictor.predict_market_price_func(
        Property_Type=test_property['Property_Type'],
        BHK=test_property['BHK'],
        Furnished_Status=test_property['Furnished_Status'],
        Size_sqft=test_property['Size_in_SqFt'],
        Bathrooms=test_property['Bathrooms'],
        Public_Transport_Accessibility=test_property['Public_Transport_Accessibility'],
        Facing=test_property['Facing'],
        Security=test_property['Security'],
        City=test_property['City'],
        State=test_property['State']
    )
    
    print(f"\n✅ Result: {result}")

if __name__ == "__main__":
    test_ml_tool()