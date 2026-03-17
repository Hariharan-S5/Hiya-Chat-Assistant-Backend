

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import db
import json as _json

app = Flask(__name__)
# Allow CORS from your frontend (React)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

OLLAMA_URL = "http://localhost:11434/api/chat"  # Local Ollama server
MODEL_NAME = "phi3"

# Import db functions
import db

create_tables = db.create_tables

@app.route('/api/checkuser', methods=['POST'])
def check_user():
    try:
        import json as _json
        data = request.get_json()
        print("Received data:", data)
        mailid = data.get('mailid')
        if not mailid:
            return jsonify({'status': 'error', 'error': 'mailid required'}), 400

        conn = db.get_connection(use_memory=False, db_file="database.db")
        db.create_tables(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM user_profile WHERE mail_id = ?", (mailid,))
        row = cursor.fetchone()
        if row:
            user_id = row[0]
        else:
            cursor.execute("INSERT INTO user_profile (mail_id) VALUES (?)", (mailid,))
            conn.commit()
            cursor.execute("SELECT user_id FROM user_profile WHERE mail_id = ?", (mailid,))
            row = cursor.fetchone()
            user_id = row[0]

        # Check for chat_history
        cursor.execute("SELECT history FROM chat_history WHERE user_id = ?", (user_id,))
        history_row = cursor.fetchone()
        if history_row:
            try:
                history_json = _json.loads(history_row[0])
            except Exception:
                history_json = {"Current conversation to HarryConnect": {"history": [],"timestamp": "2024-06-19T12:00:00Z"}}
            response = {'status': 'success', 'user_id': user_id, 'chat_history': history_json}
        else:
            # Insert empty history as object
            cursor.execute("INSERT INTO chat_history (user_id, history) VALUES (?, ?)", (user_id, _json.dumps({})))
            conn.commit()
            history_json = {"Current conversation to HarryConnect": {"history": [],"timestamp": "2024-06-19T12:00:00Z"}}
            response = {'status': 'success', 'user_id': user_id, 'chat_history': history_json}
        conn.close()
        return jsonify(response)
    except Exception as e:
        print("Error in check_user:", str(e))
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/savehistory', methods=['POST'])
def save_history():
    try:
        data = request.get_json()
        user_id = data.get('userid')
        histories = data.get('histories')
        if user_id is None or histories is None:
            return jsonify({'status': 'error', 'error': 'userid and histories required'}), 400

        
        conn = db.get_connection(use_memory=False, db_file="database.db")
        db.create_tables(conn)
        cursor = conn.cursor()
        # Check if user exists
        cursor.execute("SELECT user_id FROM user_profile WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'status': 'error', 'error': 'user_id not found'}), 404

        # Update or insert chat_history
        cursor.execute("SELECT history FROM chat_history WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            cursor.execute("UPDATE chat_history SET history = ? WHERE user_id = ?", (_json.dumps(histories), user_id))
        else:
            cursor.execute("INSERT INTO chat_history (user_id, history) VALUES (?, ?)", (user_id, _json.dumps(histories)))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    except Exception as e:
        print("Error in save_history:", str(e))
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        # Preflight CORS request
        return jsonify({'status': 'success'}), 200

    try:
        data = request.json
        user_message = data['message']
        conversation_history = data.get('history', [])

        # Format messages for Ollama
        messages = [
            {"role": msg['role'], "content": msg['content']}
            for msg in conversation_history
        ]
        messages.append({"role": "user", "content": user_message})

        # Call local Ollama server
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False
            },
            headers={"Content-Type": "application/json"},
            timeout=120
        )

        result = response.json()
        print("Ollama Response:", result)

        return jsonify({
            "response": result["message"]["content"],
            "status": "success"
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500


if __name__ == '__main__':
    print("Starting Flask server on port 5000...")
    app.run(debug=True, port=5000)