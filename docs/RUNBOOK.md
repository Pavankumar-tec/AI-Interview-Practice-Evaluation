# Setup and chain of commands

Run commands from the repository root. Use Python 3.10 or later. These instructions use Bash; PowerShell differences follow.

## 1. Install and start

```bash
git clone https://github.com/I-invincib1e/AI-Interview-Practice-Evaluation.git
cd AI-Interview-Practice-Evaluation
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python app.py
```

Open http://127.0.0.1:5000. The app creates a `learning_sessions` table on demand. It never reads old generated benchmark tables. The old seed command is retired. Stop the server with Ctrl+C.

In PowerShell use `.venv\Scripts\Activate.ps1` instead of `source`. Use `py` if `python` is not installed as a command on your machine.

## 2. Optional live practice

Choose a provider/model available in your account; no current model availability is assumed. Credentials stay in server environment variables, never browser storage or committed files.

```bash
export LLM_PROVIDER=openai
export LLM_MODEL='YOUR_SUPPORTED_MODEL_ID'
read -rsp 'API key: ' LLM_API_KEY
export LLM_API_KEY
python app.py
```

Other implemented providers: `gemini`, `anthropic`. The selected model must support the adapter’s JSON/text output and temperature settings. Provider errors stop the request without substituting demo scores. For offline mode: `unset LLM_PROVIDER LLM_MODEL LLM_API_KEY`.

PowerShell:

```powershell
$env:LLM_PROVIDER = 'openai'
$env:LLM_MODEL = 'YOUR_SUPPORTED_MODEL_ID'
$secret = Read-Host 'API key' -AsSecureString
$env:LLM_API_KEY = [System.Net.NetworkCredential]::new('', $secret).Password
python app.py
```

The app is local-only by default. Session IDs permit access to the associated practice records; there is no account/login system. Do not expose this prototype publicly or use names/sensitive information in answers. Multi-user hosting requires authentication, access control, rate limits and a deployment review.

## 3. Verify the experiment pipeline without API spending

```bash
python -m scripts.study validate data/pilot.example.jsonl
python -m scripts.study run data/pilot.example.jsonl --offline-demo --out results/demo/run.jsonl
python -m scripts.study review-sheet data/pilot.example.jsonl --reviewer reviewer_1 --out data/private/demo-reviewer-1.csv
python -m scripts.study review-sheet data/pilot.example.jsonl --reviewer reviewer_2 --out data/private/demo-reviewer-2.csv
```

The example answers are authored workflow examples, not student data. Output paths are exclusive: re-running with the same path fails instead of overwriting records. Use a new run directory each time. Offline methods intentionally use the same keyword heuristic and cannot establish the three-method hypothesis.

## 4. Prepare the actual study

Person 2 obtains content/rubric sign-off. Person 3 creates `data/private/final.jsonl`, one JSON object per line. Use `data/pilot.example.jsonl` as a format example. Required fields:

| Field | Allowed values / meaning |
|---|---|
| `sample_id` | Unique neutral ID; must not reveal quality/source to graders |
| `concept_id` | ID from `data/concepts.json` |
| `stage` | `explain`, `defend` or `transfer` |
| `answer` | Submitted text |
| `source_type` | `student`, `authored` or `synthetic` |
| `provenance` | Origin and collection/version note; exclude identifying details |
| `split` | `pilot` or `test` |
| `consent_recorded` | Must be `true` for student answers; retain actual consent privately |

Use separate files for pilot and final review distribution. Do not combine multiple samples from a participant in the primary analysis without participant-aware statistical treatment. The validator checks declarations, not whether they are truthful. Never distribute source labels or AI outputs to reviewers.

```bash
python -m scripts.study validate data/private/final.jsonl
python -m scripts.study review-sheet data/private/final.jsonl --reviewer reviewer_1 --out data/private/final-reviewer-1.csv
python -m scripts.study review-sheet data/private/final.jsonl --reviewer reviewer_2 --out data/private/final-reviewer-2.csv
```

Person 4 sends each sheet to its assigned qualified reviewer through the team’s normal process. This software does not send messages. Reviewers fill `overall_score` (0–10) and `notes`; preserve IDs and other columns. Use rubric weights and document disagreements. Empty grades remain missing, never zero-filled.

## 5. Run the frozen live experiment

Set the environment variables above. Freeze the Git commit and content before this step. The live runner rejects an uncommitted working tree. Confirm budget with the team: three model calls per selected answer, plus any explicitly planned repeats. The following command makes paid provider calls using your credentials.

```bash
python -m scripts.study run data/private/final.jsonl --split test --expert-reviewed --out results/final-01/run.jsonl
```

`--expert-reviewed` is an attestation, not a substitute for a signed review record. Each line records dataset/content hashes, commit, prompt version, requested model/settings, full prompt, response, usage if supplied, real wall-clock latency or a failure. Calls are deterministically shuffled. No retries occur automatically. Costs are left unknown; calculate from recorded usage and dated provider pricing if needed. A partial/failed run is retained and exits with status 2; investigate before creating a new run. Do not cherry-pick successful reruns.

## 6. Analyze after independent grading

```bash
python -m scripts.study analyze results/final-01/run.jsonl data/private/final-reviewer-1.csv data/private/final-reviewer-2.csv --out results/final-01/analysis.json
```

Only samples with three successful methods and two grades enter the paired comparison. Inspect exclusions, sample count and intervals before writing conclusions. Blank sheets produce an insufficient-data result. Offline results remain demo-only even if humans grade them. Different runs/settings must not be concatenated.

## 7. Team Git workflow

```bash
git pull --ff-only
git switch -c team/content-review
# Edit only the files assigned to you.
git diff
python -m unittest discover -s tests -v
git add data/concepts.json docs/TASKS.md
git commit -m "Review concept rubrics and record open content issues"
git push -u origin team/content-review
```

Open a pull request for Invi to review. Person 3 and Person 4 can submit document edits through GitHub’s interface if command-line Git is unfamiliar. Never add credentials, local databases, participant records, private sheets or raw runs to a public repository. `.gitignore` excludes the designated private/output directories; it cannot detect private data placed elsewhere.
