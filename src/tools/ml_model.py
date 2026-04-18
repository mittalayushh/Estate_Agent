import joblib
import pandas as pd
from langchain_core.tools import tool

class RealEstatePredictor:
    def __init__(self):
        # Path assumes models/ is in the project root
        self.model = joblib.load('models/model.joblib')
        translators = joblib.load('models/encoder.joblib')
        
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
        City: str,     # Added
        State: str     # Added
    ):
        """Calculates market valuation. Use City/State as used in training."""
        return self.predict_market_price_func(
            Property_Type, BHK, Furnished_Status, Size_sqft, 
            Bathrooms, Public_Transport_Accessibility, Facing, Security, City, State
        )

    def predict_market_price_func(self, **kwargs):
        try:
            # Match the exact column names from your notebook's CSV
            details = {
                'Property_Type': kwargs.get('Property_Type'),
                'BHK': kwargs.get('BHK'),
                'Furnished_Status': kwargs.get('Furnished_Status'),
                'Size_in_SqFt': kwargs.get('Size_sqft'), 
                'Bathrooms': kwargs.get('Bathrooms'),
                'Public_Transport_Accessibility': kwargs.get('Public_Transport_Accessibility'),
                'Facing': kwargs.get('Facing'),
                'Security': kwargs.get('Security'),
                'City': kwargs.get('City').lower(),  # Match the .lower() in your notebook
                'State': kwargs.get('State').lower() # Match the .lower() in your notebook
            }

            df = pd.DataFrame([details])
            
            # Translate text categories
            df[self.ordinal_cols] = self.ordinal_encoder.transform(df[self.ordinal_cols])

            # Vectorize (this will now find the City/State columns it expects)
            data_dict = df.to_dict(orient='records')
            X = self.dict_vectorizer.transform(data_dict)

            prediction = self.model.predict(X)[0]
            return float(prediction)
        except Exception as e:
            return f"Valuation Error: {str(e)}"