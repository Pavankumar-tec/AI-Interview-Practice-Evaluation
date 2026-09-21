/**
 * AI Assisted Interview Practice & Evaluation System
 * Core Frontend Application Logic
 */

const state = {
  activeTab: 'practice',
  categories: [],
  questions: [],
  selectedCategory: 'Technical Knowledge',
  currentQuestion: null,
  session: {
    id: null,
    candidateName: 'Candidate User',
    startTime: null,
    timerInterval: null,
    secondsElapsed: 0
  },
  lastEvaluation: null,
  providerConfig: {
    provider: 'offline_semantic',
    apiKey: '',
    model: ''
  }
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  loadStoredSettings();
  setupTabNavigation();
  setupEventListeners();
  await loadCategories();
  await loadQuestions();
});

function loadStoredSettings() {
  const saved = localStorage.getItem('ai_interview_settings');
  if (saved) {
    try {
      state.providerConfig = JSON.parse(saved);
      const provSelect = document.getElementById('setting-provider');
      const keyInput = document.getElementById('setting-api-key');
      if (provSelect) provSelect.value = state.providerConfig.provider || 'offline_semantic';
      if (keyInput) keyInput.value = state.providerConfig.apiKey || '';
      updateProviderBadge();
    } catch (e) {
      console.error("Error loading settings:", e);
    }
  }
}

function updateProviderBadge() {
  const badge = document.getElementById('provider-status-text');
  if (badge) {
    if (state.providerConfig.provider === 'offline_semantic') {
      badge.textContent = 'Offline Semantic Evaluator (Active)';
    } else {
      badge.textContent = `Live LLM: ${state.providerConfig.provider.toUpperCase()} (Active)`;
    }
  }
}

// Tab Navigation
function setupTabNavigation() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      switchTab(targetTab);
    });
  });
}

function switchTab(tabId) {
  state.activeTab = tabId;
  document.querySelectorAll('.tab-btn').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
  });
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.classList.toggle('active', p.id === `tab-${tabId}`);
  });

  if (tabId === 'research' && window.initResearchDashboard) {
    window.initResearchDashboard();
  } else if (tabId === 'reviewer' && window.initReviewerPortal) {
    window.initReviewerPortal();
  } else if (tabId === 'packs' && window.renderQuestionPacks) {
    window.renderQuestionPacks();
  }
}

// Load Categories from Backend
async function loadCategories() {
  try {
    const res = await fetch('/api/categories');
    const data = await res.json();
    state.categories = data.categories || [];
    renderCategories();
  } catch (err) {
    console.error("Failed to load categories:", err);
  }
}

function renderCategories() {
  const container = document.getElementById('category-cards-container');
  if (!container) return;

  container.innerHTML = state.categories.map(c => `
    <div class="cat-card ${c.name === state.selectedCategory ? 'active' : ''}" onclick="selectCategory('${c.name}')">
      <div class="cat-icon-wrap">
        ${c.name.includes('Technical') ? '💻' : (c.name.includes('Workplace') ? '🏢' : '🤝')}
      </div>
      <h3>${c.name}</h3>
      <p>${getCategoryDescription(c.name)}</p>
      <div class="cat-meta">
        <span>${c.count} Question Bank</span>
        <span>Rubric &amp; ${c.name.includes('Technical') ? 'Ref Material' : 'Evidence'}</span>
      </div>
    </div>
  `).join('');
}

function getCategoryDescription(cat) {
  if (cat.includes('Technical')) {
    return 'Evaluates technical correctness, computational depth, and trade-offs against reviewed reference material.';
  } else if (cat.includes('Workplace')) {
    return 'Evaluates situational judgment, incident mitigation, stakeholder communication, and engineering ethics.';
  } else {
    return 'Assesses communication structure (STAR), leadership, adaptability, and self-awareness.';
  }
}

window.selectCategory = function(catName) {
  state.selectedCategory = catName;
  renderCategories();
  loadQuestions(catName);
};

// Load Questions from Backend
async function loadQuestions(category = state.selectedCategory) {
  try {
    const res = await fetch(`/api/questions?category=${encodeURIComponent(category)}`);
    const data = await res.json();
    state.questions = data.questions || [];
    renderQuestionsList();
    if (state.questions.length > 0) {
      selectQuestion(state.questions[0].id);
    }
  } catch (err) {
    console.error("Failed to load questions:", err);
  }
}

function renderQuestionsList() {
  const container = document.getElementById('questions-list-container');
  if (!container) return;

  container.innerHTML = state.questions.map(q => `
    <div class="question-item ${state.currentQuestion && state.currentQuestion.id === q.id ? 'active' : ''}" 
         id="q-item-${q.id}" onclick="selectQuestion('${q.id}')">
      <div class="q-badge-row">
        <span class="q-id-tag">${q.id}</span>
        <span class="q-diff-tag diff-${q.difficulty || 'Mid-Level'}">${q.difficulty || 'Mid-Level'}</span>
      </div>
      <div class="question-item-text">${q.question_text}</div>
    </div>
  `).join('');
}

window.selectQuestion = function(qid) {
  const q = state.questions.find(x => x.id === qid);
  if (!q) return;

  state.currentQuestion = q;
  document.querySelectorAll('.question-item').forEach(el => el.classList.remove('active'));
  const activeEl = document.getElementById(`q-item-${qid}`);
  if (activeEl) activeEl.classList.add('active');

  // Populate Main Stage
  document.getElementById('q-current-id').textContent = q.id;
  document.getElementById('q-current-category').textContent = q.category;
  document.getElementById('q-current-text').textContent = q.question_text;

  const diffTag = document.getElementById('q-current-diff');
  diffTag.textContent = q.difficulty || 'Mid-Level';
  diffTag.className = `q-diff-tag diff-${q.difficulty || 'Mid-Level'}`;

  // Populate Rubric Accordion
  const rubricList = document.getElementById('rubric-items-container');
  if (rubricList) {
    rubricList.innerHTML = (q.rubric || []).map(c => `
      <div class="rubric-item-row">
        <span class="rubric-item-badge">${c.name} (${c.max_score} pts):</span>
        <span>${c.description}</span>
      </div>
    `).join('');
  }

  // Reference Material preview for Technical Questions
  const refBlock = document.getElementById('reference-material-preview');
  if (refBlock) {
    if (q.reference_material) {
      refBlock.style.display = 'block';
      document.getElementById('ref-material-text').textContent = q.reference_material;
    } else {
      refBlock.style.display = 'none';
    }
  }

  // Answer Box setup for MCQ vs Descriptive
  const textArea = document.getElementById('candidate-answer-input');
  const mcqContainer = document.getElementById('mcq-options-container');

  if (q.question_type === 'mcq') {
    textArea.style.display = 'none';
    mcqContainer.style.display = 'block';
    
    mcqContainer.innerHTML = (q.options || []).map((opt, idx) => `
      <div style="margin-bottom: 12px;">
        <label style="cursor: pointer; display: flex; align-items: center; gap: 10px;">
          <input type="radio" name="mcq_option" value="${opt.replace(/"/g, '&quot;')}" style="cursor: pointer; transform: scale(1.2);">
          <span style="color: #fff; font-size: 1.05rem;">${opt}</span>
        </label>
      </div>
    `).join('');
  } else {
    textArea.style.display = 'block';
    mcqContainer.style.display = 'none';
    textArea.value = '';
  }

  // Reset evaluation panel
  updateWordCount();
  document.getElementById('feedback-card').classList.remove('active');
  resetTimer();
  startTimer();
};

// Event Listeners for Answer Input & Timer
function setupEventListeners() {
  const answerInput = document.getElementById('candidate-answer-input');
  if (answerInput) {
    answerInput.addEventListener('input', updateWordCount);
  }

  const submitBtn = document.getElementById('btn-submit-answer');
  if (submitBtn) {
    submitBtn.addEventListener('click', submitAnswer);
  }

  const compareBtn = document.getElementById('btn-compare-methods');
  if (compareBtn) {
    compareBtn.addEventListener('click', openMethodComparisonModal);
  }

  const toggleRubricBtn = document.getElementById('rubric-toggle-bar');
  if (toggleRubricBtn) {
    toggleRubricBtn.addEventListener('click', () => {
      document.getElementById('rubric-accordion').classList.toggle('open');
    });
  }

  const searchInput = document.getElementById('search-questions');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase();
      document.querySelectorAll('.question-item').forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(term) ? 'block' : 'none';
      });
    });
  }

  // Settings Save
  const saveSettingsBtn = document.getElementById('btn-save-settings');
  if (saveSettingsBtn) {
    saveSettingsBtn.addEventListener('click', () => {
      const provider = document.getElementById('setting-provider').value;
      const apiKey = document.getElementById('setting-api-key').value.trim();
      state.providerConfig = { provider, apiKey };
      localStorage.setItem('ai_interview_settings', JSON.stringify(state.providerConfig));
      updateProviderBadge();
      alert('Settings saved successfully!');
    });
  }
}

function updateWordCount() {
  const text = (document.getElementById('candidate-answer-input').value || '').trim();
  const words = text ? text.split(/\s+/).length : 0;
  document.getElementById('word-counter').textContent = `${words} words`;
}

// Timer Functions
function startTimer() {
  clearInterval(state.session.timerInterval);
  state.session.secondsElapsed = 0;
  updateTimerDisplay();
  state.session.timerInterval = setInterval(() => {
    state.session.secondsElapsed++;
    updateTimerDisplay();
  }, 1000);
}

function resetTimer() {
  clearInterval(state.session.timerInterval);
  state.session.secondsElapsed = 0;
  updateTimerDisplay();
}

function updateTimerDisplay() {
  const timerEl = document.getElementById('session-timer');
  if (!timerEl) return;
  const mins = String(Math.floor(state.session.secondsElapsed / 60)).padStart(2, '0');
  const secs = String(state.session.secondsElapsed % 60).padStart(2, '0');
  timerEl.textContent = `⏱️ ${mins}:${secs}`;
}

// Submit Answer for Evaluation
async function submitAnswer() {
  let answerText = '';
  
  if (state.currentQuestion && state.currentQuestion.question_type === 'mcq') {
    const selected = document.querySelector('input[name="mcq_option"]:checked');
    if (selected) {
      answerText = selected.value;
    }
  } else {
    answerText = (document.getElementById('candidate-answer-input').value || '').trim();
  }

  if (!answerText) {
    alert('Please provide an answer before submitting for evaluation.');
    return;
  }

  if (!state.currentQuestion) {
    alert('No question selected.');
    return;
  }

  const submitBtn = document.getElementById('btn-submit-answer');
  submitBtn.disabled = true;
  submitBtn.innerHTML = 'Evaluating Response...';

  const methodSelect = document.getElementById('eval-method-select');
  const selectedMethod = methodSelect ? methodSelect.value : 'method_3_rubric_ref';

  try {
    const payload = {
      question_id: state.currentQuestion.id,
      answer_text: answerText,
      evaluation_method: selectedMethod,
      provider_config: state.providerConfig
    };

    const res = await fetch('/api/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const result = await res.json();
    state.lastEvaluation = result;
    renderEvaluationFeedback(result);
  } catch (err) {
    console.error("Evaluation error:", err);
    alert('An error occurred during evaluation. Please try again.');
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<span>Submit for Evaluation</span>';
  }
}

// Render Evaluation Feedback Card
function renderEvaluationFeedback(ev) {
  const card = document.getElementById('feedback-card');
  card.classList.add('active');

  // Overall Score
  document.getElementById('score-num-display').textContent = ev.overall_score.toFixed(1);

  // Clarification / Review Flag Badge (FR-09)
  const flagContainer = document.getElementById('flag-badge-container');
  if (ev.clarification_needed || ev.review_flag) {
    flagContainer.innerHTML = `
      <span class="flag-badge warning">
        ⚠️ Clarification / Review Needed: ${ev.flag_reason || 'Evidence is insufficient'}
      </span>
    `;
  } else {
    flagContainer.innerHTML = `
      <span class="flag-badge success">
        ✓ Fully Grounded in Rubric Evidence
      </span>
    `;
  }

  // Method Info
  const methodLabel = document.getElementById('eval-method-used-label');
  if (methodLabel) {
    const methodName = ev.evaluation_method === 'method_1_general' 
      ? 'Method 1 (General AI)' 
      : (ev.evaluation_method === 'method_2_rubric' ? 'Method 2 (Rubric-Based AI)' : 'Method 3 (Rubric + Ref Material)');
    methodLabel.textContent = `${methodName} • ${ev.latency_ms}ms latency`;
  }

  // Criterion Scores Breakdown
  const critContainer = document.getElementById('criteria-score-bars');
  critContainer.innerHTML = '';
  const criteria = ev.criterion_scores || {};
  for (const key in criteria) {
    const c = criteria[key];
    const pct = Math.round((c.score / (c.max_score || 3.0)) * 100);
    critContainer.innerHTML += `
      <div class="criterion-card">
        <div class="crit-header">
          <span>${c.name}</span>
          <span>${c.score.toFixed(1)} / ${c.max_score} pts</span>
        </div>
        <div class="crit-bar-bg">
          <div class="crit-bar-fill" style="width: ${pct}%"></div>
        </div>
        <div class="crit-comment">${c.feedback}</div>
      </div>
    `;
  }

  // Evidence Quotes (FR-06)
  const evidenceContainer = document.getElementById('evidence-quotes-list');
  if (ev.evidence_quotes && ev.evidence_quotes.length > 0) {
    evidenceContainer.innerHTML = ev.evidence_quotes.map(q => `
      <div class="quote-bubble">"${q}"</div>
    `).join('');
  } else {
    evidenceContainer.innerHTML = '<div class="text-muted" style="font-size: 0.85rem;">No direct evidence quotes could be matched.</div>';
  }

  // Actionable Suggestions (FR-07)
  const suggestionsContainer = document.getElementById('suggestions-list');
  if (ev.suggestions && ev.suggestions.length > 0) {
    suggestionsContainer.innerHTML = ev.suggestions.map(s => `
      <div class="suggestion-item">
        <span class="suggestion-bullet">✦</span>
        <span>${s}</span>
      </div>
    `).join('');
  } else {
    suggestionsContainer.innerHTML = '<div class="text-muted">No suggestions generated.</div>';
  }

  // Targeted Adaptive Follow-up Question (FR-08)
  const followupBlock = document.getElementById('followup-card-block');
  if (ev.followup_question) {
    followupBlock.style.display = 'block';
    document.getElementById('followup-question-prompt').textContent = ev.followup_question;
    document.getElementById('followup-reply-input').value = '';
  } else {
    followupBlock.style.display = 'none';
  }

  // Scroll down to feedback
  card.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Adaptive Follow-up Submission
window.submitFollowupReply = async function() {
  const replyText = (document.getElementById('followup-reply-input').value || '').trim();
  if (!replyText) {
    alert('Please enter your response to the follow-up question.');
    return;
  }

  const initialAnswer = document.getElementById('candidate-answer-input').value.trim();
  const btn = document.getElementById('btn-submit-followup');
  btn.disabled = true;
  btn.textContent = 'Re-Evaluating Combined Answer...';

  try {
    const payload = {
      question_id: state.currentQuestion.id,
      answer_text: initialAnswer,
      followup_answer: replyText,
      evaluation_method: 'method_3_rubric_ref',
      provider_config: state.providerConfig
    };

    const res = await fetch('/api/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const updatedResult = await res.json();
    renderEvaluationFeedback(updatedResult);
    alert('Evaluation updated with your follow-up clarification!');
  } catch (err) {
    console.error("Follow-up error:", err);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Submit Follow-Up Response';
  }
};

// Side-by-Side Method Comparison Modal
async function openMethodComparisonModal() {
  let answerText = '';
  
  if (state.currentQuestion && state.currentQuestion.question_type === 'mcq') {
    const selected = document.querySelector('input[name="mcq_option"]:checked');
    if (selected) {
      answerText = selected.value;
    }
  } else {
    answerText = (document.getElementById('candidate-answer-input').value || '').trim();
  }

  if (!answerText) {
    alert('Please provide an answer to compare methods.');
    return;
  }

  const modal = document.getElementById('comparison-modal');
  modal.classList.add('active');
  const container = document.getElementById('comparison-modal-content');
  container.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--text-muted);">Running Method 1, Method 2, and Method 3 evaluations...</div>';

  try {
    const res = await fetch('/api/compare-methods', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question_id: state.currentQuestion.id,
        answer_text: answerText
      })
    });

    const data = await res.json();
    const c = data.comparisons;

    container.innerHTML = `
      <div style="margin-bottom: 20px;">
        <h4 style="font-family: var(--font-heading); color: var(--text-accent);">Question: ${data.question_text}</h4>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
        <!-- Method 1 -->
        <div class="glass-card" style="border-top: 4px solid var(--accent-rose);">
          <div style="font-family: var(--font-heading); font-weight: 700; color: #fb7185; margin-bottom: 8px;">Method 1: General AI</div>
          <div style="font-size: 2rem; font-weight: 800; color: #fff; margin-bottom: 12px;">${c.method_1_general.overall_score} <span style="font-size: 1rem; color: var(--text-muted);">/10</span></div>
          <div style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 12px;">General prompt baseline. Lacks strict criterion weighting; higher unsupported feedback.</div>
          <div style="font-size: 0.8rem; font-weight: 600; color: var(--accent-amber);">Unsupported claims: ${c.method_1_general.unsupported_feedback_count}</div>
        </div>

        <!-- Method 2 -->
        <div class="glass-card" style="border-top: 4px solid var(--accent-amber);">
          <div style="font-family: var(--font-heading); font-weight: 700; color: #fbbf24; margin-bottom: 8px;">Method 2: Rubric-Based AI</div>
          <div style="font-size: 2rem; font-weight: 800; color: #fff; margin-bottom: 12px;">${c.method_2_rubric.overall_score} <span style="font-size: 1rem; color: var(--text-muted);">/10</span></div>
          <div style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 12px;">Calibrated against question-specific rubrics. Better criterion agreement.</div>
          <div style="font-size: 0.8rem; font-weight: 600; color: var(--accent-amber);">Unsupported claims: ${c.method_2_rubric.unsupported_feedback_count}</div>
        </div>

        <!-- Method 3 -->
        <div class="glass-card" style="border-top: 4px solid var(--accent-emerald);">
          <div style="font-family: var(--font-heading); font-weight: 700; color: #34d399; margin-bottom: 8px;">Method 3: Rubric + Ref Material</div>
          <div style="font-size: 2rem; font-weight: 800; color: #fff; margin-bottom: 12px;">${c.method_3_rubric_ref.overall_score} <span style="font-size: 1rem; color: var(--text-muted);">/10</span></div>
          <div style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 12px;">Highest alignment with human reviewers; exact citation grounding and reference checking.</div>
          <div style="font-size: 0.8rem; font-weight: 600; color: #34d399;">Unsupported claims: ${c.method_3_rubric_ref.unsupported_feedback_count}</div>
        </div>
      </div>
    `;
  } catch (err) {
    container.innerHTML = '<div style="color: var(--accent-rose); padding: 20px;">Failed to run comparison.</div>';
  }
}

window.closeModal = function(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.remove('active');
};
