"""
Agent Nodes — 7 reasoning steps for the real estate advisory pipeline.

Each node takes the AgentState, performs a specific reasoning task,
and returns a partial state update. Anti-hallucination prompting
strategies are embedded in the advisory node.
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from src.tools.ml_model import RealEstatePredictor
from src.tools.search_rag import market_researcher, rera_researcher
from src.tools.comparable_analyzer import generate_comparables
from src.tools.risk_simulator import run_risk_simulation
from src.tools.market_sentiment import analyze_market_sentiment
from src.agents.state import AgentState

# Load environment variables
load_dotenv()

# Initialize Tools and LLM
predictor = RealEstatePredictor()

# Use Groq (free & fast) as primary, fallback to OpenAI
if os.getenv("GROQ_API_KEY") and os.getenv("GROQ_API_KEY") != "your_groq_api_key_here":
    from langchain_groq import ChatGroq
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    print("🟢 LLM: Groq (llama-3.3-70b-versatile)")
elif os.getenv("OPENAI_API_KEY"):
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    print("🟢 LLM: OpenAI (gpt-4o-mini)")
else:
    raise EnvironmentError(
        "No LLM API key found! Set GROQ_API_KEY or OPENAI_API_KEY in your .env file.\n"
        "Get a free Groq key at: https://console.groq.com/keys"
    )


# ────────────────────────────────────────────
# Node 1: Input Validation
# ────────────────────────────────────────────
def validate_input_node(state: AgentState) -> dict:
    """Validates and normalizes property input data."""
    print("--- ✅ NODE 1: Input Validation ---")

    data = state.get("property_input", {})
    prefs = state.get("user_preferences", {})

    # Apply defaults for missing fields
    defaults = {
        'Property_Type': 'Apartment',
        'BHK': 2,
        'Furnished_Status': 'Semi-furnished',
        'Size_in_SqFt': 1200,
        'Bathrooms': 2,
        'Public_Transport_Accessibility': 'Medium',
        'Facing': 'East',
        'Security': 'Yes',
        'City': 'Mumbai',
        'State': 'Maharashtra'
    }

    for key, default_val in defaults.items():
        if key not in data or data[key] is None:
            data[key] = default_val

    pref_defaults = {
        'budget_min': 0,
        'budget_max': 999,
        'investment_horizon': 5,
        'risk_appetite': 'Moderate'
    }
    for key, default_val in pref_defaults.items():
        if key not in prefs or prefs[key] is None:
            prefs[key] = default_val

    return {
        "property_input": data,
        "user_preferences": prefs,
        "current_step": "Input Validated",
        "agent_trace": ["✅ Node 1: Input validated and normalized"]
    }


# ────────────────────────────────────────────
# Node 2: ML Valuation
# ────────────────────────────────────────────
def valuation_node(state: AgentState) -> dict:
    """Runs the XGBoost model to predict property market value."""
    print("--- 🤖 NODE 2: ML Valuation ---")

    data = state["property_input"]

    price = predictor.predict_market_price_func(
        Property_Type=data['Property_Type'],
        BHK=data['BHK'],
        Furnished_Status=data['Furnished_Status'],
        Size_sqft=data['Size_in_SqFt'],
        Bathrooms=data['Bathrooms'],
        Public_Transport_Accessibility=data['Public_Transport_Accessibility'],
        Facing=data['Facing'],
        Security=data['Security'],
        City=data['City'],
        State=data['State']
    )

    # Estimate confidence
    confidence = 0.0
    if isinstance(price, (int, float)):
        confidence = predictor.estimate_confidence(price, data['Size_in_SqFt'], data['City'])

    return {
        "predicted_price": price if isinstance(price, (int, float)) else 0.0,
        "confidence_score": confidence,
        "current_step": "Valuation Complete",
        "agent_trace": [f"🤖 Node 2: XGBoost predicted ₹{price} Lakhs (confidence: {confidence})"]
    }


# ────────────────────────────────────────────
# Node 3: RAG Market Research
# ────────────────────────────────────────────
def research_node(state: AgentState) -> dict:
    """Retrieves market trends and RERA guidelines from the knowledge base."""
    print("--- 📚 NODE 3: Market Research ---")

    city = state["property_input"].get("City", "India")
    prop_type = state["property_input"].get("Property_Type", "Apartment")

    # Market trends query
    market_query = f"Real estate market trends price appreciation demand for {prop_type} in {city} 2024"
    market_context = market_researcher.run(market_query)

    # RERA/Legal query
    rera_query = f"RERA compliance guidelines buyer protection rules for {city}"
    rera_context = rera_researcher.run(rera_query)

    return {
        "market_context": [market_context],
        "rera_guidelines": rera_context,
        "current_step": "Research Complete",
        "agent_trace": [
            f"📚 Node 3: Retrieved market data for {city} ({len(market_context)} chars)",
            f"📚 Node 3: Retrieved RERA guidelines ({len(rera_context)} chars)"
        ]
    }


# ────────────────────────────────────────────
# Node 4: Comparable Property Analysis
# ────────────────────────────────────────────
def comparable_node(state: AgentState) -> dict:
    """Generates comparable property analysis using ML model variations."""
    print("--- 🏘️ NODE 4: Comparable Analysis ---")

    comparables = generate_comparables(
        predictor=predictor,
        property_input=state["property_input"],
        predicted_price=state.get("predicted_price", 0)
    )

    return {
        "comparable_properties": comparables,
        "current_step": "Comparables Generated",
        "agent_trace": [f"🏘️ Node 4: Generated {len(comparables)} comparable properties"]
    }


# ────────────────────────────────────────────
# Node 5: Risk Simulation
# ────────────────────────────────────────────
def risk_node(state: AgentState) -> dict:
    """Runs multi-factor risk assessment."""
    print("--- ⚠️ NODE 5: Risk Assessment ---")

    market_context_str = "\n".join(state.get("market_context", []))

    risk_data = run_risk_simulation(
        predicted_price=state.get("predicted_price", 0),
        city=state["property_input"].get("City", "Unknown"),
        property_type=state["property_input"].get("Property_Type", "Apartment"),
        size_sqft=state["property_input"].get("Size_in_SqFt", 0),
        market_context=market_context_str
    )

    # Also compute market sentiment
    sentiment = analyze_market_sentiment(
        market_context=market_context_str,
        city=state["property_input"].get("City", "Unknown")
    )

    return {
        "risk_assessment": risk_data,
        "market_sentiment": sentiment,
        "current_step": "Risk Assessment Complete",
        "agent_trace": [
            f"⚠️ Node 5: Risk level = {risk_data['overall_risk_level']} (score: {risk_data['overall_risk_score']})",
            f"📈 Node 5: Market sentiment = {sentiment['sentiment_label']}"
        ]
    }


# ────────────────────────────────────────────
# Node 6: LLM Advisory Report
# ────────────────────────────────────────────
def advisory_node(state: AgentState) -> dict:
    """Synthesizes all data into a structured 5-section investment advisory report."""
    print("--- 🧠 NODE 6: Advisory Report Generation ---")

    # Build comparables summary
    comp_text = "No comparable data available."
    comps = state.get("comparable_properties", [])
    if comps:
        comp_lines = []
        for c in comps:
            comp_lines.append(
                f"  - {c['label']}: {c['bhk']}BHK, {c['size_sqft']}sqft, "
                f"₹{c['predicted_price_lakhs']}L ({c['price_diff_pct']:+.1f}%)"
            )
        comp_text = "\n".join(comp_lines)

    # Build risk summary
    risk_text = "No risk data available."
    risk = state.get("risk_assessment", {})
    if risk:
        risk_lines = [f"Overall: {risk.get('overall_risk_level', 'N/A')} (Score: {risk.get('overall_risk_score', 0)}/100)"]
        for f in risk.get("risk_factors", []):
            risk_lines.append(f"  - {f['factor']} [{f['severity']}]: {f['details']}")
        risk_text = "\n".join(risk_lines)

    # Build sentiment summary
    sentiment = state.get("market_sentiment", {})
    sentiment_text = f"{sentiment.get('sentiment_label', 'N/A')} — {sentiment.get('outlook', '')}"

    # User preferences
    prefs = state.get("user_preferences", {})
    prefs_text = (
        f"Budget: ₹{prefs.get('budget_min', 0)}-{prefs.get('budget_max', 999)} Lakhs, "
        f"Horizon: {prefs.get('investment_horizon', 5)} years, "
        f"Risk Appetite: {prefs.get('risk_appetite', 'Moderate')}"
    )

    prompt = ChatPromptTemplate.from_template("""You are **Estate Agent AI**, a Senior Real Estate Investment Advisor specializing in Indian property markets. You communicate with clarity, precision, and professional authority.

**ANALYSIS INPUTS:**
- Property: {input}
- Investor Profile: {preferences}
- ML Prediction: ₹{price} Lakhs (Confidence: {confidence})
- Sentiment: {sentiment}

**COMPARABLE PROPERTIES:**
{comparables}

**RISK MATRIX:**
{risk}

**MARKET INTELLIGENCE (verified sources — Knight Frank, JLL, RERA):**
{context}

**REGULATORY CONTEXT:**
{rera}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generate a structured advisory with EXACTLY these 5 sections. Use markdown formatting — bold key terms, use bullet points, and write in a confident advisory tone:

## PROPERTY VALUATION SUMMARY
Write 3-4 paragraphs covering:
- State the ML-predicted price clearly: "Based on my analysis of 10 property features, the predicted market value is **₹X Lakhs**"
- Calculate and discuss price-per-sqft (predicted_price * 100000 / size_sqft)
- Interpret the confidence score: what it means for the buyer
- How current market sentiment affects this valuation
- Compare against city benchmark ranges if available from context

## COMPARABLE PROPERTY ANALYSIS
For each comparable provided, write a brief analysis:
- Present as a structured comparison: "A **[variant]** at ₹X Lakhs represents a **[+/-X%]** differential"
- Explain WHY the price differs (more bedrooms = more value, larger area = premium, etc.)
- Identify which comparable represents the best value-for-money
- Position the subject property: "Your property sits **[above/below/at]** the median of comparables"

## MARKET & REGULATORY ANALYSIS
Write 2-3 paragraphs using ONLY data from the MARKET INTELLIGENCE above:
- City-specific trends: demand, appreciation rates, infrastructure catalysts
- RERA compliance: key provisions buyers should verify
- Supply-demand dynamics and inventory levels
- Cite sources: "According to [JLL/Knight Frank], ..."

## INVESTMENT RECOMMENDATION
Start with a clear verdict: "**RECOMMENDATION: [BUY / HOLD / AVOID]**"
Then provide:
- 3-4 bullet points justifying the recommendation
- Expected ROI range for the stated investment horizon
- Risk-adjusted analysis matching the investor's risk appetite
- Financing insight: reference the EMI scenarios from the risk data
- Timing advice: "Based on current market conditions, [now is / is not] an optimal entry point"

## DISCLAIMER
Write a professional legal disclaimer:
- This is AI-generated advisory, not licensed financial advice
- Always verify RERA registration on the state portal before purchase
- Consult a certified financial advisor and legal counsel before investing
- Past market performance does not guarantee future returns

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULES:
1. CITE ONLY data from the provided MARKET INTELLIGENCE and REGULATORY CONTEXT
2. If data is insufficient, state: "Insufficient data available for this specific micro-market"
3. Do NOT invent statistics or price figures — use ONLY the exact numbers provided
4. Use the predicted price and comparables AS-IS — do not recalculate them
5. Write in first person as an AI advisor: "Based on my analysis...", "I recommend..."
6. The DISCLAIMER section is MANDATORY
""")

    chain = prompt | llm
    report = chain.invoke({
        "input": state["property_input"],
        "preferences": prefs_text,
        "price": state.get("predicted_price", "N/A"),
        "confidence": state.get("confidence_score", "N/A"),
        "sentiment": sentiment_text,
        "comparables": comp_text,
        "risk": risk_text,
        "context": "\n".join(state.get("market_context", ["No market data available"])),
        "rera": state.get("rera_guidelines", "No RERA data available")
    })

    report_text = report.content

    # Parse into sections for UI tabs
    sections = _parse_report_sections(report_text)

    return {
        "final_advisory": report_text,
        "report_sections": sections,
        "current_step": "Advisory Report Generated",
        "agent_trace": [f"🧠 Node 6: Generated advisory report ({len(report_text)} chars, {len(sections)} sections)"]
    }


# ────────────────────────────────────────────
# Node 7: Quality Check
# ────────────────────────────────────────────
def quality_check_node(state: AgentState) -> dict:
    """Validates the advisory report has all required sections."""
    print("--- 🔍 NODE 7: Quality Check ---")

    report = state.get("final_advisory", "")
    sections = state.get("report_sections", {})

    required_keywords = ["SUMMARY", "COMPARABLE", "MARKET", "RECOMMENDATION", "DISCLAIMER"]
    missing = []

    report_upper = report.upper()
    for keyword in required_keywords:
        if keyword not in report_upper:
            missing.append(keyword)

    quality = "PASS" if len(missing) == 0 else f"PARTIAL (missing: {', '.join(missing)})"

    return {
        "current_step": f"Quality Check: {quality}",
        "agent_trace": [f"🔍 Node 7: Quality check = {quality}"]
    }


# ────────────────────────────────────────────
# Helper: Parse report into sections
# ────────────────────────────────────────────
def _parse_report_sections(report_text: str) -> dict:
    """Splits the LLM report into sections by ## headers."""
    sections = {}
    current_key = "Overview"
    current_lines = []

    for line in report_text.split("\n"):
        if line.startswith("## "):
            if current_lines:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = line.replace("## ", "").strip()
            # Clean up numbered prefixes like "1. " or "2. "
            if current_key and current_key[0].isdigit() and ". " in current_key:
                current_key = current_key.split(". ", 1)[1]
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections