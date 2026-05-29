from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import threading
from config import UPLOAD_DIR
from agents.doc_processor import ingest_document
from crew.orchestrator import run_query
from models.db_models import Session, ChatMessage, ExtractedData

app = Flask(__name__)
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)
    vectordb, raw_text = ingest_document(filepath)
    session = Session()
    record = ExtractedData(filename=filename, raw_text=raw_text)
    session.add(record)
    session.commit()
    session.close()
    return jsonify({"status": "ok", "filename": filename})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    session = Session()
    session.add(ChatMessage(role='user', content=user_message))
    session.commit()
    response = run_query(user_message)
    session.add(ChatMessage(role='assistant', content=response))
    session.commit()
    session.close()
    return jsonify({"response": response})

@app.route('/history', methods=['GET'])
def history():
    session = Session()
    messages = session.query(ChatMessage).order_by(ChatMessage.timestamp).all()
    result = [{"role": m.role, "content": m.content, "timestamp": str(m.timestamp)} for m in messages]
    session.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)