"""
Estate Agent AI — Premium Streamlit Interface.

A glassmorphism dark-mode UI for the Agentic AI Real Estate Advisory system.
Features: property input, metric cards, 5-tab report, PDF export, agent trace.
"""

import os
import sys

# ── Environment fixes for deployment ──
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

# Path fix for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page Config ──
st.set_page_config(
    page_title="🏠 Estate Agent AI — Investment Advisory",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #00ffcc;
        --primary-glow: rgba(0, 255, 204, 0.4);
        --secondary: #7b2cbf;
        --bg-color: #050508;
        --card-bg: rgba(15, 15, 25, 0.6);
        --card-border: rgba(255, 255, 255, 0.08);
        --text-main: #f0f0f5;
        --text-muted: #9aa0a6;
    }

    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-main);
    }

    /* Keep Streamlit icon glyphs intact */
    span.material-symbols-rounded,
    span.material-symbols-outlined,
    [data-testid="stSidebarCollapsedControl"] span,
    [data-testid="stExpanderToggleIcon"] span {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", sans-serif !important;
        font-style: normal; font-weight: 400; line-height: 1;
        letter-spacing: normal; text-transform: none; white-space: nowrap;
        display: inline-flex; align-items: center; justify-content: center;
        width: 1.25rem; overflow: hidden;
    }

    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10, 10, 15, 0.8) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid var(--card-border);
    }
    section[data-testid="stSidebar"] .stMarkdown { color: var(--text-main); }

    /* Metric Cards */
    .metric-row { display: flex; gap: 20px; margin-bottom: 24px; flex-wrap: wrap; }
    .metric-card {
        flex: 1; min-width: 150px;
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--card-border);
        border-radius: 16px; padding: 24px 16px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative; overflow: hidden;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    .metric-card::before {
        content: ''; position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 100%);
        pointer-events: none;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary);
        box-shadow: 0 8px 30px var(--primary-glow);
    }
    .metric-card .mc-icon { font-size: 1.8rem; margin-bottom: 8px; display: inline-block; filter: drop-shadow(0 0 8px rgba(255,255,255,0.2)); }
    .metric-card .mc-value { color: var(--text-main); font-size: 1.6rem; font-weight: 800; font-family: 'Outfit', sans-serif; text-shadow: 0 0 10px rgba(255,255,255,0.1); }
    .metric-card .mc-label { color: var(--primary); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 6px; }

    /* Neon Divider */
    .green-divider { height: 1px; background: linear-gradient(90deg, transparent, var(--primary), transparent); margin: 24px 0 32px 0; border: none; opacity: 0.5; box-shadow: 0 0 10px var(--primary); }

    /* Section Header */
    .section-header { font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 700; color: #fff; letter-spacing: 0.5px; margin-bottom: 20px; display: flex; align-items: center; gap: 12px; }
    .section-header .sh-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--primary); display: inline-block; box-shadow: 0 0 12px var(--primary); animation: pulse 2s infinite; }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 var(--primary-glow); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 204, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
    }

    /* Sidebar Branding */
    .sidebar-brand { text-align: center; padding: 20px 0 10px 0; }
    .sidebar-brand .sb-icon { font-size: 2.5rem; filter: drop-shadow(0 0 15px var(--primary)); margin-bottom: 5px; }
    .sidebar-brand .sb-name { font-size: 1.8rem; font-weight: 900; color: #fff; letter-spacing: 3px; text-transform: uppercase; background: linear-gradient(135deg, #fff, var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .sidebar-brand .sb-version { font-size: 0.75rem; color: var(--text-muted); letter-spacing: 2px; margin-top: 4px; }

    /* Sidebar Section Labels */
    .sidebar-section { font-size: 0.75rem; font-weight: 700; color: var(--primary); text-transform: uppercase; letter-spacing: 2px; margin-top: 24px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
    .sidebar-section::after { content: ''; flex-grow: 1; height: 1px; background: linear-gradient(90deg, var(--card-border), transparent); }

    /* Welcome Card */
    .welcome-card { background: var(--card-bg); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid var(--card-border); border-radius: 20px; padding: 40px 30px; text-align: center; margin-top: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); animation: float 6s ease-in-out infinite; }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
    .welcome-card .wc-icon { font-size: 3.5rem; margin-bottom: 16px; filter: drop-shadow(0 0 20px rgba(255,255,255,0.2)); }
    .welcome-card .wc-title { font-size: 1.4rem; font-weight: 800; color: #fff; margin-bottom: 12px; letter-spacing: 1px; }
    .welcome-card .wc-text { font-size: 0.95rem; color: var(--text-muted); line-height: 1.7; }
    .welcome-card .wc-hint { display: inline-block; padding: 6px 12px; background: rgba(0, 255, 204, 0.1); border-radius: 20px; border: 1px solid rgba(0, 255, 204, 0.2); font-size: 0.8rem; color: var(--primary); margin-top: 20px; font-weight: 600; }

    /* Button Overrides */
    .stButton > button[kind="primary"] {
        background: rgba(0, 255, 204, 0.05) !important;
        color: var(--primary) !important;
        font-weight: 800 !important; font-family: 'Outfit', sans-serif !important;
        letter-spacing: 2px !important;
        border: 1px solid var(--primary) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.1), inset 0 0 10px rgba(0, 255, 204, 0.05) !important;
        min-height: 54px !important;
    }
    .stButton > button[kind="primary"] p { color: inherit !important; }
    .stButton > button[kind="primary"]:hover {
        background: var(--primary) !important;
        color: #050508 !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5), inset 0 0 15px rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    .stDownloadButton > button {
        background: rgba(0, 255, 204, 0.05) !important;
        color: var(--primary) !important;
        font-weight: 700 !important; font-family: 'Outfit', sans-serif !important;
        border: 1px solid var(--primary) !important;
        border-radius: 8px !important;
        text-transform: uppercase; letter-spacing: 1.5px !important;
        transition: all 0.3s ease !important;
        min-height: 50px !important;
    }
    .stDownloadButton > button p { color: inherit !important; }
    .stDownloadButton > button:hover {
        background: var(--primary) !important;
        color: #050508 !important;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4) !important;
    }

    /* Inputs Styling */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background-color: rgba(0,0,0,0.2) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important; color: #fff !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--card-bg) !important;
        border-radius: 8px !important;
        border: 1px solid var(--card-border) !important;
        font-weight: 600 !important; color: #fff !important;
    }

    /* Status */
    [data-testid="stStatusWidget"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
    }

    /* Hide chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Cache the graph ──
@st.cache_resource
def load_agent():
    from src.agents.graph import app
    return app


# ── City-State Mapping ──
CITY_STATE_MAP = {
    "Mumbai": "Maharashtra", "Pune": "Maharashtra", "Thane": "Maharashtra",
    "Delhi": "Delhi", "Noida": "Uttar Pradesh", "Gurgaon": "Haryana",
    "Bangalore": "Karnataka", "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana", "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal", "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan", "Lucknow": "Uttar Pradesh",
    "Chandigarh": "Punjab", "Kochi": "Kerala",
    "Indore": "Madhya Pradesh", "Nagpur": "Maharashtra",
}


def main():
    # ═══════════════════════════════════════
    # SIDEBAR — Control Panel
    # ═══════════════════════════════════════
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-brand">
                <div class="sb-icon">🏠</div>
                <div class="sb-name">Estate Agent</div>
                <div class="sb-version">AI Advisory · v2.0</div>
            </div>
        """, unsafe_allow_html=True)

        # ── Property Details ──
        st.markdown('<div class="sidebar-section">🏗️ Property Details</div>', unsafe_allow_html=True)

        city = st.selectbox("City", list(CITY_STATE_MAP.keys()), index=0)
        state_val = CITY_STATE_MAP[city]
        st.caption(f"State: **{state_val}**")

        prop_type = st.selectbox("Property Type", ["Apartment", "Independent House", "Villa", "Plot"])

        c1, c2 = st.columns(2)
        with c1:
            bhk = st.selectbox("BHK", [1, 2, 3, 4, 5], index=1)
        with c2:
            bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)

        size_sqft = st.number_input("Size (sq ft)", min_value=200, max_value=10000, value=1500, step=50)
        furnished = st.selectbox("Furnished Status", ["Semi-furnished", "Fully furnished", "Unfurnished"])

        c3, c4 = st.columns(2)
        with c3:
            facing = st.selectbox("Facing", ["East", "North", "West", "South", "North-East", "South-East"])
        with c4:
            security = st.selectbox("Security", ["Yes", "No"])

        transport = st.selectbox("Public Transport", ["High", "Medium", "Low"])

        # ── Investor Preferences ──
        st.markdown('<div class="sidebar-section">💼 Investor Preferences</div>', unsafe_allow_html=True)

        c5, c6 = st.columns(2)
        with c5:
            budget_min = st.number_input("Min Budget (₹L)", min_value=0, max_value=5000, value=50, step=10)
        with c6:
            budget_max = st.number_input("Max Budget (₹L)", min_value=0, max_value=5000, value=200, step=10)

        horizon = st.slider("Investment Horizon (years)", 1, 15, 5)
        risk_appetite = st.selectbox("Risk Appetite", ["Conservative", "Moderate", "Aggressive"])

        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀  GENERATE ADVISORY", type="primary", use_container_width=True)

    # ═══════════════════════════════════════
    # MAIN PANEL — Header
    # ═══════════════════════════════════════
    st.markdown("""
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:10px;">
            <div style="font-size:2.8rem; filter: drop-shadow(0 0 10px rgba(0,255,204,0.5));">🏠</div>
            <div>
                <div style="font-size:2.4rem; font-weight:900; font-family:'Outfit', sans-serif; letter-spacing:2px;
                    background: linear-gradient(135deg, #ffffff, var(--primary));
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    text-transform: uppercase; line-height: 1.2;">Estate Agent AI</div>
                <div style="color:var(--text-muted); font-size:1rem; font-weight:500;">
                    Agentic AI Real Estate Investment Advisory System
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # ANALYSIS
    # ═══════════════════════════════════════
    if analyze_btn:
        # Build inputs
        property_input = {
            'Property_Type': prop_type,
            'BHK': bhk,
            'Furnished_Status': furnished,
            'Size_in_SqFt': size_sqft,
            'Bathrooms': bathrooms,
            'Public_Transport_Accessibility': transport,
            'Facing': facing,
            'Security': security,
            'City': city,
            'State': state_val
        }

        user_preferences = {
            'budget_min': budget_min,
            'budget_max': budget_max,
            'investment_horizon': horizon,
            'risk_appetite': risk_appetite
        }

        inputs = {
            "property_input": property_input,
            "user_preferences": user_preferences,
            "market_context": []
        }

        # ── Run Pipeline ──
        st.markdown('<div class="section-header"><span class="sh-dot"></span> AI Processing Pipeline</div>', unsafe_allow_html=True)

        agent_app = load_agent()
        final_state = None

        with st.status("🧠 Running 7-node advisory pipeline...", expanded=True) as status:
            try:
                for output in agent_app.stream(inputs):
                    for key, value in output.items():
                        step = value.get("current_step", key)
                        st.write(f"✅ **{key}** → {step}")
                        final_state = {**inputs, **(final_state or {}), **value}
                status.update(label="✅ Advisory pipeline complete!", state="complete")
            except Exception as e:
                status.update(label=f"❌ Pipeline error: {str(e)}", state="error")
                st.error(f"Error: {str(e)}")
                return

        if not final_state:
            st.error("No output from pipeline.")
            return

        st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

        # ── Metric Cards ──
        predicted_price = final_state.get("predicted_price", 0)
        confidence = final_state.get("confidence_score", 0)
        sentiment = final_state.get("market_sentiment", {})
        risk = final_state.get("risk_assessment", {})

        sentiment_label = sentiment.get("sentiment_label", "N/A")
        sentiment_emoji = sentiment.get("sentiment_emoji", "📊")
        risk_level = risk.get("overall_risk_level", "N/A")
        risk_score = risk.get("overall_risk_score", 0)

        risk_color = "#00ffcc" if risk_score <= 25 else ("#ffc107" if risk_score <= 50 else "#ff3366")
        risk_icon = "🟢" if risk_score <= 25 else ("🟡" if risk_score <= 50 else "🔴")

        st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card">
                    <div class="mc-icon">💰</div>
                    <div class="mc-value">₹{predicted_price:.1f}L</div>
                    <div class="mc-label">Predicted Price</div>
                </div>
                <div class="metric-card">
                    <div class="mc-icon">📍</div>
                    <div class="mc-value">{city}</div>
                    <div class="mc-label">Location</div>
                </div>
                <div class="metric-card">
                    <div class="mc-icon">🎯</div>
                    <div class="mc-value">{confidence:.0%}</div>
                    <div class="mc-label">Confidence</div>
                </div>
                <div class="metric-card">
                    <div class="mc-icon">{sentiment_emoji}</div>
                    <div class="mc-value" style="font-size:1.1rem;">{sentiment_label}</div>
                    <div class="mc-label">Market Sentiment</div>
                </div>
                <div class="metric-card" style="border-color:{risk_color};">
                    <div class="mc-icon">{risk_icon}</div>
                    <div class="mc-value" style="color:{risk_color}; font-size:1.1rem;">{risk_level}</div>
                    <div class="mc-label">Risk Level ({risk_score}/100)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

        # ── Report Tabs ──
        st.markdown('<div class="section-header"><span class="sh-dot"></span> Investment Advisory Report</div>', unsafe_allow_html=True)

        sections = final_state.get("report_sections", {})
        if sections:
            tab_names = list(sections.keys())
            tabs = st.tabs(tab_names)
            for tab, key in zip(tabs, tab_names):
                with tab:
                    st.markdown(sections[key])
        else:
            st.markdown(final_state.get("final_advisory", "No report generated."))

        st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

        # ── Comparable Properties Table ──
        comps = final_state.get("comparable_properties", [])
        if comps:
            st.markdown('<div class="section-header"><span class="sh-dot"></span> Comparable Properties</div>', unsafe_allow_html=True)
            import pandas as pd
            comp_df = pd.DataFrame(comps)
            comp_df.columns = ["Variant", "BHK", "Size (sqft)", "Furnished", "Price (₹L)", "Diff %", "Diff (₹L)"]
            st.dataframe(comp_df, use_container_width=True, hide_index=True)

        st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

        # ── EMI Scenarios ──
        emi = risk.get("emi_scenarios", {})
        if emi:
            st.markdown('<div class="section-header"><span class="sh-dot"></span> EMI Scenarios (80% LTV, 20yr)</div>', unsafe_allow_html=True)
            import pandas as pd
            emi_df = pd.DataFrame([
                {"Interest Rate": rate, "Monthly EMI": f"₹{val}K"}
                for rate, val in emi.items()
            ])
            st.dataframe(emi_df, use_container_width=True, hide_index=True)

        st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

        # ── PDF Export ──
        try:
            from src.tools.report_generator import generate_pdf
            pdf_bytes = generate_pdf(
                report_text=final_state.get("final_advisory", ""),
                property_data=property_input,
                comparables=comps,
                risk_data=risk
            )
            if isinstance(pdf_bytes, bytes):
                st.download_button(
                    label="📥  EXPORT PDF ADVISORY REPORT",
                    data=pdf_bytes,
                    file_name="Estate_Agent_Advisory.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.info("PDF generation requires reportlab. Install with: pip install reportlab")
        except Exception as e:
            st.warning(f"PDF export unavailable: {e}")

        # ── Agent Trace ──
        with st.expander("🧠 Agent Reasoning Trace"):
            trace = final_state.get("agent_trace", [])
            for step in trace:
                st.markdown(f"- {step}")

        # ── Raw Report ──
        with st.expander("📄 Full Report (Raw)"):
            st.code(final_state.get("final_advisory", ""), language="markdown")

    else:
        # ── Welcome Card ──
        st.markdown("""
            <div class="welcome-card">
                <div class="wc-icon">🏠</div>
                <div class="wc-title">System Standby</div>
                <div class="wc-text">
                    Configure property details and investor preferences in the control panel.
                    The AI advisory system will run a 7-node autonomous pipeline:<br><br>
                    <strong>Validate → Valuate → Research → Compare → Assess Risk → Advise → Quality Check</strong>
                </div>
                <div class="wc-hint">✨ Powered by LangGraph · XGBoost · ChromaDB RAG · GPT-4o-mini</div>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
