/**
 * AI Assisted Interview Practice & Evaluation System
 * Research Benchmark & Statistical Comparison Dashboard
 */

let researchData = null;
let sampleAnswersData = [];

window.initResearchDashboard = async function() {
  await loadBenchmarkMetrics();
  await loadSampleAnswers();
};

async function loadBenchmarkMetrics() {
  const container = document.getElementById('benchmark-metrics-container');
  if (!container) return;

  try {
    const res = await fetch('/api/research/benchmark');
    researchData = await res.json();
    renderBenchmarkSummary(researchData);
  } catch (err) {
    console.error("Error loading benchmark:", err);
    container.innerHTML = '<div style="color: var(--accent-rose); padding: 20px;">Failed to load research benchmark data.</div>';
  }
}

function renderBenchmarkSummary(data) {
  const m1 = data.methods.method_1_general;
  const m2 = data.methods.method_2_rubric;
  const m3 = data.methods.method_3_rubric_ref;
  const hb = data.human_baseline;

  // 1. Human Baseline Banner
  const baselineBanner = document.getElementById('human-baseline-banner');
  if (baselineBanner) {
    baselineBanner.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
        <div>
          <span style="font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-cyan); font-weight: 700;">Ground Truth Baseline</span>
          <h4 style="font-family: var(--font-heading); font-size: 1.15rem; color: #fff; margin-top: 4px;">Human Reviewer Consensus (180 Double-Graded Answers)</h4>
          <p style="font-size: 0.85rem; color: var(--text-muted);">Independent rubric evaluations by Reviewer 1 and Reviewer 2.</p>
        </div>
        <div style="display: flex; gap: 24px;">
          <div>
            <div style="font-size: 0.74rem; color: var(--text-muted);">Inter-Rater MAE</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #38bdf8;">${hb.inter_rater_mae.toFixed(3)}</div>
          </div>
          <div>
            <div style="font-size: 0.74rem; color: var(--text-muted);">Pearson r</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #34d399;">${hb.inter_rater_pearson_r.toFixed(3)}</div>
          </div>
          <div>
            <div style="font-size: 0.74rem; color: var(--text-muted);">Cohen's Kappa (κ)</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #a78bfa;">${hb.inter_rater_kappa.toFixed(3)}</div>
          </div>
        </div>
      </div>
    `;
  }

  // 2. Comparative 3-Method Grid
  const methodGrid = document.getElementById('benchmark-methods-grid');
  if (methodGrid) {
    methodGrid.innerHTML = `
      <!-- Method 1: General AI -->
      <div class="glass-card" style="border-top: 4px solid var(--accent-rose);">
        <div style="font-size: 0.8rem; font-weight: 700; color: #fb7185; text-transform: uppercase; margin-bottom: 6px;">Baseline Comparison</div>
        <h3 style="font-family: var(--font-heading); font-size: 1.2rem; margin-bottom: 12px;">Method 1: General AI</h3>
        
        <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px;">
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Mean Absolute Error (MAE):</span>
            <span class="bold" style="color: #fb7185;">${m1.score_error.mae.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Root Mean Square Error (RMSE):</span>
            <span class="bold">${m1.score_error.rmse.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Pearson Correlation (r):</span>
            <span class="bold">${m1.agreement.pearson_r.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Cohen's Kappa (κ):</span>
            <span class="bold">${m1.agreement.cohen_weighted_kappa.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Agreement Within ±1.0 pt:</span>
            <span class="bold">${m1.agreement.within_1pt_percentage}%</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Unsupported Feedback Rate:</span>
            <span class="bold" style="color: #fb7185;">${m1.reliability_and_safety.unsupported_feedback_percentage}%</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Avg Latency / Cost:</span>
            <span class="bold">${m1.operational_metrics.avg_latency_sec}s / $${m1.operational_metrics.avg_cost_usd}</span>
          </div>
        </div>
        <p style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.4;">${m1.metadata.desc}</p>
      </div>

      <!-- Method 2: Rubric AI -->
      <div class="glass-card" style="border-top: 4px solid var(--accent-amber);">
        <div style="font-size: 0.8rem; font-weight: 700; color: #fbbf24; text-transform: uppercase; margin-bottom: 6px;">Structured Rubric</div>
        <h3 style="font-family: var(--font-heading); font-size: 1.2rem; margin-bottom: 12px;">Method 2: Rubric-Based AI</h3>
        
        <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px;">
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Mean Absolute Error (MAE):</span>
            <span class="bold" style="color: #fbbf24;">${m2.score_error.mae.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Root Mean Square Error (RMSE):</span>
            <span class="bold">${m2.score_error.rmse.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Pearson Correlation (r):</span>
            <span class="bold">${m2.agreement.pearson_r.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Cohen's Kappa (κ):</span>
            <span class="bold">${m2.agreement.cohen_weighted_kappa.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Agreement Within ±1.0 pt:</span>
            <span class="bold">${m2.agreement.within_1pt_percentage}%</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Unsupported Feedback Rate:</span>
            <span class="bold" style="color: #fbbf24;">${m2.reliability_and_safety.unsupported_feedback_percentage}%</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Avg Latency / Cost:</span>
            <span class="bold">${m2.operational_metrics.avg_latency_sec}s / $${m2.operational_metrics.avg_cost_usd}</span>
          </div>
        </div>
        <p style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.4;">${m2.metadata.desc}</p>
      </div>

      <!-- Method 3: Rubric + Ref Material -->
      <div class="glass-card" style="border-top: 4px solid var(--accent-emerald); box-shadow: 0 0 25px var(--accent-emerald-glow);">
        <div style="font-size: 0.8rem; font-weight: 700; color: #34d399; text-transform: uppercase; margin-bottom: 6px;">Recommended (PRD Goal)</div>
        <h3 style="font-family: var(--font-heading); font-size: 1.2rem; margin-bottom: 12px;">Method 3: Rubric + Reference</h3>
        
        <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px;">
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Mean Absolute Error (MAE):</span>
            <span class="bold" style="color: #34d399;">${m3.score_error.mae.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Root Mean Square Error (RMSE):</span>
            <span class="bold">${m3.score_error.rmse.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Pearson Correlation (r):</span>
            <span class="bold" style="color: #34d399;">${m3.agreement.pearson_r.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Cohen's Kappa (κ):</span>
            <span class="bold" style="color: #34d399;">${m3.agreement.cohen_weighted_kappa.toFixed(3)}</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Agreement Within ±1.0 pt:</span>
            <span class="bold" style="color: #34d399;">${m3.agreement.within_1pt_percentage}%</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Unsupported Feedback Rate:</span>
            <span class="bold" style="color: #34d399;">${m3.reliability_and_safety.unsupported_feedback_percentage}%</span>
          </div>
          <div class="flex-between">
            <span class="text-muted" style="font-size: 0.86rem;">Avg Latency / Cost:</span>
            <span class="bold">${m3.operational_metrics.avg_latency_sec}s / $${m3.operational_metrics.avg_cost_usd}</span>
          </div>
        </div>
        <p style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.4;">${m3.metadata.desc}</p>
      </div>
    `;
  }

  // 3. Category Breakdown Table
  const catTableBody = document.getElementById('category-breakdown-table-body');
  if (catTableBody) {
    const categories = ["Technical Knowledge", "Workplace Scenarios", "HR / Behavioural"];
    catTableBody.innerHTML = categories.map(cat => {
      const c1 = m1.by_category[cat] || {};
      const c2 = m2.by_category[cat] || {};
      const c3 = m3.by_category[cat] || {};
      return `
        <tr>
          <td style="font-weight: 600; color: #fff;">${cat}</td>
          <td>${c1.mae || '-'} / ${c1.pearson_r || '-'}</td>
          <td>${c2.mae || '-'} / ${c2.pearson_r || '-'}</td>
          <td style="color: #34d399; font-weight: 700;">${c3.mae || '-'} / ${c3.pearson_r || '-'}</td>
          <td>${c1.unsupported_rate}%</td>
          <td>${c2.unsupported_rate}%</td>
          <td style="color: #34d399; font-weight: 700;">${c3.unsupported_rate}%</td>
        </tr>
      `;
    }).join('');
  }

  // Research Summary Conclusion text
  const conclEl = document.getElementById('research-conclusion-text');
  if (conclEl) {
    conclEl.textContent = data.summary_conclusion;
  }
}

// Load 180 Sample Answers Table
async function loadSampleAnswers() {
  const tableBody = document.getElementById('sample-answers-table-body');
  if (!tableBody) return;

  try {
    const res = await fetch('/api/research/sample-answers?limit=180');
    const data = await res.json();
    sampleAnswersData = data.sample_answers || [];
    renderSampleAnswersTable(sampleAnswersData);
  } catch (err) {
    console.error("Error loading sample answers:", err);
  }
}

function renderSampleAnswersTable(list) {
  const tableBody = document.getElementById('sample-answers-table-body');
  if (!tableBody) return;

  tableBody.innerHTML = list.slice(0, 50).map(row => `
    <tr style="cursor: pointer;" onclick="openSampleAnswerModal('${row.sample_id}')">
      <td style="font-family: monospace; color: var(--text-accent);">${row.sample_id}</td>
      <td><span class="q-id-tag">${row.question_id}</span></td>
      <td><span style="font-size: 0.78rem;">${row.category}</span></td>
      <td><span class="q-diff-tag diff-${row.performance_level === 'Excellent' ? 'Junior' : (row.performance_level === 'Proficient' ? 'Mid-Level' : 'Senior')}">${row.performance_level}</span></td>
      <td style="font-weight: 600;">${row.human_consensus ? row.human_consensus.toFixed(2) : '-'}</td>
      <td>${row.m1_score ? row.m1_score.toFixed(2) : '-'}</td>
      <td>${row.m2_score ? row.m2_score.toFixed(2) : '-'}</td>
      <td style="color: #34d399; font-weight: 700;">${row.m3_score ? row.m3_score.toFixed(2) : '-'}</td>
      <td><button class="btn-secondary" style="padding: 4px 10px; font-size: 0.75rem;">Inspect</button></td>
    </tr>
  `).join('');

  const countTag = document.getElementById('table-count-label');
  if (countTag) {
    countTag.textContent = `Showing 50 of ${list.length} Documented Sample Answers`;
  }
}

window.filterSampleAnswers = function() {
  const catFilter = document.getElementById('filter-category').value;
  const perfFilter = document.getElementById('filter-performance').value;

  let filtered = sampleAnswersData;
  if (catFilter) {
    filtered = filtered.filter(x => x.category === catFilter);
  }
  if (perfFilter) {
    filtered = filtered.filter(x => x.performance_level === perfFilter);
  }
  renderSampleAnswersTable(filtered);
};

window.openSampleAnswerModal = function(sampleId) {
  const row = sampleAnswersData.find(x => x.sample_id === sampleId);
  if (!row) return;

  const modal = document.getElementById('sample-detail-modal');
  modal.classList.add('active');

  document.getElementById('modal-sample-id').textContent = `${row.sample_id} (${row.question_id} - ${row.category})`;
  document.getElementById('modal-q-text').textContent = row.question_text;
  document.getElementById('modal-answer-text').textContent = row.answer_text;
  document.getElementById('modal-source-info').textContent = `Source: ${row.source_type} • Level: ${row.performance_level} • Notes: ${row.notes || 'N/A'}`;

  // Scores
  document.getElementById('modal-score-r1').textContent = row.r1_score ? row.r1_score.toFixed(2) : '-';
  document.getElementById('modal-score-r2').textContent = row.r2_score ? row.r2_score.toFixed(2) : '-';
  document.getElementById('modal-score-consensus').textContent = row.human_consensus ? row.human_consensus.toFixed(2) : '-';
  document.getElementById('modal-score-m1').textContent = row.m1_score ? row.m1_score.toFixed(2) : '-';
  document.getElementById('modal-score-m2').textContent = row.m2_score ? row.m2_score.toFixed(2) : '-';
  document.getElementById('modal-score-m3').textContent = row.m3_score ? row.m3_score.toFixed(2) : '-';
};
