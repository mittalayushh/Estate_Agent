"""
Comparable Property Analyzer — Generates comparable property analysis.

Runs the ML model with parameter variations to show how similar
properties are priced, giving investors a relative value perspective.
"""

import os
import sys

# Ensure project root is in path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def generate_comparables(predictor, property_input: dict, predicted_price: float) -> list:
    """
    Generates comparable property analysis by varying key parameters.

    Args:
        predictor: RealEstatePredictor instance
        property_input: Original property details dict
        predicted_price: The predicted price of the original property

    Returns:
        List of dicts, each representing a comparable property with price differential
    """
    comparables = []

    # Define variations to test
    variations = [
        {
            "label": "Same area, 1 BHK less",
            "changes": {"BHK": max(1, property_input.get('BHK', 2) - 1),
                        "Bathrooms": max(1, property_input.get('Bathrooms', 2) - 1)}
        },
        {
            "label": "Same area, 1 BHK more",
            "changes": {"BHK": property_input.get('BHK', 2) + 1,
                        "Bathrooms": property_input.get('Bathrooms', 2) + 1}
        },
        {
            "label": "20% smaller unit",
            "changes": {"Size_in_SqFt": int(property_input.get('Size_in_SqFt', 1500) * 0.8)}
        },
        {
            "label": "20% larger unit",
            "changes": {"Size_in_SqFt": int(property_input.get('Size_in_SqFt', 1500) * 1.2)}
        },
        {
            "label": "Unfurnished variant",
            "changes": {"Furnished_Status": "Unfurnished"}
        },
        {
            "label": "Fully furnished variant",
            "changes": {"Furnished_Status": "Fully furnished"}
        },
    ]

    for variation in variations:
        # Skip if the variation matches the original
        skip = True
        for key, val in variation["changes"].items():
            if property_input.get(key) != val:
                skip = False
                break
        if skip:
            continue

        # Build modified property input
        modified = property_input.copy()
        modified.update(variation["changes"])

        try:
            comp_price = predictor.predict_market_price_func(
                Property_Type=modified.get('Property_Type', 'Apartment'),
                BHK=modified.get('BHK', 2),
                Furnished_Status=modified.get('Furnished_Status', 'Semi-furnished'),
                Size_sqft=modified.get('Size_in_SqFt', 1500),
                Bathrooms=modified.get('Bathrooms', 2),
                Public_Transport_Accessibility=modified.get('Public_Transport_Accessibility', 'Medium'),
                Facing=modified.get('Facing', 'East'),
                Security=modified.get('Security', 'Yes'),
                City=modified.get('City', 'Mumbai'),
                State=modified.get('State', 'Maharashtra')
            )

            if isinstance(comp_price, (int, float)):
                diff_pct = ((comp_price - predicted_price) / predicted_price) * 100

                comparables.append({
                    "label": variation["label"],
                    "bhk": modified.get('BHK'),
                    "size_sqft": modified.get('Size_in_SqFt'),
                    "furnished": modified.get('Furnished_Status'),
                    "predicted_price_lakhs": round(comp_price, 2),
                    "price_diff_pct": round(diff_pct, 1),
                    "price_diff_lakhs": round(comp_price - predicted_price, 2)
                })
        except Exception:
            continue  # Skip failed predictions silently

    return comparables
