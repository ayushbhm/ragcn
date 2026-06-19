from flask import Blueprint, jsonify, request, current_app
import uuid
import traceback
import os

os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

from ingest import extract_text, chunk_docs, embed_and_store
from rag import get_rag_chain

main = Blueprint('main', __name__)

@main.route('/session', methods=['GET'])
def get_session():
    return jsonify({'session_id': str(uuid.uuid4())})

@main.route('/ingest', methods=['POST'])
def ingest():
    try:
        
        file = request.files['file']
        session_id = request.form['session_id']
        docs = extract_text(file)
        chunks = chunk_docs(docs)
        embed_and_store(chunks, session_id)
        return jsonify({'success': True})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
@main.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id')
        question = data.get('question')
        print("Data received:", data)
        print("Session ID:", session_id)
        print("Question:", question)
        if not session_id or not question:
            return jsonify({'error': 'session_id and question are required'}), 400
        chain = get_rag_chain(session_id)
        answer = chain.invoke(question)
        return jsonify({'answer': answer})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
