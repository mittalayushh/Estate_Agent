"""
ML Model Tool — XGBoost Property Price Predictor.

Wraps the trained model for use by the LangGraph agent.
All paths are dynamically resolved — no hardcoded paths.
"""

import os
import joblib
import pandas as pd
import numpy as np
from langchain_core.tools import tool


# Resolve paths relative to project root
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_MODEL_PATH = os.path.join(_PROJECT_ROOT, "models", "model.joblib")
_ENCODER_PATH = os.path.join(_PROJECT_ROOT, "models", "encoder.joblib")


class RealEstatePredictor:
    """Loads the trained XGBoost model and encoders for price prediction."""

    def __init__(self):
        if not os.path.exists(_MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {_MODEL_PATH}. Train the model first.")
        if not os.path.exists(_ENCODER_PATH):
            raise FileNotFoundError(f"Encoder not found at {_ENCODER_PATH}. Train the model first.")

        self.model = joblib.load(_MODEL_PATH)
        translators = joblib.load(_ENCODER_PATH)

        self.ordinal_encoder = translators['ordinal_encoder']
        self.dict_vectorizer = translators['dict_vectorizer']

        self.ordinal_cols = [
            'Property_Type', 'Furnished_Status',
            'Public_Transport_Accessibility', 'Facing', 'Security'
        ]

    @tool
    def predict_market_price(
        self,
        Property_Type: str,
        BHK: int,
        Furnished_Status: str,
        Size_sqft: float,
        Bathrooms: int,
        Public_Transport_Accessibility: str,
        Facing: str,
        Security: str,
        City: str,
        State: str
    ):
        """Calculates market valuation using XGBoost. Use City/State as in training data."""
        return self.predict_market_price_func(
            Property_Type=Property_Type, BHK=BHK,
            Furnished_Status=Furnished_Status, Size_sqft=Size_sqft,
            Bathrooms=Bathrooms, Public_Transport_Accessibility=Public_Transport_Accessibility,
            Facing=Facing, Security=Security, City=City, State=State
        )

    def predict_market_price_func(self, **kwargs):
        """Core prediction logic — callable directly without LangChain tool wrapper."""
        try:
            details = {
                'Property_Type': kwargs.get('Property_Type'),
                'BHK': kwargs.get('BHK'),
                'Furnished_Status': kwargs.get('Furnished_Status'),
                'Size_in_SqFt': kwargs.get('Size_sqft'),
                'Bathrooms': kwargs.get('Bathrooms'),
                'Public_Transport_Accessibility': kwargs.get('Public_Transport_Accessibility'),
                'Facing': kwargs.get('Facing'),
                'Security': kwargs.get('Security'),
                'City': kwargs.get('City', '').lower(),
                'State': kwargs.get('State', '').lower()
            }

            df = pd.DataFrame([details])

            # Encode ordinal columns
            df[self.ordinal_cols] = self.ordinal_encoder.transform(df[self.ordinal_cols])

            # Vectorize for model input
            data_dict = df.to_dict(orient='records')
            X = self.dict_vectorizer.transform(data_dict)

            prediction = self.model.predict(X)[0]
            return float(prediction)

        except Exception as e:
            return f"Valuation Error: {str(e)}"

    def estimate_confidence(self, predicted_price: float, size_sqft: float, city: str) -> float:
        """
        Estimates prediction confidence based on how typical the input is.
        Returns a value between 0.0 and 1.0.
        """
        confidence = 0.85  # Base confidence for XGBoost

        # Penalize extreme price-per-sqft ratios
        if size_sqft and size_sqft > 0:
            price_per_sqft = (predicted_price * 100000) / size_sqft  # Convert lakhs to INR
            if price_per_sqft < 1000 or price_per_sqft > 50000:
                confidence -= 0.15  # Unusual price range
            elif price_per_sqft < 2000 or price_per_sqft > 30000:
                confidence -= 0.05

        # Higher confidence for tier-1 cities (more training data)
        tier1_cities = ['mumbai', 'delhi', 'bangalore', 'bengaluru', 'hyderabad', 'chennai', 'pune', 'kolkata']
        if city.lower() in tier1_cities:
            confidence += 0.05
        else:
            confidence -= 0.10

        return round(max(0.3, min(1.0, confidence)), 2)