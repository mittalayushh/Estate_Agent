"""Test: Full 7-node agentic workflow end-to-end."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.graph import app
from dotenv import load_dotenv

load_dotenv()


def test_full_agent():
    print("🌍 STARTING FULL 7-NODE AGENTIC WORKFLOW TEST...\n")

    inputs = {
        "property_input": {
            'Property_Type': 'Apartment', 'BHK': 3,
            'Furnished_Status': 'Semi-furnished',
            'Size_in_SqFt': 1800, 'Bathrooms': 3,
            'Public_Transport_Accessibility': 'High',
            'Facing': 'East', 'Security': 'Yes',
            'City': 'Mumbai', 'State': 'Maharashtra'
        },
        "user_preferences": {
            'budget_min': 80,
            'budget_max': 200,
            'investment_horizon': 5,
            'risk_appetite': 'Moderate'
        },
        "market_context": []
    }

    # Run the Graph and stream outputs
    final_state = None
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"\n📍 FINISHED STEP: {key} → {value.get('current_step', '')}")
            final_state = {**inputs, **(final_state or {}), **value}

    # Validate outputs
    assert final_state is not None, "No output from agent"
    assert final_state.get("predicted_price") is not None, "No price prediction"
    assert final_state.get("final_advisory") is not None, "No advisory report"
    assert len(final_state.get("comparable_properties", [])) > 0, "No comparables"
    assert final_state.get("risk_assessment") is not None, "No risk assessment"

    print("\n" + "=" * 60)
    print("FINAL ADVISORY REPORT")
    print("=" * 60)
    print(final_state["final_advisory"][:1000] + "...")

    print("\n" + "=" * 60)
    print("AGENT TRACE")
    print("=" * 60)
    for step in final_state.get("agent_trace", []):
        print(f"  {step}")

    print("\n🎉 Full agent test passed!")


if __name__ == "__main__":
    test_full_agent()