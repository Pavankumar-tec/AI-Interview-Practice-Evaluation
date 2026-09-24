# Revised project plan

## Concept

**Explain, Defend, Improve: AI-Assisted Concept Practice and Evidence-Based Feedback.**

Students may remember a definition without being able to explain its consequences. Our prototype provides a short practice loop: initial explanation, a concept-specific defense question, a brief lesson/activity, and a new application question. It supports preparation; it does not certify employability or detect true understanding with certainty.

The first validated domain is placement-focused CS fundamentals. The content format remains extensible. A focused, reviewed study is more useful than an unvalidated general-purpose claim.

## Research questions

1. Primary: Does adding question-specific rubrics and reference material improve AI agreement with independent human grades relative to a general scoring prompt?
2. Exploratory: How do these methods behave on correct paraphrases, keyword-heavy wrong answers, short correct answers, uncertainty and prompt-injection attempts?
3. Optional later study: Does targeted practice improve performance on unseen related questions compared with generic feedback under equal practice time?

Questions 1–2 are the current experiment scope. Question 3 requires real participants, a comparison condition and an approved design. The current app does not randomize participants or implement a controlled learning-gain study. Do not infer a learning gain from its session scores.

## Deliverables and acceptance

| Deliverable | Acceptance condition |
|---|---|
| Student prototype | Completes four stages, preserves responses, displays honest engine labels, exports a session |
| Concept pack | Each item has prompts, scoring criteria, lesson and references; knowledgeable reviewer signs off before study |
| Frozen dataset | Sources and consent are documented; pilot/test sets separated; no fabricated student labels |
| Experiment | Identical model/settings; distinct information conditions; every call recorded; failures retained |
| Human baseline | Two capable people grade independently before seeing AI scores |
| Analysis | Paired common subset; sample exclusions and uncertainty reported; no predetermined winning method |
| Final presentation | Live learning demonstration, valid method/results explanation, limitations and individual contributions |

## Suggested sequence (adjust to the submission date)

| Stage | Team output | Exit gate |
|---|---|---|
| Week 1: content and setup | Everyone runs the app; select and review concept packs | Faculty approves scope; content reviewer signs off |
| Week 2: pilot | Small pilot dataset, trial human grades, confusing rubrics corrected | Freeze rubrics and prompts before final answers are scored |
| Week 3: final evaluation | Approximately 60–100 answers as a practical pilot target; independent grading and real calls | All exclusions recorded; no tuning on test results |
| Week 4: analysis and defense | Results, report, demo, individual viva practice | All four members can explain their own work |

The suggested answer count is a feasibility target, not a statistical power calculation. Agree the final design with the supervisor. Start smaller for pipeline testing.

## Scope limits

No voice/video interview analysis, emotion detection, hiring rankings, avatars, streak gamification, or model training is needed for the first study. The contribution is a transparent implementation and careful evaluation in a bounded educational setting. Novelty relative to prior literature still needs a documented literature review; no publication or showcase outcome is guaranteed.
