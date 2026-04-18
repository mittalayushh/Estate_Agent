import joblib
import pandas as pd
from langchain.tools import tool

class RealEstatePredictor:
    def __init__(self):
        # Load the "Brain" and the "Translators"
        self.model = joblib.load('models/model.joblib')
        translators = joblib.load('models/encoder.joblib')
        
        self.ordinal_encoder = translators['ordinal_encoder']
        self.dict_vectorizer = translators['dict_vectorizer']
        
        # Features requiring ordinal encoding (Matching your notebook)
        self.ordinal_cols = [
            'Property_Type', 'Furnished_Status', 
            'Public_Transport_Accessibility', 'Facing', 'Security'
        ]

    @tool
    def predict_market_price(self, details: dict):
        """
        Calculates the market valuation of an Indian property in Lakhs.
        Input dictionary keys: Property_Type, BHK, Furnished_Status, 
        Size_sqft, Bathrooms, Public_Transport_Accessibility, Facing, Security.
        """
        try:
            # 1. Prepare Dataframe
            df = pd.DataFrame([details])
            
            # 2. Categorical Translation (Text -> Numbers)
            df[self.ordinal_cols] = self.ordinal_encoder.transform(df[self.ordinal_cols])
            
            # 3. Vectorization (Data -> Matrix)
            data_dict = df.to_dict(orient='records')
            X = self.dict_vectorizer.transform(data_dict)
            
            # 4. XGBoost Prediction
            prediction = self.model.predict(X)[0]
            
            return float(prediction)
        except Exception as e:
            return f"Valuation Error: {str(e)}"