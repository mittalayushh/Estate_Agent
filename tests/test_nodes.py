"""Test: Individual node transitions."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.nodes import validate_input_node, valuation_node, research_node, comparable_node, risk_node


def test_node_flow():
    print("🚀 Testing Node Transitions...\n")

    # Initial State
    initial_state = {
        "property_input": {
            'Property_Type': 'Apartment', 'BHK': 3,
            'Furnished_Status': 'Semi-furnished',
            'Size_in_SqFt': 1800, 'Bathrooms': 3,
            'Public_Transport_Accessibility': 'High',
            'Facing': 'East', 'Security': 'Yes',
            'City': 'Mumbai', 'State': 'Maharashtra'
        },
        "user_preferences": {},
        "market_context": []
    }

    # 1. Validate
    val_result = validate_input_node(initial_state)
    print(f"✅ Validate Node: {val_result['current_step']}")
    assert val_result['current_step'] == "Input Validated"

    # 2. Valuation
    state = {**initial_state, **val_result}
    price_result = valuation_node(state)
    print(f"✅ Valuation Node: ₹{price_result['predicted_price']} Lakhs")
    assert isinstance(price_result['predicted_price'], float)
    assert price_result['confidence_score'] > 0

    # 3. Research
    res_result = research_node(state)
    print(f"✅ Research Node: {len(res_result['market_context'][0])} chars retrieved")
    assert len(res_result['market_context'][0]) > 50

    # 4. Comparable
    state = {**state, **price_result}
    comp_result = comparable_node(state)
    print(f"✅ Comparable Node: {len(comp_result['comparable_properties'])} comparables generated")
    assert len(comp_result['comparable_properties']) > 0

    # 5. Risk
    state = {**state, **res_result}
    risk_result = risk_node(state)
    print(f"✅ Risk Node: {risk_result['risk_assessment']['overall_risk_level']}")
    assert risk_result['risk_assessment']['overall_risk_score'] >= 0

    print("\n🎉 All node tests passed!")


if __name__ == "__main__":
    test_node_flow()