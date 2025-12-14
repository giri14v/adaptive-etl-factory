# Adaptive ETL Factory 🚀
👉 **Live App:** https://hackathon-theta-khaki.vercel.app/
👉 **YouTube Demo:** https://youtu.be/LNFg__9e3p8

An **end-to-end, production-style ETL orchestration system** that automatically plans, generates, executes, evaluates, and exposes data transformation pipelines — designed with **AI-readiness** at its core.

> ⚠️ **Important clarification**
>
> - The project is **AI-ready**, not fully AI-powered in the current hackathon build.
> - Autonomous AI-driven code generation (via **Cline CLI**) was partially used during development.
> - Due to **Cline free-tier credit limits**, the final hackathon version runs in a **deterministic fallback mode**.
> - Once a **paid Cline subscription** is enabled, the system can **evolve autonomously** without architectural changes.

This makes the project **future-proof** and immediately scalable into a true AI-driven ETL factory.

---

## 🔥 What Problem Does This Project Solve?

Data teams repeatedly face:

- Manual ETL script writing
- Poor data quality visibility
- Tight coupling between data ingestion, transformation, and evaluation
- No clear orchestration or observability

**Adaptive ETL Factory** solves this by:

- Orchestrating ETL as **modular agents**
- Automatically generating transformation logic
- Executing pipelines dynamically
- Evaluating data quality quantitatively
- Providing a **user-facing UI** to trigger and download results

All without requiring the user to write ETL code.

---

## 🧠 High-Level Architecture

```
User (Browser)
   │
   ▼
React UI (Vercel)
   │
   ▼
FastAPI Trigger API
   │
   ▼
Kestra Orchestration Engine
   │
   ▼
Planner → CodeGen → Executor → Evaluator
   │
   ▼
Cleaned CSV + Metrics
```

---

## 🧩 System Phases (Agent-Based Design)

### 1️⃣ Planner Agent

**Purpose:** Decide _what_ transformations are needed.

- Profiles dataset schema (when rows are available)
- Falls back to a default transformation plan when metadata-only input is provided
- Outputs a **JSON transformation plan**

Example operations:

- Date parsing
- Missing value imputation
- Deduplication

📍 `services/planner/main.py`

---

### 2️⃣ CodeGen Agent

**Purpose:** Decide _how_ to implement the plan.

Two modes:

#### 🔹 AI Mode (Cline CLI – Paid)

- Uses LLM-powered code generation
- Produces optimized, context-aware ETL scripts

#### 🔹 Deterministic Fallback Mode (Hackathon-safe)

- Generates a **safe, self-contained Python ETL script**
- Fully reproducible
- Requires no AI credits

📍 `services/codegen/main.py`

---

### 3️⃣ Executor Agent

**Purpose:** Run the generated ETL pipeline.

- Downloads input dataset (URL-based input)
- Executes generated `transform.py`
- Produces:

  - `input.csv`
  - `output.csv`

📍 `services/executor/main.py`

---

### 4️⃣ Evaluator Agent

**Purpose:** Measure data quality objectively.

Metrics computed:

- Row count
- Column count
- Null count
- Null density
- Overall quality score (0–1)

Outputs:

```json
{
  "rows": 100,
  "columns": 5,
  "null_density": 0.04,
  "quality_score": 0.96
}
```

📍 `services/evaluator/main.py`

---

### 5️⃣ (Optional) Evolve Agent 🚧

**Purpose:** Improve future pipelines based on past performance.

- Planned for reinforcement-based optimization
- Currently disabled due to AI credit constraints

📍 `services/evolve/main.py`

---

## 🧭 Orchestration with Kestra

Kestra acts as the **control plane**:

- Coordinates all agents
- Tracks execution state
- Handles retries and failures
- Exposes execution metadata via API

Flow:

```
planner → codegen → executor → evaluator
```

📍 `kestra/adaptive_etl_flow.yaml`

---

## 🖥️ User Interface (React + Vercel)

The UI allows users to:

- Paste a dataset URL
- Trigger ETL execution
- View pipeline progress
- Inspect quality score
- Download cleaned CSV

Built with:

- React (Vite)
- Tailwind CSS
- Async polling for execution status

📍 `ui/`

---

## 🛠️ Technology Stack

### Backend

- **Python 3.12**
- **FastAPI** (API services)
- **Kestra** (Orchestration)
- **Pandas** (Data processing)

### Frontend

- **React (Vite)**
- **Tailwind CSS**
- **Vercel** (Deployment)

### Dev & Workflow

- **GitHub** (Version control)
- **CodeRabbit** (AI code review)
- **Cline CLI** (AI code generation – optional)

---

## 📦 Project Folder Structure

```
adaptive-etl-factory/
├── api/                 # FastAPI trigger API
├── services/            # Planner, CodeGen, Executor, Evaluator agents
├── kestra/              # Kestra flow definitions
├── ui/                  # React frontend
├── runs/                # Runtime outputs (gitignored)
├── run_all_agents.sh    # Local service launcher
├── README.md
```

---

## ⚙️ Setup Instructions (Local)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/adaptive-etl-factory
cd adaptive-etl-factory
```

---

### 2️⃣ Backend Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate
pip install -r requirements.txt
```

Start all agents:

```bash
bash run_all_agents.sh
```

Start trigger API:

```bash
uvicorn api.run_etl:app --port 9000 --reload
```

---

### 3️⃣ Frontend Setup

```bash
cd ui
npm install
npm run dev
```

---

## ▶️ Usage

1. Open UI
2. Paste dataset URL (CSV)
3. Click **Run ETL**
4. Track progress
5. View quality score
6. Download cleaned CSV

---

## 🧠 AI-Readiness & Future Evolution

This project was **intentionally designed** to support autonomous AI behavior:

- CodeGen agent already supports LLM-based generation
- Evolve agent scaffolding exists
- No architectural changes required to enable AI

Once **Cline CLI paid subscription** is enabled:

- ETL logic can self-improve
- Pipelines adapt based on metrics
- Manual intervention becomes unnecessary

---

## 🏆 Hackathon Highlights

- Real orchestration engine (Kestra)
- Agent-based ETL design
- Deterministic + AI hybrid strategy
- Production-style workflow
- CodeRabbit-powered PR reviews

---

## 📜 License

MIT License

---

## 👤 Author

**Giri V**
Data Engineer / Analyst
Built for AI Agent Hackathon

## Why These Transformations?

This project intentionally focuses on **three core ETL transformations**:

- **Missing value handling (NA / NaN normalization)**
- **Date parsing and standardization**
- **Deduplication**

This is a **deliberate engineering decision**, not a limitation.

### Why these three?

These operations are the **only transformations that are universally safe and necessary across almost all real-world datasets**, regardless of domain (finance, healthcare, education, logs, analytics, etc.).

#### 1. Missing Values (NA / NaN)

Missing values are unavoidable in real datasets coming from APIs, CSV exports, logs, and user-generated sources. Unhandled missing values can silently break analytics, aggregations, and downstream pipelines.

What this project does:

- Normalizes missing values consistently
- Replaces `NA`, `NaN`, and empty placeholders safely
- Applies conservative, deterministic strategies to avoid data corruption

#### 2. Date Parsing

Dates are often stored as strings in multiple formats. Inconsistent date formats can break time-series analysis, grouping, and reporting.

What this project does:

- Detects date-like columns
- Parses and standardizes them into a consistent datetime format
- Ensures safe, reversible transformations

#### 3. Deduplication

Duplicate records are extremely common due to retries, joins, logging systems, and data ingestion errors.

What this project does:

- Removes exact duplicates
- Uses deterministic logic to ensure no semantic data loss

### Why not more transformations?

More advanced transformations (feature engineering, scaling, encoding, outlier removal, semantic renaming) **require understanding the meaning of data**. Applying them without AI inference is risky and can permanently corrupt datasets.

This project prioritizes:

- **Safety over aggressiveness**
- **Explainability over black-box logic**
- **Reproducibility over heuristics**

### AI-Ready by Design

The architecture is built to support **autonomous, AI-driven evolution**. Once AI inference (e.g., via a paid Cline CLI subscription) is enabled:

- The Planner agent can infer column semantics and choose optimal transformations
- The CodeGen agent can generate custom ETL code dynamically
- The Evolve agent can learn from evaluation metrics and improve future runs

No refactor is required — the current deterministic system seamlessly upgrades to AI-driven autonomy.

> In short: this project is **safe by default, intelligent by design, and AI-ready when enabled**.

---

## 🚀 Deployment & Live Demo

### 🌐 Frontend (Live)

The frontend of **Adaptive ETL Factory** is deployed on **Vercel** and serves as the primary user-facing interface.

👉 **Live App:** https://hackathon-theta-khaki.vercel.app/

Users can:

- Paste a dataset URL
- Trigger the ETL pipeline
- Track execution status
- View data quality metrics
- Download the cleaned CSV output

---

### 🎥 Demo Video

A complete end-to-end walkthrough of the project is available on YouTube, covering:

- Architecture overview
- UI flow
- Kestra orchestration
- Backend agents
- Final outputs & metrics

👉 **YouTube Demo:** https://youtu.be/LNFg__9e3p8

---

### 🖥️ Backend Deployment Note (Important)

The **backend services (Planner, CodeGen, Executor, Evaluator, API Gateway, Kestra)** are intentionally **run only in a local environment**.

This decision was made due to:

- Hackathon **time constraints**
- **Kestra OSS authentication & networking limitations** on managed cloud platforms
- Multi-service orchestration complexity (Kestra + FastAPI agents)
- Local filesystem dependency for generated artifacts (`runs/<run_id>/`)

Despite running locally, the backend is:

- Fully production-grade in structure
- API-driven and stateless where possible
- Ready for cloud deployment with minor adjustments (object storage, secrets manager, managed Kestra)

---

### 🔮 Production Readiness

With additional time and infrastructure, the backend can be deployed using:

- Docker Compose / Kubernetes
- Cloud object storage (S3/GCS) instead of local files
- Managed Kestra or self-hosted Kestra cluster
- Secure secrets management

The current setup intentionally prioritizes **clarity, correctness, and hackathon feasibility** over premature cloud complexity.

---

