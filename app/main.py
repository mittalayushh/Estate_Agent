"""
Estate Agent AI — Agent-Centric Premium Streamlit Interface.
Shows agent deployment, working status, and structured AI responses.
"""
import os, sys
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="🏠 Estate Agent AI", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

# ── Premium CSS ──
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--primary:#00ffcc;--primary-glow:rgba(0,255,204,0.4);--bg:#050508;--card:rgba(15,15,25,0.6);--border:rgba(255,255,255,0.08);--text:#f0f0f5;--muted:#9aa0a6;--green:#00d4aa;--amber:#ffc107;--red:#ff3366;}
html,body,.stApp{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);}
.block-container{padding-top:1.5rem;padding-bottom:2rem;}
section[data-testid="stSidebar"]{background:rgba(10,10,15,0.85)!important;backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-right:1px solid var(--border);}

/* Keep Streamlit icons working */
span.material-symbols-rounded,span.material-symbols-outlined,[data-testid="stSidebarCollapsedControl"] span,[data-testid="stExpanderToggleIcon"] span{font-family:"Material Symbols Rounded","Material Symbols Outlined",sans-serif!important;font-style:normal;font-weight:400;line-height:1;letter-spacing:normal;text-transform:none;white-space:nowrap;display:inline-flex;align-items:center;justify-content:center;width:1.25rem;overflow:hidden;}

/* Agent Status Cards */
.agent-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin:20px 0;}
.agent-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px;position:relative;overflow:hidden;transition:all .3s ease;}
.agent-card::before{content:'';position:absolute;top:0;left:0;width:100%;height:3px;background:var(--border);}
.agent-card.deployed::before{background:var(--primary);box-shadow:0 0 15px var(--primary-glow);}
.agent-card.working::before{background:var(--amber);box-shadow:0 0 15px rgba(255,193,7,0.4);animation:glow 1.5s ease-in-out infinite alternate;}
.agent-card.done::before{background:var(--green);box-shadow:0 0 15px rgba(0,212,170,0.4);}
.agent-card .ac-icon{font-size:1.6rem;margin-bottom:8px;}
.agent-card .ac-name{font-family:'Outfit',sans-serif;font-weight:700;font-size:.95rem;color:#fff;margin-bottom:4px;}
.agent-card .ac-status{font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;}
.agent-card .ac-status.standby{color:var(--muted);}
.agent-card .ac-status.active{color:var(--amber);}
.agent-card .ac-status.complete{color:var(--green);}
@keyframes glow{0%{opacity:.6;}100%{opacity:1;}}

/* Metric Row */
.metric-row{display:flex;gap:16px;margin:20px 0;flex-wrap:wrap;}
.metric-card{flex:1;min-width:140px;background:var(--card);backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:14px;padding:20px 14px;text-align:center;transition:all .4s cubic-bezier(.175,.885,.32,1.275);position:relative;overflow:hidden;}
.metric-card:hover{transform:translateY(-4px);border-color:var(--primary);box-shadow:0 8px 25px var(--primary-glow);}
.metric-card .mc-icon{font-size:1.5rem;margin-bottom:6px;display:inline-block;}
.metric-card .mc-value{color:#fff;font-size:1.4rem;font-weight:800;font-family:'Outfit',sans-serif;}
.metric-card .mc-label{color:var(--primary);font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;margin-top:4px;}

/* Dividers & Headers */
.neon-divider{height:1px;background:linear-gradient(90deg,transparent,var(--primary),transparent);margin:20px 0 28px;opacity:.4;box-shadow:0 0 8px var(--primary);}
.sec-header{font-family:'Outfit',sans-serif;font-size:1.2rem;font-weight:700;color:#fff;margin-bottom:16px;display:flex;align-items:center;gap:10px;}
.sec-header .dot{width:8px;height:8px;border-radius:50%;background:var(--primary);box-shadow:0 0 10px var(--primary);animation:pulse 2s infinite;}
@keyframes pulse{0%{box-shadow:0 0 0 0 var(--primary-glow);}70%{box-shadow:0 0 0 8px rgba(0,255,204,0);}100%{box-shadow:0 0 0 0 rgba(0,255,204,0);}}

/* Sidebar */
.sb-brand{text-align:center;padding:16px 0 8px;}
.sb-brand .sb-icon{font-size:2.2rem;filter:drop-shadow(0 0 12px var(--primary));}
.sb-brand .sb-name{font-size:1.6rem;font-weight:900;letter-spacing:3px;text-transform:uppercase;background:linear-gradient(135deg,#fff,var(--primary));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.sb-brand .sb-ver{font-size:.7rem;color:var(--muted);letter-spacing:2px;margin-top:2px;}
.sb-section{font-size:.7rem;font-weight:700;color:var(--primary);text-transform:uppercase;letter-spacing:2px;margin:20px 0 10px;display:flex;align-items:center;gap:8px;}
.sb-section::after{content:'';flex-grow:1;height:1px;background:linear-gradient(90deg,var(--border),transparent);}

/* Welcome */
.welcome{background:var(--card);backdrop-filter:blur(16px);border:1px solid var(--border);border-radius:18px;padding:36px 28px;text-align:center;margin-top:16px;box-shadow:0 8px 35px rgba(0,0,0,.2);animation:float 6s ease-in-out infinite;}
@keyframes float{0%{transform:translateY(0);}50%{transform:translateY(-8px);}100%{transform:translateY(0);}}
.welcome .wc-icon{font-size:3rem;margin-bottom:12px;}
.welcome .wc-title{font-size:1.3rem;font-weight:800;color:#fff;margin-bottom:10px;}
.welcome .wc-text{font-size:.9rem;color:var(--muted);line-height:1.7;}
.welcome .wc-badge{display:inline-block;padding:5px 12px;background:rgba(0,255,204,.1);border-radius:20px;border:1px solid rgba(0,255,204,.2);font-size:.75rem;color:var(--primary);margin-top:16px;font-weight:600;}

/* Buttons */
.stButton>button[kind="primary"]{background:rgba(0,255,204,.05)!important;color:var(--primary)!important;font-weight:800!important;font-family:'Outfit',sans-serif!important;letter-spacing:2px!important;border:1px solid var(--primary)!important;border-radius:8px!important;text-transform:uppercase;box-shadow:0 0 12px rgba(0,255,204,.1)!important;min-height:52px!important;transition:all .3s!important;}
.stButton>button[kind="primary"] p{color:inherit!important;}
.stButton>button[kind="primary"]:hover{background:var(--primary)!important;color:#050508!important;box-shadow:0 0 25px rgba(0,255,204,.5)!important;transform:translateY(-2px)!important;}
.stDownloadButton>button{background:rgba(0,255,204,.05)!important;color:var(--primary)!important;font-weight:700!important;border:1px solid var(--primary)!important;border-radius:8px!important;text-transform:uppercase;letter-spacing:1.5px!important;min-height:48px!important;transition:all .3s!important;}
.stDownloadButton>button p{color:inherit!important;}
.stDownloadButton>button:hover{background:var(--primary)!important;color:#050508!important;}

/* AI Response Block */
.ai-response{background:rgba(0,255,204,.03);border:1px solid rgba(0,255,204,.1);border-radius:12px;padding:24px;margin:12px 0;position:relative;}
.ai-response::before{content:'🤖 AI';position:absolute;top:-10px;left:16px;background:var(--bg);padding:0 8px;font-size:.7rem;font-weight:700;color:var(--primary);letter-spacing:1.5px;text-transform:uppercase;}

/* Hide chrome */
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
</style>""", unsafe_allow_html=True)

# ── Agent Definitions ──
AGENTS = [
    {"id": "validator", "icon": "🛡️", "name": "Input Validator", "desc": "Normalizes & validates property data"},
    {"id": "valuator", "icon": "💰", "name": "Price Predictor", "desc": "XGBoost ML valuation engine"},
    {"id": "researcher", "icon": "📚", "name": "Market Researcher", "desc": "RAG-powered market intelligence"},
    {"id": "comparator", "icon": "🏘️", "name": "Comparable Analyst", "desc": "Property variation analysis"},
    {"id": "risk_mgr", "icon": "⚠️", "name": "Risk Assessor", "desc": "Multi-factor risk simulation"},
    {"id": "advisor", "icon": "🧠", "name": "Investment Advisor", "desc": "LLM advisory synthesis"},
    {"id": "qa", "icon": "✅", "name": "Quality Auditor", "desc": "Report completeness check"},
]

NODE_TO_AGENT = {"validate": 0, "valuation": 1, "research": 2, "comparable": 3, "risk": 4, "advisory": 5, "quality_check": 6}

@st.cache_resource
def load_agent():
    from src.agents.graph import app
    return app

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

def render_agent_grid(agent_states):
    """Renders the 7 agent status cards."""
    cols = st.columns(len(AGENTS))
    for i, (col, agent) in enumerate(zip(cols, AGENTS)):
        state = agent_states.get(i, "standby")
        css_class = "deployed" if state == "standby" else ("working" if state == "working" else "done")
        status_label = "🔵 DEPLOYED" if state == "standby" else ("🟡 WORKING..." if state == "working" else "🟢 COMPLETE")
        status_css = "standby" if state == "standby" else ("active" if state == "working" else "complete")
        with col:
            st.markdown(f"""<div class="agent-card {css_class}">
                <div class="ac-icon">{agent['icon']}</div>
                <div class="ac-name">{agent['name']}</div>
                <div class="ac-status {status_css}">{status_label}</div>
            </div>""", unsafe_allow_html=True)

def main():
    # ═══ SIDEBAR ═══
    with st.sidebar:
        st.markdown("""<div class="sb-brand"><div class="sb-icon">🏠</div>
            <div class="sb-name">Estate Agent</div><div class="sb-ver">Agentic AI · v2.0</div></div>""", unsafe_allow_html=True)

        st.markdown('<div class="sb-section">🏗️ Property Details</div>', unsafe_allow_html=True)
        city = st.selectbox("City", list(CITY_STATE_MAP.keys()), index=0)
        state_val = CITY_STATE_MAP[city]
        st.caption(f"State: **{state_val}**")
        prop_type = st.selectbox("Property Type", ["Apartment", "Independent House", "Villa", "Plot"])
        c1, c2 = st.columns(2)
        with c1: bhk = st.selectbox("BHK", [1, 2, 3, 4, 5], index=1)
        with c2: bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)
        size_sqft = st.number_input("Size (sq ft)", min_value=200, max_value=10000, value=1500, step=50)
        furnished = st.selectbox("Furnished Status", ["Semi-furnished", "Fully furnished", "Unfurnished"])
        c3, c4 = st.columns(2)
        with c3: facing = st.selectbox("Facing", ["East", "North", "West", "South", "North-East", "South-East"])
        with c4: security = st.selectbox("Security", ["Yes", "No"])
        transport = st.selectbox("Public Transport", ["High", "Medium", "Low"])

        st.markdown('<div class="sb-section">💼 Investor Preferences</div>', unsafe_allow_html=True)
        c5, c6 = st.columns(2)
        with c5: budget_min = st.number_input("Min Budget (₹L)", min_value=0, max_value=5000, value=50, step=10)
        with c6: budget_max = st.number_input("Max Budget (₹L)", min_value=0, max_value=5000, value=200, step=10)
        horizon = st.slider("Investment Horizon (years)", 1, 15, 5)
        risk_appetite = st.selectbox("Risk Appetite", ["Conservative", "Moderate", "Aggressive"])
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀  GENERATE ADVISORY", type="primary", use_container_width=True)

    # ═══ HEADER ═══
    st.markdown("""<div style="display:flex;align-items:center;gap:14px;margin-bottom:6px;">
        <div style="font-size:2.5rem;filter:drop-shadow(0 0 10px rgba(0,255,204,.5));">🏠</div>
        <div><div style="font-size:2.2rem;font-weight:900;font-family:'Outfit',sans-serif;letter-spacing:2px;
            background:linear-gradient(135deg,#fff,var(--primary));-webkit-background-clip:text;-webkit-text-fill-color:transparent;
            text-transform:uppercase;line-height:1.2;">Estate Agent AI</div>
        <div style="color:var(--muted);font-size:.95rem;">Agentic AI Real Estate Investment Advisory System</div></div>
    </div>""", unsafe_allow_html=True)

    if not analyze_btn:
        # ═══ STANDBY: Show deployed agents ═══
        st.markdown('<div class="sec-header"><span class="dot"></span> Agents Deployed</div>', unsafe_allow_html=True)
        render_agent_grid({i: "standby" for i in range(7)})
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        st.markdown("""<div class="welcome"><div class="wc-icon">🏠</div>
            <div class="wc-title">Multi-Agent System Ready</div>
            <div class="wc-text">7 specialized AI agents are deployed and awaiting your query.<br>
            Configure property details in the sidebar and click <strong>Generate Advisory</strong> to activate the autonomous pipeline.<br><br>
            <strong>🛡️ Validate → 💰 Valuate → 📚 Research → 🏘️ Compare → ⚠️ Assess Risk → 🧠 Advise → ✅ Audit</strong></div>
            <div class="wc-badge">✨ Powered by LangGraph · XGBoost · ChromaDB RAG · Groq LLM</div></div>""", unsafe_allow_html=True)
        return

    # ═══ RUNNING PIPELINE ═══
    property_input = {
        'Property_Type': prop_type, 'BHK': bhk, 'Furnished_Status': furnished,
        'Size_in_SqFt': size_sqft, 'Bathrooms': bathrooms,
        'Public_Transport_Accessibility': transport, 'Facing': facing,
        'Security': security, 'City': city, 'State': state_val
    }
    user_preferences = {'budget_min': budget_min, 'budget_max': budget_max,
                        'investment_horizon': horizon, 'risk_appetite': risk_appetite}
    inputs = {"property_input": property_input, "user_preferences": user_preferences, "market_context": []}

    # Agent Status Header
    st.markdown('<div class="sec-header"><span class="dot"></span> Agent Orchestration — Live</div>', unsafe_allow_html=True)
    agent_status_placeholder = st.empty()
    agent_states = {i: "standby" for i in range(7)}

    # Show all agents as deployed
    with agent_status_placeholder.container():
        render_agent_grid(agent_states)

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    # Pipeline execution with live agent updates
    agent_app = load_agent()
    final_state = None
    log_container = st.container()

    with log_container:
        with st.status("🧠 Orchestrating 7-agent advisory pipeline...", expanded=True) as status:
            try:
                for output in agent_app.stream(inputs):
                    for key, value in output.items():
                        step = value.get("current_step", key)
                        idx = NODE_TO_AGENT.get(key, -1)

                        # Update agent states
                        if idx >= 0:
                            # Mark previous agents as done
                            for j in range(idx):
                                agent_states[j] = "done"
                            agent_states[idx] = "working"

                        with agent_status_placeholder.container():
                            render_agent_grid(agent_states)

                        # Show step log
                        agent_name = AGENTS[idx]['name'] if idx >= 0 else key
                        agent_icon = AGENTS[idx]['icon'] if idx >= 0 else "🔧"
                        st.write(f"{agent_icon} **{agent_name}** → {step}")

                        if idx >= 0:
                            agent_states[idx] = "done"

                        final_state = {**inputs, **(final_state or {}), **value}

                # Mark all done
                for i in range(7):
                    agent_states[i] = "done"
                with agent_status_placeholder.container():
                    render_agent_grid(agent_states)

                status.update(label="✅ All 7 agents completed successfully!", state="complete")
            except Exception as e:
                status.update(label=f"❌ Pipeline error: {str(e)}", state="error")
                st.error(f"Error: {str(e)}")
                return

    if not final_state:
        st.error("No output from pipeline.")
        return

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    # ═══ METRICS ═══
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

    st.markdown(f"""<div class="metric-row">
        <div class="metric-card"><div class="mc-icon">💰</div><div class="mc-value">₹{predicted_price:.1f}L</div><div class="mc-label">Predicted Price</div></div>
        <div class="metric-card"><div class="mc-icon">📍</div><div class="mc-value">{city}</div><div class="mc-label">Location</div></div>
        <div class="metric-card"><div class="mc-icon">🎯</div><div class="mc-value">{confidence:.0%}</div><div class="mc-label">Model Confidence</div></div>
        <div class="metric-card"><div class="mc-icon">{sentiment_emoji}</div><div class="mc-value" style="font-size:1rem;">{sentiment_label}</div><div class="mc-label">Market Sentiment</div></div>
        <div class="metric-card" style="border-color:{risk_color};"><div class="mc-icon">{risk_icon}</div><div class="mc-value" style="color:{risk_color};font-size:1rem;">{risk_level}</div><div class="mc-label">Risk ({risk_score}/100)</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    # ═══ AI ADVISORY REPORT (Tabbed) ═══
    st.markdown('<div class="sec-header"><span class="dot"></span> AI Advisory Report</div>', unsafe_allow_html=True)

    sections = final_state.get("report_sections", {})
    if sections:
        tab_names = list(sections.keys())
        tabs = st.tabs(tab_names)
        for tab, key in zip(tabs, tab_names):
            with tab:
                st.markdown(f'<div class="ai-response">{sections[key]}</div>', unsafe_allow_html=True)
    else:
        report_text = final_state.get("final_advisory", "No report generated.")
        st.markdown(f'<div class="ai-response">{report_text}</div>', unsafe_allow_html=True)

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    # ═══ COMPARABLE PROPERTIES ═══
    comps = final_state.get("comparable_properties", [])
    if comps:
        st.markdown('<div class="sec-header"><span class="dot"></span> Comparable Properties Analysis</div>', unsafe_allow_html=True)
        import pandas as pd
        comp_df = pd.DataFrame(comps)
        comp_df.columns = ["Variant", "BHK", "Size (sqft)", "Furnished", "Price (₹L)", "Diff %", "Diff (₹L)"]
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

    # ═══ EMI SCENARIOS ═══
    emi = risk.get("emi_scenarios", {})
    if emi:
        st.markdown('<div class="sec-header"><span class="dot"></span> EMI Scenarios (80% LTV, 20yr tenure)</div>', unsafe_allow_html=True)
        import pandas as pd
        emi_df = pd.DataFrame([{"Interest Rate": r, "Monthly EMI": f"₹{v}K"} for r, v in emi.items()])
        st.dataframe(emi_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    # ═══ PDF EXPORT ═══
    try:
        from src.tools.report_generator import generate_pdf
        pdf_bytes = generate_pdf(report_text=final_state.get("final_advisory", ""),
            property_data=property_input, comparables=comps, risk_data=risk)
        if isinstance(pdf_bytes, bytes):
            st.download_button(label="📥  DOWNLOAD PDF REPORT", data=pdf_bytes,
                file_name="Estate_Agent_Advisory.pdf", mime="application/pdf", use_container_width=True)
    except Exception as e:
        st.warning(f"PDF export unavailable: {e}")

    # ═══ AGENT TRACE ═══
    with st.expander("🧠 Agent Reasoning Trace (Debug)"):
        for step in final_state.get("agent_trace", []):
            st.markdown(f"- {step}")

    with st.expander("📄 Raw Report Output"):
        st.code(final_state.get("final_advisory", ""), language="markdown")

if __name__ == "__main__":
    main()
