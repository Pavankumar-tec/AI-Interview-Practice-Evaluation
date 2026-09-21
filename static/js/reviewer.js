/**
 * AI Assisted Interview Practice & Evaluation System
 * Human Reviewer Portal & Question Packs Management Logic
 */

let activeReviewer = 'reviewer_1';
let reviewerSamples = [];
let selectedReviewSample = null;

window.initReviewerPortal = async function() {
  setupReviewerEventListeners();
  await loadReviewerSamples();
};

function setupReviewerEventListeners() {
  const r1Btn = document.getElementById('btn-select-r1');
  const r2Btn = document.getElementById('btn-select-r2');

  if (r1Btn && r2Btn) {
    r1Btn.addEventListener('click', () => {
      activeReviewer = 'reviewer_1';
      r1Btn.classList.add('active');
      r2Btn.classList.remove('active');
      document.getElementById('current-reviewer-indicator').textContent = 'Currently Grading as: Reviewer 1 (Independent)';
    });

    r2Btn.addEventListener('click', () => {
      activeReviewer = 'reviewer_2';
      r2Btn.classList.add('active');
      r1Btn.classList.remove('active');
      document.getElementById('current-reviewer-indicator').textContent = 'Currently Grading as: Reviewer 2 (Independent)';
    });
  }

  const submitReviewBtn = document.getElementById('btn-submit-review');
  if (submitReviewBtn) {
    submitReviewBtn.addEventListener('click', submitReviewScore);
  }
}

async function loadReviewerSamples() {
  try {
    const res = await fetch('/api/research/sample-answers?limit=180');
    const data = await res.json();
    reviewerSamples = data.sample_answers || [];
    renderReviewerSampleSelect();
  } catch (e) {
    console.error("Failed to load reviewer samples:", e);
  }
}

function renderReviewerSampleSelect() {
  const selectEl = document.getElementById('reviewer-sample-select');
  if (!selectEl) return;

  selectEl.innerHTML = '<option value="">-- Choose a Sample Answer to Grade --</option>' +
    reviewerSamples.map(s => `
      <option value="${s.sample_id}">[${s.sample_id}] ${s.question_id} - ${s.category} (${s.performance_level})</option>
    `).join('');

  selectEl.addEventListener('change', (e) => {
    const sid = e.target.value;
    if (sid) {
      loadSampleForGrading(sid);
    }
  });

  if (reviewerSamples.length > 0) {
    selectEl.value = reviewerSamples[0].sample_id;
    loadSampleForGrading(reviewerSamples[0].sample_id);
  }
}

async function loadSampleForGrading(sampleId) {
  selectedReviewSample = reviewerSamples.find(x => x.sample_id === sampleId);
  if (!selectedReviewSample) return;

  document.getElementById('rev-question-text').textContent = selectedReviewSample.question_text;
  document.getElementById('rev-answer-text').textContent = selectedReviewSample.answer_text;
  document.getElementById('rev-meta-tag').textContent = `${selectedReviewSample.sample_id} • ${selectedReviewSample.category} • Source: ${selectedReviewSample.source_type}`;

  // Fetch full question to get rubric
  try {
    const res = await fetch(`/api/questions/${selectedReviewSample.question_id}`);
    const qData = await res.json();
    renderReviewRubricCriteria(qData.rubric || []);
  } catch (err) {
    console.error("Failed to fetch rubric for reviewer:", err);
  }
}

function renderReviewRubricCriteria(rubric) {
  const container = document.getElementById('reviewer-rubric-inputs');
  if (!container) return;

  container.innerHTML = rubric.map((crit, idx) => `
    <div class="criterion-card" style="margin-bottom: 12px;">
      <div class="flex-between mb-16">
        <div>
          <div style="font-weight: 600; color: #fff;">${crit.name}</div>
          <div style="font-size: 0.82rem; color: var(--text-muted);">${crit.description}</div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <input type="number" step="0.1" min="0" max="${crit.max_score}" value="${(crit.max_score * 0.75).toFixed(1)}" 
                 class="input-field rev-crit-score" data-crit-id="${crit.id || 'c'+(idx+1)}" data-max="${crit.max_score}" 
                 style="width: 70px; text-align: center; font-weight: 700;" oninput="updateTotalReviewScore()">
          <span style="font-size: 0.85rem; color: var(--text-muted);">/ ${crit.max_score}</span>
        </div>
      </div>
    </div>
  `).join('');

  updateTotalReviewScore();
}

window.updateTotalReviewScore = function() {
  const inputs = document.querySelectorAll('.rev-crit-score');
  let earned = 0;
  let possible = 0;

  inputs.forEach(inp => {
    earned += parseFloat(inp.value) || 0;
    possible += parseFloat(inp.getAttribute('data-max')) || 3.0;
  });

  const scaledTotal = possible > 0 ? (earned / possible) * 10.0 : 0;
  document.getElementById('reviewer-calculated-score').textContent = scaledTotal.toFixed(1);
};

async function submitReviewScore() {
  if (!selectedReviewSample) {
    alert('Please select a sample answer to grade.');
    return;
  }

  const inputs = document.querySelectorAll('.rev-crit-score');
  const criterionScores = {};
  let earned = 0;
  let possible = 0;

  inputs.forEach(inp => {
    const cid = inp.getAttribute('data-crit-id');
    const val = parseFloat(inp.value) || 0;
    criterionScores[cid] = val;
    earned += val;
    possible += parseFloat(inp.getAttribute('data-max')) || 3.0;
  });

  const overallScore = possible > 0 ? (earned / possible) * 10.0 : 0;
  const feedbackNotes = document.getElementById('reviewer-notes-input').value.trim();

  const payload = {
    sample_id: selectedReviewSample.sample_id,
    reviewer_id: activeReviewer,
    overall_score: parseFloat(overallScore.toFixed(2)),
    criterion_scores: criterionScores,
    feedback_notes: feedbackNotes || `Independent rating by ${activeReviewer}`
  };

  try {
    const res = await fetch('/api/reviewer/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      alert(`Success: Review saved for ${activeReviewer.replace('_', ' ').toUpperCase()}!`);
      // Update local item
      if (activeReviewer === 'reviewer_1') {
        selectedReviewSample.r1_score = payload.overall_score;
      } else {
        selectedReviewSample.r2_score = payload.overall_score;
      }
    }
  } catch (err) {
    console.error("Submit review error:", err);
    alert('Failed to submit review score.');
  }
}

// Question Packs View
window.renderQuestionPacks = async function() {
  const container = document.getElementById('question-packs-library-container');
  if (!container) return;

  try {
    const res = await fetch('/api/questions');
    const data = await res.json();
    const allQuestions = data.questions || [];

    container.innerHTML = allQuestions.map(q => `
      <div class="glass-card" style="margin-bottom: 16px;">
        <div class="flex-between mb-16">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span class="q-id-tag">${q.id}</span>
            <span style="font-size: 0.8rem; color: var(--text-accent); font-weight: 600;">${q.category}</span>
            <span class="q-diff-tag diff-${q.difficulty}">${q.difficulty}</span>
          </div>
          <span style="font-size: 0.76rem; color: var(--text-dim);">${q.pack_id}</span>
        </div>
        <h4 style="font-family: var(--font-heading); font-size: 1.1rem; margin-bottom: 12px; color: #fff;">${q.question_text}</h4>
        
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: var(--radius-sm); margin-bottom: 10px;">
          <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-accent); font-weight: 700; margin-bottom: 6px;">Scoring Rubric Criteria</div>
          <div style="display: flex; flex-direction: column; gap: 6px;">
            ${(q.rubric || []).map(r => `
              <div style="font-size: 0.82rem; color: var(--text-muted);">
                <strong style="color: #cbd5e1;">${r.name} (${r.max_score} pts):</strong> ${r.description}
              </div>
            `).join('')}
          </div>
        </div>

        ${q.reference_material ? `
          <div style="background: rgba(6, 182, 212, 0.05); border: 1px solid rgba(6, 182, 212, 0.2); padding: 12px; border-radius: var(--radius-sm); font-size: 0.82rem; color: #bae6fd;">
            <strong style="color: #38bdf8;">Reviewed Reference Material:</strong> ${q.reference_material}
          </div>
        ` : ''}
      </div>
    `).join('');
  } catch (err) {
    console.error("Failed to render packs:", err);
  }
};
