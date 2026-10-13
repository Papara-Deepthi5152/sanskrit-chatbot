"""
Vāgdevī - Sanskrit Conversational AI Chatbot
Flask Web Application & API Server
"""

import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from flask import Flask, render_template, request, jsonify
from engine.dialogue_manager import DialogueManager
from engine.transliteration import to_devanagari, to_iast, normalize_sanskrit
from engine.knowledge_base import (
    SUBHASHITA_COLLECTION, SHABDARUPA_DATA, DHATURUPA_DATA, SANDHI_RULES
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sanskrit-vagdevi-secret-key-2026'

# Global dialogue manager instance
dm = DialogueManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400

    response = dm.process_message(message)
    return jsonify(response)

@app.route('/api/shloka-of-the-day', methods=['GET'])
def shloka_of_the_day():
    import random
    shloka = random.choice(SUBHASHITA_COLLECTION)
    return jsonify(shloka)

@app.route('/api/quiz/question', methods=['GET'])
def quiz_question():
    q = dm.quiz.get_random_question()
    dm.context["active_quiz"] = q["id"]
    return jsonify(q)

@app.route('/api/quiz/answer', methods=['POST'])
def quiz_answer():
    data = request.get_json(silent=True) or {}
    qid = data.get('qid')
    answer_idx = data.get('answer_idx')

    if qid is None or answer_idx is None:
        return jsonify({"error": "Missing qid or answer_idx"}), 400

    result = dm.quiz.evaluate_answer(qid, int(answer_idx))
    dm.context["quiz_score"]["total"] += 1
    if result.get("is_correct"):
        dm.context["quiz_score"]["correct"] += 1

    result["score"] = dm.context["quiz_score"]
    return jsonify(result)

@app.route('/api/transliterate', methods=['POST'])
def transliterate():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '').strip()
    deva = to_devanagari(text)
    iast = to_iast(deva)
    return jsonify({
        "original": text,
        "devanagari": deva,
        "iast": iast
    })

@app.route('/api/sandhi', methods=['POST'])
def sandhi_join():
    data = request.get_json(silent=True) or {}
    word1 = data.get('word1', '').strip()
    word2 = data.get('word2', '').strip()

    if not word1 or not word2:
        return jsonify({"error": "Both words required"}), 400

    res = dm.sandhi.join_words(word1, word2)
    return jsonify(res)

@app.route('/api/grammar/shabda/<name>', methods=['GET'])
def get_shabda(name):
    data = dm.grammar.lookup_shabda(name)
    if not data:
        return jsonify({"error": "Word not found"}), 404
    return jsonify(data)

@app.route('/api/grammar/dhatu/<name>', methods=['GET'])
def get_dhatu(name):
    data = dm.grammar.lookup_dhatu(name)
    if not data:
        return jsonify({"error": "Dhatu not found"}), 404
    return jsonify(data)

@app.route('/api/rules/sandhi', methods=['GET'])
def get_sandhi_rules():
    return jsonify(SANDHI_RULES)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Sanskrit Vagdevi Chatbot server on port {port}...")
    app.run(host='127.0.0.1', port=port, debug=False)
