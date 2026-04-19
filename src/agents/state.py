"""
Enhanced Agent State — Tracks the full advisory pipeline.

Each key represents a distinct phase of reasoning, enabling
LangGraph to pass structured data between nodes.
"""

from typing import TypedDict, Annotated, List, Optional
import operator


class AgentState(TypedDict):
    # ── User Inputs ──
    property_input: dict                # Raw property details (BHK, City, Size, etc.)
    user_preferences: dict              # Budget range, investment horizon, risk appetite

    # ── ML Prediction ──
    predicted_price: Optional[float]    # XGBoost predicted price in Lakhs
    confidence_score: Optional[float]   # Model confidence estimate (0-1)

    # ── RAG Research ──
    market_context: Annotated[List[str], operator.add]  # Retrieved market documents
    rera_guidelines: Optional[str]      # Specific RERA findings for the city

    # ── Comparable Analysis ──
    comparable_properties: Optional[List[dict]]  # Similar properties with prices

    # ── Risk Assessment ──
    risk_assessment: Optional[dict]     # Market risk factors & scenario analysis

    # ── Market Sentiment ──
    market_sentiment: Optional[dict]    # Extracted sentiment indicators

    # ── Final Output ──
    final_advisory: Optional[str]       # Full structured 5-section report
    report_sections: Optional[dict]     # Parsed sections for UI tab display

    # ── Pipeline Tracking ──
    current_step: str                   # Current node name
    agent_trace: Annotated[List[str], operator.add]  # Full reasoning log