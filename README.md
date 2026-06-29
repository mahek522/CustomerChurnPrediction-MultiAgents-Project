# Customer Churn Intelligence Platform

An enterprise-grade Agentic AI platform for customer churn prediction and retention strategy generation using a multi-agent architecture.

## 🏦 Overview

The Customer Churn Intelligence Platform leverages CrewAI's multi-agent system to analyze customer behavior, predict churn risk, and generate actionable retention recommendations. The platform uses RAG (Retrieval-Augmented Generation) with ChromaDB for semantic search, enforces numerical calculations via a Pandas-based analytics tool, validates grounding policies using Pydantic AI, exports professional PDF reports, and maintains long-term memory with PostgreSQL.

---

## ✨ Features

- **Multi-Agent Collaboration**: 6 specialized AI agents collaborate sequentially to process, analyze, predict, and validate churn queries.
- **Dynamic Analytics Grounding**: Enforces strict numerical validation on statistical inquiries using Pandas aggregations to eliminate LLM mathematical hallucinations.
- **Pydantic AI Validation**: Enforces business compliance (Grounding, Hallucination checks, and Confidence Score threshold $\ge 70\%$) using a structured validation schema.
- **Executive PDF Export**: Generates and downloads professionally formatted executive summary reports in PDF.
- **Memory & History Management**: Stateful session memory persisted dynamically in PostgreSQL.
- **Interactive UI & Charts**: Streamlit dashboard displaying live dataset metrics, status counts, and segment risks.
- **REST API**: FastAPI backend powering modular endpoints.

---

## 🏗️ Architecture

### Multi-Agent Sequence Workflow

```
User Query
    ↓
Query Agent (Retrieves customer records from ChromaDB)
    ↓
Data Analyst Agent (Calculates verified churn stats using Pandas tool)
    ↓
Prediction Agent (Predicts risk levels and probabilities)
    ↓
Recommendation Agent (Maps retention strategies based on segment risk)
    ↓
Validation Agent (Validates findings against Grounding Policies using Pydantic AI)
    ↓
Reporting Agent (Formats report into markdown executive summary)
```

---

## 📁 Project Structure

```
customer-churn-agentic-ai/
├── backend/
│   ├── agents/                   # Definitions of specialized agents
│   │   ├── churn_prediction_agent.py  # Predicts risk levels & probabilities
│   │   ├── data_analyst_agent.py      # Performs verified calculations
│   │   ├── llm_config.py              # Central LLM setup (Groq / Ollama switchover)
│   │   ├── memory_agent.py            # Long-term context retriever from DB
│   │   ├── query_agent.py             # User query classification & intent handler
│   │   ├── recommendation_agent.py    # Retention strategy generation
│   │   ├── reporting_agent.py         # Formats outputs into markdown reports
│   │   └── validation_agent.py        # Safety, grounding, and policy enforcement
│   ├── api/
│   │   └── app.py                     # FastAPI REST endpoints
│   ├── crews/                    # Orchestration pipelines
│   │   ├── analysis_tasks.py          # Query, analysis, and prediction task definitions
│   │   ├── churn_crew.py              # Sequence setup & delayed execution
│   │   ├── reporting_tasks.py         # Recommendation & report format task definitions
│   │   └── validation_tasks.py        # Validation task definitions
│   ├── guardrails/               # Safety layers filtering inputs/outputs
│   │   ├── input_guardrails.py        # Injection, SQL, and exfiltration filtering
│   │   └── output_guardrails.py       # PII, toxicity, and recommendation filtering
│   ├── memory/                   # Database models & connections
│   │   ├── database.py                # SQLAlchemy engine
│   │   ├── init_db.py                 # Schema initializer
│   │   ├── memory_service.py          # Session persistence (CRUD operations)
│   │   └── models.py                  # Database tables schema
│   ├── schemas/                  # Pydantic schemas
│   │   ├── customer_schema.py         # Customer records definition
│   │   └── validation_schema.py       # Pydantic AI structured validation output
│   ├── services/                 # Business logic services
│   │   ├── config.py                  # Environment-specific configuration paths
│   │   ├── data_ingestion_pipeline.py # Processing and importing CSVs to ChromaDB
│   │   ├── memory_context_service.py  # High-level memory utility
│   │   └── pdf_service.py             # Reportlab-based PDF generation engine
│   └── tools/                    # CrewAI tools
│       ├── analytics_tool.py          # Pandas-based analytical calculations
│       ├── memory_tool.py             # SQL retrieval tool for logs
│       ├── retrieval_tool.py          # Semantic vectorstore query tool
│       └── validation_tool.py         # Pydantic AI validation executor
├── datasets/
│   └── BNPParibas_Data.csv            # Cleaned customer dataset (911 records)
├── frontend/
│   └── streamlit_app.py               # Streamlit dashboard & chat UI
├── tests/
│   └── test_api.py                    # Integration tests for FastAPI endpoints
├── .env                               # Environment configurations
├── setup_chromadb.py                  # Populates ChromaDB vector database
├── setup_postgres.py                  # Sets up PostgreSQL database schema
└── requirements.txt                   # Dependency list
```

---

## 🚀 Setup & Local Execution

### 1. Create Virtual Environment & Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
USE_OLLAMA=false
USE_MOCK_MODE=false
OTEL_SDK_DISABLED=true
```

### 3. Initialize Databases
Ensure PostgreSQL is running locally, then initialize:

```bash
# Setup relational database schema
python setup_postgres.py

# Ingest dataset to ChromaDB
python setup_chromadb.py
```

### 4. Running the Platform

Start the FastAPI backend:
```bash
uvicorn backend.api.app:app --reload --host 127.0.0.1 --port 8000
```

Start the Streamlit dashboard:
```bash
streamlit run frontend/streamlit_app.py
```

---

## ☁️ Deployment Guide (Railway)

Follow these steps to deploy the PostgreSQL database, FastAPI backend, and Streamlit frontend on Railway.

### 1. Provision a PostgreSQL Database on Railway
1. Go to the [Railway Console](https://railway.app/) and create a new project.
2. Select **Provision PostgreSQL**.
3. Under the PostgreSQL service, go to **Variables** and copy the **DATABASE_URL** (e.g. `postgresql://postgres:password@host:port/railway`).

### 2. Deploy the FastAPI Backend
1. Click **New** $\rightarrow$ **Github Repo** $\rightarrow$ select your repository.
2. Under **Variables** for the backend service, add:
   - `DATABASE_URL` = *Your Railway PostgreSQL URL*
   - `GROQ_API_KEY` = *Your Groq Cloud API Key*
   - `USE_OLLAMA` = `false`
   - `USE_MOCK_MODE` = `false`
   - `PORT` = `8000`
3. Under **Settings**, set:
   - **Start Command**: `uvicorn backend.api.app:app --host 0.0.0.0 --port $PORT`
4. Under **Network**, click **Generate Domain** to get your backend URL (e.g., `https://backend-production.up.railway.app`).

### 3. Run Ingestion Scripts on the Cloud Postgres
Using the Railway CLI, run the database migrations in your project directory:
```bash
railway run python setup_postgres.py
railway run python setup_chromadb.py
```

### 4. Deploy the Streamlit Frontend
1. Click **New** $\rightarrow$ **Github Repo** $\rightarrow$ select your repository.
2. Rename the service to `frontend` or `streamlit-dashboard`.
3. Under **Variables** for the frontend service, add:
   - `API_URL` = *Your Backend URL generated in Step 2* (e.g. `https://backend-production.up.railway.app`)
4. Under **Settings**, set:
   - **Start Command**: `streamlit run frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
5. Under **Network**, click **Generate Domain** to get your public user-facing Streamlit URL.
