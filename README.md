# Explain, Defend, Improve

An AI-assisted learning coach for placement-focused CS fundamentals. MCA final-year research prototype, 2026–2027.

**Purpose:** help students explain a concept, defend their reasoning, study one missing idea, and apply it to a different scenario. Research investigates feedback reliability; improved learning remains a hypothesis to test.

## Try it

```bash
python -m venv .venv
# Linux / macOS:
source .venv/bin/activate
# Windows PowerShell instead:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. No database seeding or API key is needed for the offline demonstration. For live feedback, set `LLM_PROVIDER`, `LLM_MODEL` and `LLM_API_KEY` on the server; see [commands](docs/RUNBOOK.md). No model has been selected or paid API call made on your behalf.

## What is implemented

- Responsive light/dark interface and 12 draft CS concept packs.
- Explain → Defend → Learn → Transfer flow, with a persisted learning trail and session export.
- Concept-specific, authored defense questions. These are deliberately fixed, not claimed to be dynamically adaptive.
- Live provider adapters; exact-substring quote validation; explicit model failures.
- Three genuinely separate research prompt conditions, using the same model/settings.
- Dataset validation, shuffled blind grading sheets, recorded experiment runs and paired analysis.
- MAE, RMSE, correlation, quadratic weighted kappa, question-cluster bootstrap intervals and explicit exclusions.
- Four-person ownership plan, review gates, task checklist and demo instructions.

## Research status: not measured

The previous version contained generated reviewer scores and benchmark outcomes. Those are not experimental evidence. The generated-results dashboard, seed generator, tracked database and Python bytecode have been retired from the current source tree. Existing local database files are preserved, but their old tables are not used by the new application. Historical commits still contain the original demo assets.

The offline evaluator measures keyword coverage only. It cannot validate factual correctness, identify understanding reliably, or establish a winning LLM method. Offline experiment outputs are labelled `demo_only`. Live costs and unsupported-feedback rates remain null until separately measured. Reference links and rubrics are drafts awaiting expert review.

## Project guide

| Document | Purpose |
|---|---|
| [Revised concept and scope](docs/PROJECT_PLAN.md) | Research questions, deliverables, limits and milestones |
| [Four-person work distribution](docs/TEAM_PLAN.md) | Owners, beginner-friendly tasks, handoffs and chain of command |
| [Command runbook](docs/RUNBOOK.md) | Setup, practice, grading sheets, benchmark, analysis and Git workflow |
| [Study protocol](docs/STUDY_PROTOCOL.md) | Fair comparison, independent grading and honest interpretation |
| [Task board](docs/TASKS.md) | Implemented work and remaining human tasks |
| [Presentation guide](docs/DEMO.md) | Junior-friendly demonstration and professor-facing explanation |
| [Verification](docs/VERIFICATION.md) | Tests performed and remaining validation |

## Tests

```bash
python -m unittest discover -s tests -v
```

This is a local prototype, not an authenticated multi-user service. Keep participant datasets, grading sheets and API credentials out of Git. The command-line study workflow writes private outputs into ignored directories. See the runbook before running a formal study.
