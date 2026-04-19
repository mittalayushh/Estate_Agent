import streamlit as st
import time

# Premium page config
st.set_page_config(
    page_title="Agentic Real Estate Advisor",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Styling for the hero section */
    .hero-container {
        padding: 3rem;
        background: linear-gradient(135deg, #09203f 0%, #537895 100%);
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        opacity: 0.9;
        font-weight: 300;
    }
    /* Style tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-size: 1.1rem;
    }
    .stTabs [aria-selected="true"] {
        color: #09203f !important;
        font-weight: bold;
    }
    /* Style metric cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.05);
    }
    /* Style disclaimer */
    .disclaimer {
        padding: 1.5rem;
        background-color: #fffbeb;
        border-left: 6px solid #fbbf24;
        color: #92400e;
        border-radius: 8px;
        font-size: 0.95rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR INPUTS -----------------
st.sidebar.markdown(
    """<div style='text-align: center;'><img src='https://img.icons8.com/color/96/000000/real-estate.png' width='80'></div>""", 
    unsafe_allow_html=True
)
st.sidebar.title("Property Details")
st.sidebar.markdown("Provide details for AI-driven valuation & advisory.")

with st.sidebar.form("property_form"):
    st.subheader("Location")
    col1, col2 = st.columns(2)
    with col1:
        state = st.text_input("State", value="Maharashtra")
    with col2:
        city = st.text_input("City", value="Mumbai")

    st.subheader("Basics")
    prop_type = st.selectbox("Property Type", ["Apartment", "Independent Floor", "Independent House", "Villa"])
    bhk = st.number_input("BHK", min_value=1, max_value=10, value=2)
    size_sqft = st.number_input("Size (Sq.Ft)", min_value=100, max_value=10000, value=1200)
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)

    st.subheader("Features")
    furnishing = st.selectbox("Furnished Status", ["Furnished", "Semi-Furnished", "Unfurnished"])
    transport = st.selectbox("Public Transport Access", ["High", "Medium", "Low"])
    facing = st.selectbox("Facing", ["North", "South", "East", "West", "North-East"])
    security = st.selectbox("Security", ["Gated Community", "Basic", "None"])

    submit_button = st.form_submit_button("Generate Advisory Report", type="primary", use_container_width=True)

# ----------------- MAIN LAYOUT -----------------

if not submit_button:
    # Empty State / Hero Screen
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Agentic Real Estate Advisory</div>
            <div class="hero-subtitle">Autonomous reasoning for property valuation and investment insights</div>
        </div>
    """, unsafe_allow_html=True)

    st.info("👈 Enter the property details in the sidebar and click **Generate Advisory Report** to begin the AI analysis.")
    
    st.write("---")
    
    # Placeholder images / graphics for premium look
    cols = st.columns(3)
    with cols[0]:
        st.markdown("### 🎯 Accuracy<br><span style='color:gray;font-size:1em'>Powered by trained ML Regressors</span>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown("### 📚 Context<br><span style='color:gray;font-size:1em'>Live RAG search of regional trends</span>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown("### 🤖 Reasoning<br><span style='color:gray;font-size:1em'>Multi-step logic for investment advice</span>", unsafe_allow_html=True)

else:
    # Action Triggered - Show Loading & Mock Report
    progress_bar = st.progress(0)
    status_text = st.empty()

    steps = [
        "Agent initializing workflow...",
        "Running ML valuation models...",
        f"Searching RERA and market reports for {city}...",
        "Synthesizing final advisory response..."
    ]

    for i, step in enumerate(steps):
        status_text.text(step)
        time.sleep(0.8)
        progress_bar.progress((i + 1) * 25)
    
    status_text.empty()
    progress_bar.empty()
    st.success("Analysis Complete!")

    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h2 style="margin-bottom: 0px; color: #09203f;">Property Assessment: {bhk} BHK {prop_type} in {city}</h2>
            <span style="color:gray;">Generated by Agentic Workflow • {size_sqft} sq.ft • {furnishing}</span>
        </div>
    """, unsafe_allow_html=True)

    # 1. Summary Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Predicted Market Value", value="₹1.45 Cr", delta="↑ 4.2% YoY locally")
    col2.metric(label="Rental Yield Estimate", value="3.8%", delta="-0.2% vs City avg", delta_color="inverse")
    col3.metric(label="Agent Confidence", value="High", delta="Based on 45 Comps")

    st.write("---")

    # Expandable Tabs for Detailed Output
    tab1, tab2, tab3 = st.tabs(["📝 Summary View", "📊 Market Comps", "💼 Action Plan"])

    with tab1:
        st.subheader("1. Property Valuation & Market View")
        st.markdown(f"""
        **Valuation Rationale:**
        Based on our internal ML model evaluations, the base price for a **{size_sqft} sq.ft** {prop_type.lower()} with '{security}' security in **{city}** is approximately **₹1.45 Cr**. This pricing heavily weights the '{transport}' public transport connectivity which is a premium factor in {city}.

        **Market Context (RAG Insights):**
        * The {city} real estate market has seen a steady surge in demand for {bhk} BHK units over the last 3 quarters. 
        * Recent policy shifts related to RERA guidelines in {state} have improved developer accountability, driving up buyer trust.
        * Interest rates and home loan incentives are keeping suburban investments highly attractive.
        """)

    with tab2:
        st.subheader("2. Comparable Property Analysis")
        st.markdown("""
        The agent retrieved the following similar transactions within a 5 km radius over the last 6 months:
        """)
        st.dataframe({
            "Property": [f"Project Alpha ({bhk} BHK)", "Ozone Residences", "Vertex Tower"],
            "Similarity Score": ["94%", "88%", "82%"],
            "Distance": ["1.2 km", "3.0 km", "0.5 km"],
            "Price": ["₹1.42 Cr", "₹1.80 Cr", "₹1.50 Cr"],
            "Vs Model Prediction": ["-2.1%", "+24%", "+3.4%"]
        }, use_container_width=True)

    with tab3:
        st.subheader("3. Buy/Invest Recommendation")
        st.info("**Decision: MODERATELY POSITIVE INVESTMENT (HOLD/BUY)**")
        st.markdown(f"""
        **Actionable Insights:**
        1. **End-User Perspective:** Excellent buy due to '{transport}' public transport accessibility and '{security}' amenities.
        2. **Investor Perspective:** While capital appreciation is steady, rental yields are slightly below the city average. Consider this a long-term hold (5-7 years).
        3. **Negotiation Tip:** The prevailing supply of {furnishing} properties in {city} gives you a ~3-5% negotiation window. Start your offer around ₹1.38 Cr.
        """)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        <b>4. Financial & Legal Disclaimer:</b><br>
        This report is generated autonomously by an AI agent using predictive models and fetched historical data. 
        It does not constitute formal financial, legal, or investment advice. Always consult with a certified financial planner and legal 
        attorney before executing large real estate obligations or signing agreements.
    </div>
    """, unsafe_allow_html=True)
