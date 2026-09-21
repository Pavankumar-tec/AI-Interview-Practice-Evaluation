import os
import sys
import json
import uuid
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import pandas as pd
import io

from config import Config
from database import get_db_connection, init_db
from services.evaluator import evaluate_interview_response
from services.research_service import compute_research_benchmark, get_sample_answers_table

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

# --- CATEGORIES & QUESTIONS ---
@app.route("/api/categories", methods=["GET"])
def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT category, COUNT(*) as count 
    FROM questions 
    GROUP BY category
    """)
    rows = cursor.fetchall()
    conn.close()
    return jsonify({
        "categories": [
            {
                "name": r["category"], 
                "count": r["count"],
                "icon": "code" if "Technical" in r["category"] else ("briefcase" if "Workplace" in r["category"] else "users")
            }
            for r in rows
        ]
    })

@app.route("/api/questions", methods=["GET"])
def get_questions():
    category = request.args.get("category")
    difficulty = request.args.get("difficulty")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id, pack_id, category, question_text, rubric_json, reference_material, difficulty, keywords_json, question_type, options_json, correct_option, explanation FROM questions WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)
    query += " ORDER BY id ASC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    questions = []
    for r in rows:
        q_obj = {
            "id": r["id"],
            "pack_id": r["pack_id"],
            "category": r["category"],
            "question_text": r["question_text"],
            "rubric": json.loads(r["rubric_json"]),
            "reference_material": r["reference_material"],
            "difficulty": r["difficulty"],
            "keywords": json.loads(r["keywords_json"]) if r["keywords_json"] else [],
            "question_type": r["question_type"] or "descriptive",
            "options": json.loads(r["options_json"]) if r["options_json"] else None,
            "correct_option": r["correct_option"],
            "explanation": r["explanation"]
        }
        questions.append(q_obj)
    return jsonify({"questions": questions})

@app.route("/api/questions/<qid>", methods=["GET"])
def get_question_detail(qid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (qid,))
    r = cursor.fetchone()
    conn.close()
    if not r:
        return jsonify({"error": "Question not found"}), 404
        
    return jsonify({
        "id": r["id"],
        "pack_id": r["pack_id"],
        "category": r["category"],
        "question_text": r["question_text"],
        "rubric": json.loads(r["rubric_json"]),
        "reference_material": r["reference_material"],
        "difficulty": r["difficulty"],
        "keywords": json.loads(r["keywords_json"]) if r["keywords_json"] else [],
        "question_type": r["question_type"] or "descriptive",
        "options": json.loads(r["options_json"]) if r["options_json"] else None,
        "correct_option": r["correct_option"],
        "explanation": r["explanation"]
    })

# --- INTERVIEW SESSION & EVALUATION ---
@app.route("/api/sessions/start", methods=["POST"])
def start_session():
    data = request.get_json() or {}
    candidate_name = data.get("candidate_name", "Student Candidate")
    category = data.get("category", "Technical Knowledge")
    pack_id = data.get("pack_id", "pack-tech-01")
    session_id = str(uuid.uuid4())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO interview_sessions (id, candidate_name, category, pack_id, status)
    VALUES (?, ?, ?, ?, 'active')
    """, (session_id, candidate_name, category, pack_id))
    conn.commit()
    conn.close()
    
    return jsonify({
        "session_id": session_id,
        "candidate_name": candidate_name,
        "category": category
    })

@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json() or {}
    session_id = data.get("session_id", "demo-session")
    question_id = data.get("question_id")
    answer_text = data.get("answer_text", "").strip()
    evaluation_method = data.get("evaluation_method", "method_3_rubric_ref")
    followup_answer = data.get("followup_answer")
    provider_config = data.get("provider_config") # optional live LLM config
    
    if not question_id or not answer_text:
        return jsonify({"error": "question_id and answer_text are required"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    q_row = cursor.fetchone()
    if not q_row:
        conn.close()
        return jsonify({"error": "Question not found"}), 404
        
    question_dict = dict(q_row)
    
    # Run evaluation
    eval_result = evaluate_interview_response(
        question=question_dict,
        answer_text=answer_text,
        evaluation_method=evaluation_method,
        followup_answer=followup_answer,
        provider_config=provider_config
    )
    
    # Store candidate answer
    cursor.execute("""
    INSERT INTO candidate_answers (session_id, question_id, answer_text, followup_question, followup_answer)
    VALUES (?, ?, ?, ?, ?)
    """, (session_id, question_id, answer_text, eval_result.get("followup_question"), followup_answer))
    answer_id = cursor.lastrowid
    
    # Store evaluation record
    cursor.execute("""
    INSERT INTO evaluations (
        answer_id, evaluation_method, overall_score, criterion_scores_json, evidence_quotes_json,
        suggestions_json, followup_question, clarification_needed, review_flag,
        unsupported_feedback_count, latency_ms, token_cost
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        answer_id,
        evaluation_method,
        eval_result["overall_score"],
        json.dumps(eval_result["criterion_scores"]),
        json.dumps(eval_result["evidence_quotes"]),
        json.dumps(eval_result["suggestions"]),
        eval_result.get("followup_question"),
        1 if eval_result.get("clarification_needed") else 0,
        1 if eval_result.get("review_flag") else 0,
        eval_result.get("unsupported_feedback_count", 0),
        eval_result.get("latency_ms", 0),
        eval_result.get("token_cost", 0.0)
    ))
    eval_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    eval_result["evaluation_id"] = eval_id
    eval_result["answer_id"] = answer_id
    return jsonify(eval_result)

@app.route("/api/compare-methods", methods=["POST"])
def compare_methods():
    """
    Evaluates the submitted answer using all 3 methods side-by-side:
    - Method 1: General AI Prompting
    - Method 2: Rubric-Based AI
    - Method 3: Rubric + Supporting Reference Material
    """
    data = request.get_json() or {}
    question_id = data.get("question_id")
    answer_text = data.get("answer_text", "").strip()
    
    if not question_id or not answer_text:
        return jsonify({"error": "question_id and answer_text are required"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    q_row = cursor.fetchone()
    conn.close()
    if not q_row:
        return jsonify({"error": "Question not found"}), 404
        
    question_dict = dict(q_row)
    
    m1 = evaluate_interview_response(question_dict, answer_text, "method_1_general")
    m2 = evaluate_interview_response(question_dict, answer_text, "method_2_rubric")
    m3 = evaluate_interview_response(question_dict, answer_text, "method_3_rubric_ref")
    
    return jsonify({
        "question_id": question_id,
        "question_text": question_dict["question_text"],
        "answer_text": answer_text,
        "comparisons": {
            "method_1_general": m1,
            "method_2_rubric": m2,
            "method_3_rubric_ref": m3
        }
    })

# --- RESEARCH BENCHMARK & HUMAN REVIEW ---
@app.route("/api/research/benchmark", methods=["GET"])
def get_research_benchmark():
    benchmark_data = compute_research_benchmark()
    return jsonify(benchmark_data)

@app.route("/api/research/sample-answers", methods=["GET"])
def get_sample_answers():
    limit = int(request.args.get("limit", 180))
    cat = request.args.get("category")
    perf = request.args.get("performance_level")
    answers = get_sample_answers_table(limit=limit, category=cat, performance_level=perf)
    return jsonify({"total": len(answers), "sample_answers": answers})

@app.route("/api/reviewer/submit", methods=["POST"])
def submit_human_review():
    data = request.get_json() or {}
    sample_id = data.get("sample_id")
    reviewer_id = data.get("reviewer_id", "reviewer_1")
    overall_score = float(data.get("overall_score", 0.0))
    criterion_scores = data.get("criterion_scores", {})
    feedback_notes = data.get("feedback_notes", "")
    
    if not sample_id or overall_score <= 0:
        return jsonify({"error": "sample_id and valid overall_score are required"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO human_reviews (sample_id, reviewer_id, overall_score, criterion_scores_json, feedback_notes)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(sample_id, reviewer_id) DO UPDATE SET
        overall_score = excluded.overall_score,
        criterion_scores_json = excluded.criterion_scores_json,
        feedback_notes = excluded.feedback_notes,
        created_at = CURRENT_TIMESTAMP
    """, (sample_id, reviewer_id, overall_score, json.dumps(criterion_scores), feedback_notes))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "message": f"Review saved successfully for {reviewer_id}"})

# --- EXTENSIBILITY: QUESTION PACKS ---
@app.route("/api/questions/create", methods=["POST"])
def create_question():
    data = request.get_json() or {}
    qid = data.get("id") or f"CUSTOM-{uuid.uuid4().hex[:6].upper()}"
    pack_id = data.get("pack_id", "pack-custom")
    category = data.get("category", "Technical Knowledge")
    question_text = data.get("question_text")
    rubric = data.get("rubric", [])
    ref_material = data.get("reference_material", "")
    difficulty = data.get("difficulty", "Mid-Level")
    keywords = data.get("keywords", [])
    
    if not question_text or not rubric:
        return jsonify({"error": "question_text and rubric are required"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO questions (id, pack_id, category, question_text, rubric_json, reference_material, difficulty, keywords_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (qid, pack_id, category, question_text, json.dumps(rubric), ref_material, difficulty, json.dumps(keywords)))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "question_id": qid})

# --- EXPORT DATASET (CSV / JSON) ---
@app.route("/api/export/research-data", methods=["GET"])
def export_research_data():
    format_type = request.args.get("format", "csv").lower()
    answers = get_sample_answers_table(limit=180)
    df = pd.DataFrame(answers)
    
    if format_type == "json":
        return jsonify(answers)
    else:
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode("utf-8")),
            mimetype="text/csv",
            as_attachment=True,
            download_name="ai_interview_research_180_dataset.csv"
        )

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting AI Assisted Interview Practice & Evaluation server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
