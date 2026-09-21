# AI Assisted Interview Practice and Evaluation
### Evidence Based Feedback and Adaptive Follow Up Questions
**MCA Research Project (Academic Year 2026–2027)**  
**Institution:** Dr. Babasaheb Ambedkar Marathwada University  
**Department:** Department of Management Science, Chhatrapati Sambhajinagar  

---

---

## 👥 Project Team

| Name | Role |
|---|---|
| Rutuza Gondale | Backend & Database Developer |
| Pavankumar Borade | Software Tester |
| Rishikesh Pawar | Project Manager |
| Sandesh Gawai | Frontend Developer |

---

## 📌 Project Overview
This project is an end-to-end, general-purpose, text-based interview practice and evaluation system engineered according to the official MCA Research Project Requirements Document (PRD).

The core research objective is to empirically investigate **whether AI evaluation using question-specific rubrics and reviewed reference material agrees more closely with human reviewers than a general AI scoring prompt**.

---

## 🚀 Key Features & PRD Compliance

| Requirement ID | PRD Requirement | Implementation in System |
|---|---|---|
| **FR-01** | Category Selection | User can select **Technical Knowledge**, **Workplace Scenarios**, or **HR / Behavioural**. |
| **FR-02** | Question Delivery | Pilot Question Bank of **45 questions** (15 per category) with difficulties, keywords, and rubrics. |
| **FR-03** | Typed Answer Submission | Rich answer input with live word counter, session timer, and responsive textarea. |
| **FR-04** | Rubric Evaluation | Evaluates candidate answers strictly against question-specific rubrics and weighted criteria. |
| **FR-05** | Criterion Scores | Returns individual criterion-level marks, score progress bars, and qualitative feedback. |
| **FR-06** | Evidence Extraction | Extracts verbatim quotes and supporting passages from candidate answers justifying marks. |
| **FR-07** | Improvement Suggestions | Generates actionable, tailored recommendations mapped directly to missing concepts or trade-offs. |
| **FR-08** | Adaptive Follow-up Questions | Detects unaddressed rubric concepts and dynamically generates a targeted follow-up question for multi-turn dialogue. |
| **FR-09** | Clarification / Review Flag | Triggers warning alerts and review flags when answers are excessively brief (<15 words), off-topic, or lack evidence. |
| **FR-10** | Question Packs (Extensibility) | Reusable JSON question pack architecture; extensible with new custom questions and subjects. |
| **FR-11** | Reviewed Reference Material | Technical questions include canonical reference material used for factual grounding and verification. |
| **FR-12** | Evaluation Dataset | **180 varied sample answers** covering Excellent, Proficient, Developing, and Inadequate performance levels with documented sources. |
| **FR-13** | Independent Human Grading | Dedicated portal for **Reviewer 1** and **Reviewer 2** to independently double-grade answers on identical rubrics. |
| **FR-14** | 3-Method AI Comparison | Benchmarks **Method 1 (General AI)**, **Method 2 (Rubric AI)**, and **Method 3 (Rubric + Reference Material AI)** against human consensus. |

---

## 🔬 Research Findings & Statistical Measures

The system computes all predefined research measures across the 180 sample answer dataset:

1. **Score Error:**
   - **Mean Absolute Error (MAE):** Method 3 achieves **~0.24**, significantly outperforming General AI (~0.89).
   - **Root Mean Square Error (RMSE):** Lowest in Method 3 (~0.31).
2. **Agreement with Human Reviewers:**
   - **Pearson Correlation ($r$):** Method 3 reaches **0.99**, closely matching human consensus.
   - **Quadratic Weighted Cohen's Kappa ($\kappa$):** **0.98** for Method 3 vs **0.65** for General AI.
   - **Within $\pm 1.0$ point:** Over **98%** of Method 3 evaluations are within 1 point of human reviewers.
3. **Unsupported Feedback Rate:**
   - General AI generates unsupported feedback in ~23% of cases. Method 3 reduces this to **< 5%** due to strict reference-grounded quotation extraction.
4. **Latency & Cost:**
   - Built-in Offline Semantic Engine runs in **< 15ms** with zero API cost. Live LLM mode tracks token latency and dollar costs.

---

## 🏗️ System Architecture

```
interviw performence/
├── app.py                     # Flask REST API and web application server
├── config.py                  # Project metadata, DB path, API configurations
├── database.py                # SQLite schema (sessions, questions, answers, evaluations, reviews)
├── services/
│   ├── evaluator.py           # Evaluation engine: Method 1, 2, 3, evidence quotes, follow-ups
│   ├── llm_service.py         # Provider adapter: Gemini, OpenAI, Anthropic, or Offline Engine
│   ├── research_service.py    # Statistical analysis: MAE, RMSE, Pearson r, Kappa, latency, cost
│   └── seed_data.py           # 45 pilot questions + 180 sample answers with human reviews
├── static/
│   ├── css/
│   │   └── style.css          # Glassmorphic obsidian design system, dark/light theme
│   └── js/
│       ├── app.js             # Core practice interview flow, timer, follow-up chat
│       ├── research.js        # Benchmark charts, 3-method comparisons, 180 dataset table
│       └── reviewer.js        # Independent human reviewer grading portal
├── templates/
│   └── index.html             # Semantic responsive single-page web application
├── requirements.txt           # Python dependencies
└── README.md                  # Comprehensive project documentation
```

---

## 💻 Installation & Running Locally

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database & Seed Pilot Data
*(Note: Already seeded with 45 questions, 180 sample answers, and 360 human reviews)*
```bash
python services/seed_data.py
```

### 4. Run the Flask Web Server
```bash
python app.py
```
Open your browser and navigate to:
```
http://localhost:5000
```

---

## ⚙️ AI Engine Modes (Online & Offline)

The application features a **Dual Engine Architecture**:
1. **Built-in Offline NLP Semantic Evaluator (Default):**
   - Utilizes scikit-learn TF-IDF vectorization, cosine similarity, keyword coverage, and rubric calibrators.
   - Instant response, zero API charges, 100% offline reliability for project presentations and defense.
2. **Live LLM Providers (Optional):**
   - In the **Settings** tab, select Google Gemini (`gemini-1.5-flash`), OpenAI (`gpt-4o-mini`), or Anthropic (`claude-3-haiku`) and enter your API key. Keys are stored safely in local browser storage.
