"""
Risk Simulator — What-if scenario analysis for real estate investments.

Evaluates interest rate sensitivity, market cycle positioning,
and location appreciation potential to produce a structured risk matrix.
"""


def run_risk_simulation(
    predicted_price: float,
    city: str,
    property_type: str,
    size_sqft: float,
    market_context: str
) -> dict:
    """
    Runs a multi-factor risk assessment for the property.

    Args:
        predicted_price: ML-predicted price in Lakhs
        city: Property city
        property_type: Apartment/House/Villa etc.
        size_sqft: Property size
        market_context: RAG-retrieved market insights

    Returns:
        dict with risk factors, severity levels, and overall assessment
    """
    risk_factors = []
    overall_risk_score = 0  # 0-100 scale

    # ── Factor 1: Interest Rate Sensitivity ──
    # EMI impact at different interest rates
    loan_amount = predicted_price * 0.8 * 100000  # 80% LTV in INR
    tenure_months = 240  # 20 years

    emi_scenarios = {}
    for rate in [7.5, 8.5, 9.5, 10.5]:
        monthly_rate = rate / 12 / 100
        emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months) / \
              (((1 + monthly_rate) ** tenure_months) - 1)
        emi_scenarios[f"{rate}%"] = round(emi / 1000, 1)  # In thousands

    rate_spread = emi_scenarios["10.5%"] - emi_scenarios["7.5%"]
    if rate_spread > 30:
        severity = "HIGH"
        overall_risk_score += 25
    elif rate_spread > 15:
        severity = "MEDIUM"
        overall_risk_score += 15
    else:
        severity = "LOW"
        overall_risk_score += 5

    risk_factors.append({
        "factor": "Interest Rate Sensitivity",
        "severity": severity,
        "details": f"EMI range: ₹{emi_scenarios['7.5%']}K to ₹{emi_scenarios['10.5%']}K/month",
        "emi_scenarios": emi_scenarios
    })

    # ── Factor 2: Market Cycle Position ──
    market_lower = market_context.lower() if market_context else ""

    bullish_signals = sum(1 for term in [
        "growth", "appreciation", "demand", "rising", "boom", "surge", "bullish"
    ] if term in market_lower)

    bearish_signals = sum(1 for term in [
        "decline", "correction", "slowdown", "oversupply", "stagnant", "bearish"
    ] if term in market_lower)

    if bullish_signals > bearish_signals + 2:
        cycle_position = "GROWTH PHASE"
        cycle_severity = "LOW"
        overall_risk_score += 5
    elif bearish_signals > bullish_signals:
        cycle_position = "CORRECTION PHASE"
        cycle_severity = "HIGH"
        overall_risk_score += 25
    else:
        cycle_position = "STABLE / TRANSITIONING"
        cycle_severity = "MEDIUM"
        overall_risk_score += 15

    risk_factors.append({
        "factor": "Market Cycle Position",
        "severity": cycle_severity,
        "details": f"Current assessment: {cycle_position}",
        "bullish_signals": bullish_signals,
        "bearish_signals": bearish_signals
    })

    # ── Factor 3: Price-per-SqFt Analysis ──
    if size_sqft and size_sqft > 0:
        price_per_sqft = (predicted_price * 100000) / size_sqft

        # City-wise benchmark ranges (INR per sqft)
        benchmarks = {
            'mumbai': (15000, 45000), 'delhi': (8000, 30000),
            'bangalore': (5000, 18000), 'bengaluru': (5000, 18000),
            'hyderabad': (4000, 15000), 'pune': (4000, 14000),
            'chennai': (4000, 14000), 'kolkata': (3000, 10000),
            'ahmedabad': (3000, 10000), 'noida': (4000, 12000),
            'gurgaon': (6000, 20000), 'gurugram': (6000, 20000),
        }
        low, high = benchmarks.get(city.lower(), (3000, 15000))

        if price_per_sqft < low * 0.7 or price_per_sqft > high * 1.3:
            val_severity = "HIGH"
            val_detail = f"₹{int(price_per_sqft)}/sqft is OUTSIDE typical range ₹{low}-₹{high}/sqft"
            overall_risk_score += 20
        elif price_per_sqft < low or price_per_sqft > high:
            val_severity = "MEDIUM"
            val_detail = f"₹{int(price_per_sqft)}/sqft is at the edge of range ₹{low}-₹{high}/sqft"
            overall_risk_score += 10
        else:
            val_severity = "LOW"
            val_detail = f"₹{int(price_per_sqft)}/sqft is within expected range ₹{low}-₹{high}/sqft"
            overall_risk_score += 5
    else:
        val_severity = "UNKNOWN"
        val_detail = "Unable to compute price-per-sqft"
        overall_risk_score += 10

    risk_factors.append({
        "factor": "Valuation Benchmark",
        "severity": val_severity,
        "details": val_detail
    })

    # ── Factor 4: Liquidity Risk ──
    high_liquidity_types = ['apartment', 'flat']
    if property_type.lower() in high_liquidity_types:
        liq_severity = "LOW"
        liq_detail = "Apartments have high resale liquidity"
        overall_risk_score += 5
    else:
        liq_severity = "MEDIUM"
        liq_detail = f"{property_type} properties may take longer to sell"
        overall_risk_score += 15

    risk_factors.append({
        "factor": "Liquidity Risk",
        "severity": liq_severity,
        "details": liq_detail
    })

    # ── Overall Assessment ──
    overall_risk_score = min(100, overall_risk_score)

    if overall_risk_score <= 25:
        overall_level = "LOW RISK"
        recommendation = "Strong investment candidate"
    elif overall_risk_score <= 50:
        overall_level = "MODERATE RISK"
        recommendation = "Viable with due diligence"
    elif overall_risk_score <= 75:
        overall_level = "ELEVATED RISK"
        recommendation = "Proceed with caution; consult advisor"
    else:
        overall_level = "HIGH RISK"
        recommendation = "Not recommended without further analysis"

    return {
        "risk_factors": risk_factors,
        "overall_risk_score": overall_risk_score,
        "overall_risk_level": overall_level,
        "recommendation": recommendation,
        "emi_scenarios": emi_scenarios
    }
