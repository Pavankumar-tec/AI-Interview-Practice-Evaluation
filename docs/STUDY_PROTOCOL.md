# Study protocol — draft for supervisor review

## Primary experiment

Compare the same frozen model under three information conditions: question/answer only; question/answer plus rubric; question/answer plus rubric and reference. Output instructions, temperature and dataset stay constant. Reference material and rubrics are withheld from the general baseline. The result is an evaluation of this configuration on this dataset, not all LLMs.

Select a manageable set from the 12 draft concept packs. Person 2 and a qualified reviewer should replace broad rubric descriptions with concept-specific observable anchors and acceptable alternatives. Keep pilot answers separate from the final test set. Record content approval, versions and the study plan before collecting final results.

Include varied correct, partially correct and incorrect answers, correct paraphrases, jargon-heavy wrong answers, short correct explanations, and candidate text containing instructions to manipulate the evaluator. Keep answer construction labels away from graders and model prompts. Report authored/synthetic/student proportions separately. Do not build all strong answers by copying the same reference used by Method 3; this would favor lexical/reference matching.

Use qualified independent graders. They assess with the same weighted rubric and reference. They do not see the AI results, another grader’s scores, or expected performance/source labels. Rubric training uses pilot examples only. Record grader qualifications, disagreements and any adjudication separately; the implemented comparison uses the mean of the original two scores.

## Outcomes

Primary outcome: paired difference in MAE, Method 3 minus Method 1, against the mean human grade. A negative value favors Method 3. Secondary outcomes: all methods’ MAE/RMSE, weighted kappa on rounded 0–10 scores, Pearson correlation, percentage within one point, latency, and human inter-rater MAE. Correlation alone is not agreement.

The implementation reports deterministic percentile bootstrap intervals resampling question clusters. Few clusters produce unstable inference. It does not handle dependence from repeated participants; collect one independent answer per participant for that analysis or extend it appropriately. Confirm sample size and analysis with the supervisor. Repeatability across model calls needs a separate prespecified repeat experiment; variation across different answers is not repeatability.

All methods are compared on the same complete subset. Missing grades and failed model calls are excluded visibly. Inspect whether excluded answers systematically differ. The code records usage if supplied but does not calculate monetary cost. Unsupported feedback requires a separately defined claim-level human annotation process; quote substring checks alone do not validate support or truth. No automatic unsupported-feedback rate is claimed.

## Optional educational-impact study (not implemented)

If time and supervisor approval permit, compare targeted practice with generic feedback using random assignment, equal practice time, an unseen transfer test and blind human scoring. Keep test material unavailable during practice; the current practice app reveals lessons and is not a secure test environment. Consider a delayed test to distinguish retention from immediate recall. Plan participant-aware analysis and sample size before recruitment. Do not call the difference between two different practice question scores a learning gain.

## Data handling

Explain voluntary participation, what text is collected, external model processing if applicable, retention, who can access records and how to withdraw before anonymization/analysis. Follow the institution’s requirements. Use neutral study IDs and keep consent/identity mappings separately. Do not collect unnecessary names, emails or sensitive personal interview stories. Agree and document a deletion date. Never publish raw participant responses without appropriate permission.

## Remaining evidence requirements

- Literature review on automated scoring, LLM evaluators, feedback and transfer learning; identify the specific gap without claiming this is the first such system.
- Expert review of every included prompt, rubric, reference and lesson.
- Genuine independent grades and actual provider runs.
- Honest report of negative findings, disagreements and failure cases.
