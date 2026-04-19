# 🏠 Estate Agent AI — Agentic Real Estate Advisory System

An autonomous AI-powered real estate advisory system that synthesizes **XGBoost price predictions** with **RAG-based market intelligence** to generate structured, investor-grade property advisory reports for the Indian real estate market.

🌐 **Live Demo**: [estate-agent-ai.streamlit.app](https://estate-agent-ai.streamlit.app/)

---

## 📋 Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Agent Workflow](#agent-workflow)
- [Tools & Components](#tools--components)
- [Structured Advisory Output](#structured-advisory-output)
- [Anti-Hallucination Strategies](#anti-hallucination-strategies)

---

## Overview

Indian real estate presents complex investment decisions requiring analysis across price trends, legal compliance (RERA), location dynamics, and risk factors. **Estate Agent AI** addresses this through a 7-node autonomous pipeline:

1. **Property Valuation Agent** — XGBoost ML model predicts market price based on 10 property features
2. **Market Research Agent** — RAG retrieves relevant market data from Knight Frank, JLL, and RERA documents
3. **Comparable Analysis Engine** — Generates comparable property analysis through ML model variations
4. **Risk Assessment Engine** — Multi-factor risk simulation (interest rate, market cycle, valuation, liquidity)
5. **Advisory Synthesizer** — LLM (GPT-4o-mini) synthesizes all data into a 5-section investment report

---

## System Architecture

```
User Query (Property Details + Investor Preferences)
│
▼
┌───────────────────────────────────────────────────────┐
│            LangGraph Workflow Engine                   │
│               (7-Node StateGraph)                      │
│                                                        │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐       │
│   │ VALIDATE │───▶│ VALUATE  │───▶│ RESEARCH │       │
│   │  Input   │    │  (ML)    │    │  (RAG)   │       │
│   └──────────┘    └──────────┘    └──────────┘       │
│                                        │              │
│                    ┌──────────────┐    │              │
│                    │  COMPARABLE  │◀───┘              │
│                    │  ANALYSIS    │                    │
│                    └──────┬───────┘                    │
│                           │                            │
│                    ┌──────────────┐                    │
│                    │    RISK      │                    │
│                    │  SIMULATOR   │                    │
│                    └──────┬───────┘                    │
│                           │                            │
│                    ┌──────────────┐                    │
│                    │  ADVISORY    │                    │
│                    │  (LLM Brain) │                    │
│                    └──────┬───────┘                    │
│                           │                            │
│                    ┌──────────────┐                    │
│                    │  QUALITY     │◀─┐                │
│                    │  CHECK       │  │ (retry if      │
│                    └──────┬───────┘  │  incomplete)   │
│                           │──────────┘                │
│                           ▼                            │
│                      [END / OUTPUT]                    │
└───────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────┐
│              Data & Knowledge Layer                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐  │
│  │  XGBoost   │  │  ChromaDB  │  │  Knowledge     │  │
│  │  Price     │  │  Vector    │  │  Base (MD)     │  │
│  │  Model     │  │  Store     │  │  RERA/Market   │  │
│  └────────────┘  └────────────┘  └────────────────┘  │
└───────────────────────────────────────────────────────┘
        │
        ▼
  Structured 5-Section Advisory Report
  + PDF Export + Interactive Streamlit UI
```

---

## Project Structure

```
Estate_Agent/
├── app/
│   └── main.py                     # Streamlit UI (premium glassmorphism)
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── graph.py                # LangGraph workflow (7 nodes, conditional edges)
│   │   ├── nodes.py                # Agent reasoning steps (7 nodes)
│   │   └── state.py                # Enhanced TypedDict state schema
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── ml_model.py             # XGBoost price predictor + confidence estimation
│   │   ├── search_rag.py           # ChromaDB RAG retrieval (lazy loading)
│   │   ├── comparable_analyzer.py  # Comparable property analysis via ML variations
│   │   ├── risk_simulator.py       # Multi-factor risk assessment
│   │   ├── market_sentiment.py     # Market sentiment extraction from RAG context
│   │   ├── report_generator.py     # Professional PDF export (ReportLab)
│   │   └── ingest.py               # Knowledge base builder (PDF + Markdown)
│   └── utils/
│       └── __init__.py
├── data/
│   ├── raw_reports/                # Source PDFs (RERA, JLL, Knight Frank)
│   │   ├── REAL_ESTATE_REGULATION_AND_DEVELOPMENT_ACT.pdf
│   │   ├── india-affordable-housing-2025-12385.pdf
│   │   ├── india-real-estate-residential-and-office-market-h1-2024-11307.pdf
│   │   └── jll-q4-2023-residential-market-update-final.pdf
│   ├── knowledge_base/             # Curated markdown knowledge docs
│   │   ├── india_market_overview_2024.md
│   │   ├── rera_compliance_guide.md
│   │   └── investment_guidelines.md
│   └── vector_store/               # ChromaDB index (auto-rebuilt)
├── models/
│   ├── model.joblib                # Trained XGBoost model
│   └── encoder.joblib              # Feature encoders/scalers
├── tests/
│   ├── __init__.py
│   ├── test_full_agent.py          # End-to-end pipeline test
│   ├── test_nodes.py               # Individual node tests
│   ├── test_ml.py                  # ML model + confidence tests
│   └── test_rag.py                 # RAG retrieval tests
├── .streamlit/
│   └── config.toml                 # Streamlit dark theme config
├── .env                            # API keys (gitignored)
├── .gitignore
├── requirements.txt
├── streamlit_app.py                # Deployment entry point
└── README.md
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | LangGraph (StateGraph + conditional edges) |
| LLM | OpenAI GPT-4o-mini |
| ML Model | XGBoost (property price prediction) |
| RAG Vector Store | ChromaDB with HuggingFace `all-MiniLM-L6-v2` embeddings |
| State Management | Python TypedDict with `Annotated` operators |
| Data Validation | Pydantic schemas |
| Web UI | Streamlit (glassmorphism dark theme) |
| PDF Export | ReportLab |
| Knowledge Sources | Knight Frank, JLL, RERA Act PDFs + curated markdown |

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/mittalayushh/Estate_Agent.git
cd Estate_Agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API keys
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Get an API key at [platform.openai.com](https://platform.openai.com).

### 4. Build the knowledge base (first run only)
```bash
python -m src.tools.ingest
```

This indexes all PDFs and markdown files into ChromaDB. Use `--force` to rebuild.

---

## Running the Application

### Streamlit Web App (Recommended)
```bash
streamlit run streamlit_app.py
```
Open http://localhost:8501 in your browser.

### Run Agent Directly (for testing)
```bash
python tests/test_full_agent.py
```

### Run Individual Tests
```bash
python tests/test_ml.py        # ML model test
python tests/test_rag.py       # RAG retrieval test
python tests/test_nodes.py     # Node transition test
```

---

## Agent Workflow

The 7-node pipeline follows a strict reasoning protocol:

### Node 1 — Input Validation
Validates and normalizes all property details. Fills defaults for missing fields to ensure robust downstream processing.

### Node 2 — ML Valuation
Runs the XGBoost model on 10 property features (type, BHK, size, city, state, furnishing, bathrooms, facing, security, transport). Computes a confidence score based on input typicality.

### Node 3 — Market Research (RAG)
Queries ChromaDB for two types of intelligence:
- **Market Trends**: City-specific price data, appreciation rates, demand drivers
- **RERA Compliance**: Legal guidelines, buyer protections, regulatory requirements

All results include source attribution (e.g., `[Source: JLL Q4 2023]`).

### Node 4 — Comparable Analysis
Generates 6 property variations (±1 BHK, ±20% size, different furnishing) and predicts their prices to show relative value positioning.

### Node 5 — Risk Assessment
Four-factor risk analysis:
1. **Interest Rate Sensitivity** — EMI impact at 7.5%, 8.5%, 9.5%, 10.5%
2. **Market Cycle Position** — Bullish/stable/bearish based on RAG signals
3. **Valuation Benchmark** — Price-per-sqft vs city benchmark ranges
4. **Liquidity Risk** — Property type resale analysis

### Node 6 — Advisory Synthesis (LLM)
GPT-4o-mini synthesizes all data into a structured 5-section report with anti-hallucination constraints.

### Node 7 — Quality Check
Validates the report contains all 5 required sections. If sections are missing, retries Node 6 (max 1 retry).

---

## Structured Advisory Output

Every report contains exactly 5 sections:

| Section | Content |
|---------|---------|
| 📋 **Property Valuation Summary** | Predicted price vs benchmarks, confidence analysis |
| 🏘️ **Comparable Property Analysis** | Similar properties with price differentials |
| 📊 **Market & Regulatory Analysis** | City trends, RERA compliance, infrastructure impact |
| 💰 **Investment Recommendation** | Buy/Hold/Avoid with ROI projections and EMI scenarios |
| ⚖️ **Legal & Financial Disclaimer** | Standard advisory disclaimers and RERA verification |

---

## Anti-Hallucination Strategies

1. **RAG-Grounded Citations**: LLM is instructed to cite ONLY from provided market context
2. **Source Attribution**: Every RAG chunk carries its source filename
3. **Confidence Scoring**: ML predictions include a confidence metric based on input typicality
4. **Structured Output Enforcement**: Quality check node validates all 5 sections exist
5. **Retry Loop**: Incomplete reports trigger a retry with the same context
6. **Explicit Uncertainty**: If data is insufficient, the LLM states "Data not available" instead of guessing
7. **Mandatory Disclaimer**: Every report must include a legal/financial disclaimer

---

## Deployment

### Streamlit Community Cloud
1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set the main file path to `streamlit_app.py`
5. Add `OPENAI_API_KEY` in the Secrets section

---

## License

MIT License

---

*Estate Agent AI — April 2026*
