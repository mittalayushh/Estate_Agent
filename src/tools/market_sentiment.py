"""
Market Sentiment Analyzer — Extracts sentiment indicators from RAG context.
"""

import re


def analyze_market_sentiment(market_context: str, city: str) -> dict:
    text = market_context.lower() if market_context else ""

    positive_terms = ["growth", "appreciation", "demand", "rising", "surge", "boom",
        "recovery", "strong", "robust", "opportunity", "premium",
        "infrastructure", "metro", "development", "smart city", "increasing", "positive", "bullish"]
    negative_terms = ["decline", "drop", "slowdown", "oversupply", "stagnation",
        "correction", "risk", "uncertainty", "delay", "sluggish", "falling", "negative", "bearish"]
    neutral_terms = ["stable", "steady", "moderate", "unchanged", "flat", "balanced", "normal"]

    pos_count = sum(1 for t in positive_terms if t in text)
    neg_count = sum(1 for t in negative_terms if t in text)
    neu_count = sum(1 for t in neutral_terms if t in text)
    total = max(pos_count + neg_count + neu_count, 1)
    sentiment_score = ((pos_count - neg_count) / total) * 100

    if sentiment_score > 30:
        sentiment_label, emoji = "BULLISH", "📈"
    elif sentiment_score > 10:
        sentiment_label, emoji = "MODERATELY POSITIVE", "🟢"
    elif sentiment_score > -10:
        sentiment_label, emoji = "NEUTRAL", "⚖️"
    elif sentiment_score > -30:
        sentiment_label, emoji = "MODERATELY NEGATIVE", "🟡"
    else:
        sentiment_label, emoji = "BEARISH", "📉"

    key_metrics = []
    pct_pattern = r'(\d+\.?\d*)\s*(%|percent)'
    percentages = re.findall(pct_pattern, text)
    if percentages:
        key_metrics.append(f"Mentioned growth/change rates: {', '.join([f'{p[0]}%' for p in percentages[:5]])}")

    city_mentions = text.count(city.lower())
    key_metrics.append(f"City-specific data points: {city_mentions} mentions of {city}")

    infra_terms = ["metro", "airport", "highway", "IT corridor", "sez", "smart city", "railway"]
    infra_found = [t for t in infra_terms if t in text]

    demand_terms = ["affordable housing", "luxury", "premium", "mid-segment", "budget"]
    demand_segments = [t for t in demand_terms if t in text]

    if sentiment_label in ["BULLISH", "MODERATELY POSITIVE"]:
        outlook = f"{city} shows positive momentum"
        if infra_found:
            outlook += f", supported by {', '.join(infra_found[:3])}"
        outlook += ". Favorable for investment entry."
    elif sentiment_label == "NEUTRAL":
        outlook = f"{city} market is stable. Suitable for long-term investment."
    else:
        outlook = f"{city} market shows caution signals. Time entry carefully."

    return {
        "sentiment_label": sentiment_label,
        "sentiment_emoji": emoji,
        "sentiment_score": round(sentiment_score, 1),
        "positive_signals": pos_count,
        "negative_signals": neg_count,
        "neutral_signals": neu_count,
        "key_metrics": key_metrics,
        "infrastructure_catalysts": infra_found,
        "demand_segments": demand_segments,
        "data_quality": "HIGH" if len(text) > 2000 else ("MEDIUM" if len(text) > 500 else "LOW"),
        "outlook": outlook
    }
