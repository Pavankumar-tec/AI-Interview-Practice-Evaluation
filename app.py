"""Local teaching prototype. Research collection uses the separate study CLI."""
import json
import os
import sqlite3
import uuid
from flask import Flask, jsonify, render_template, request
from config import DATABASE_PATH
from services.learning import PACKS, PACK_MAP, public_state, question_for
from services.evaluator import evaluate_interview_response

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100_000


def connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('CREATE TABLE IF NOT EXISTS learning_sessions (id TEXT PRIMARY KEY, concept_id TEXT NOT NULL, stage TEXT NOT NULL, history TEXT NOT NULL)')
    return conn


@app.get('/')
def index():
    return render_template('coach.html')


@app.get('/api/concepts')
def concepts():
    return jsonify([{'id': p['id'], 'title': p['title'], 'status': p['status']} for p in PACKS])


@app.post('/api/learning/start')
def start():
    data = request.get_json() or {}
    cid = data.get('concept_id')
    if cid not in PACK_MAP:
        return jsonify(error='Choose a valid concept.'), 400
    sid = str(uuid.uuid4())
    with connection() as conn:
        conn.execute('INSERT INTO learning_sessions VALUES (?, ?, ?, ?)', (sid, cid, 'explain', '[]'))
        record = conn.execute('SELECT * FROM learning_sessions WHERE id=?', (sid,)).fetchone()
    return jsonify(public_state(record))


@app.get('/api/learning/<sid>')
def state(sid):
    with connection() as conn:
        record = conn.execute('SELECT * FROM learning_sessions WHERE id=?', (sid,)).fetchone()
    if record is None:
        return jsonify(error='Session not found.'), 404
    return jsonify(public_state(record))


@app.post('/api/learning/<sid>/advance')
def advance(sid):
    data = request.get_json() or {}
    with connection() as conn:
        record = conn.execute('SELECT * FROM learning_sessions WHERE id=?', (sid,)).fetchone()
    if record is None:
        return jsonify(error='Session not found.'), 404
    stage = record['stage']
    if stage == 'complete' or data.get('stage') != stage:
        return jsonify(error='Stage changed. Reload the session before submitting.'), 409
    answer = data.get('answer', '')
    if not isinstance(answer, str) or not answer.strip() or len(answer) > 10000:
        return jsonify(error='Enter an answer or learning reflection (1–10,000 characters).'), 400
    pack = PACK_MAP[record['concept_id']]
    history = json.loads(record['history'])
    entry = {'stage': stage, 'answer': answer.strip()}
    if stage != 'learn':
        provider = os.environ.get('LLM_PROVIDER', 'offline_semantic')
        config = {'provider': provider, 'model': os.environ.get('LLM_MODEL'), 'api_key': os.environ.get('LLM_API_KEY')}
        if provider != 'offline_semantic' and (not config['model'] or not config['api_key']):
            return jsonify(error='Live mode requires server LLM_MODEL and LLM_API_KEY.'), 503
        try:
            entry['evaluation'] = evaluate_interview_response(question_for(pack, stage), answer, provider_config=config)
            # Raw provider output stays out of the student interface.
            entry['evaluation'].pop('raw_response', None)
        except (RuntimeError, ValueError) as exc:
            return jsonify(error=str(exc)), 502
    history.append(entry)
    next_stage = {'explain':'defend', 'defend':'learn', 'learn':'transfer', 'transfer':'complete'}[stage]
    with connection() as conn:
        updated = conn.execute('UPDATE learning_sessions SET stage=?, history=? WHERE id=? AND stage=?',
            (next_stage, json.dumps(history), sid, stage))
        if updated.rowcount != 1:
            return jsonify(error='Another submission already advanced this session.'), 409
        record = conn.execute('SELECT * FROM learning_sessions WHERE id=?', (sid,)).fetchone()
    return jsonify(public_state(record))


@app.get('/api/learning/<sid>/export')
def export(sid):
    response = state(sid)
    if isinstance(response, tuple):
        return response
    response.headers['Content-Disposition'] = 'attachment; filename=learning-session.json'
    return response


@app.get('/api/research/benchmark')
def research_status():
    return jsonify(status='not_measured', methods={},
        summary_conclusion='No research findings are claimed. Use the study CLI with a frozen dataset, live model runs, and independent human reviews. Classroom sessions are not automatically research data.')


if __name__ == '__main__':
    app.run(host=os.environ.get('HOST', '127.0.0.1'), port=int(os.environ.get('PORT', 5000)), debug=False)
