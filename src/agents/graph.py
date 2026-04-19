"""
LangGraph Workflow — 7-node advisory pipeline with conditional edges.

Flow: validate → valuate → research → comparable → risk → advisory → quality_check
With a conditional retry loop: quality_check can send back to advisory (max 1 retry).
"""

from langgraph.graph import StateGraph, END
from src.agents.state import AgentState
from src.agents.nodes import (
    validate_input_node,
    valuation_node,
    research_node,
    comparable_node,
    risk_node,
    advisory_node,
    quality_check_node
)


def _should_retry(state: AgentState) -> str:
    """Conditional edge: retry advisory if quality check found missing sections."""
    step = state.get("current_step", "")
    trace = state.get("agent_trace", [])

    # Count how many times advisory has run (prevent infinite loops)
    advisory_runs = sum(1 for t in trace if "Node 6:" in t)

    if "PARTIAL" in step and advisory_runs < 2:
        print("🔄 Quality check failed — retrying advisory node...")
        return "retry"
    return "finish"


def build_graph():
    """Builds and compiles the 7-node LangGraph workflow."""

    workflow = StateGraph(AgentState)

    # ── Add Nodes ──
    workflow.add_node("validate", validate_input_node)
    workflow.add_node("valuation", valuation_node)
    workflow.add_node("research", research_node)
    workflow.add_node("comparable", comparable_node)
    workflow.add_node("risk", risk_node)
    workflow.add_node("advisory", advisory_node)
    workflow.add_node("quality_check", quality_check_node)

    # ── Define Flow ──
    workflow.set_entry_point("validate")
    workflow.add_edge("validate", "valuation")
    workflow.add_edge("valuation", "research")
    workflow.add_edge("research", "comparable")
    workflow.add_edge("comparable", "risk")
    workflow.add_edge("risk", "advisory")
    workflow.add_edge("advisory", "quality_check")

    # ── Conditional Edge: Retry or Finish ──
    workflow.add_conditional_edges(
        "quality_check",
        _should_retry,
        {
            "retry": "advisory",
            "finish": END
        }
    )

    return workflow.compile()


# Global app instance
app = build_graph()