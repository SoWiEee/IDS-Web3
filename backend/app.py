from flask import Flask, request, jsonify
from config import GEMINI_API_KEY
import google.generativeai as genai
from flask_cors import CORS
from blockchain_adapter import write_logs_to_contract, get_logs_from_contract, write_maliciousLogs_to_contract, get_malicious_logs_from_contract
from threading import Thread
from etw_listener import listen_security_log, listen_sysmon, listen_sysmon_registry


app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])    # allow Vue call API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route("/")
def index():
    return "[V] Backend API is running!"

@app.route('/api/analyze', methods=['POST'])
def analyze_logs():
    try:
        data = request.get_json()
        logs = data.get('logs', [])
        if not logs:
            return jsonify({'result': '⚠️ 沒有收到任何紀錄資料'}), 400
        
        summary = "\n".join(
            f"{log.get('timestamp', '')} | {log.get('event_type', '')} | {log.get('command_line', '')}"
            for log in logs
        )

        prompt = f"""你是一個資安分析助理，請根據以下紀錄判斷是否有異常或惡意事件，並用繁體中文解釋：
{summary}
請指出可疑事件的時間、類型及可能風險。限制在 120 字內。"""

        # send prompt
        response = model.generate_content(prompt)

        return jsonify({'result': response.text})

    except Exception as e:
        return jsonify({'message': f'分析過程發生錯誤: {str(e)}'}), 500



@app.route("/api/logs", methods=["POST"])
def create_logs():
    data = request.json

    try:
        required_fields = ["event_type", "timestamp", "image", "command_line", "pid", "user", "integrity_level"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        tx_hash = write_logs_to_contract(
            data["event_type"],
            data["timestamp"],
            data["image"],
            data["command_line"],
            data["pid"],
            data["user"],
            data["integrity_level"]
        )
        return jsonify({"status": "success", "tx_hash": tx_hash})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/logs", methods=["GET"])
def get_logs():
    try:
        logs = get_logs_from_contract()
        if not logs:
            return jsonify({"status": "error", "message": "No logs found"}), 404
        return jsonify(logs)
    except Exception as e:
        print("[X] Failed to fetch logs:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/malicious', methods=['GET'])
def get_malicious_logs():
    try:
        logs = get_malicious_logs_from_contract()
        if not logs:
            return jsonify({"status": "error", "message": "No malicious logs found"}), 404
        return jsonify(logs)
    except Exception as e:
        print("[X] Failed to fetch malicious logs:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/malicious', methods=['POST'])
def write_malicious_log():
    try:
        payload = request.get_json()

        if not payload:
            return jsonify({"error": "No payload provided"}), 400

        tx_hash = write_maliciousLogs_to_contract(payload)

        return jsonify({"status": "ok", "tx_hash": tx_hash}), 200
    except Exception as e:
        print(f"[!] Error handling malicious log: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    Thread(target=listen_security_log, daemon=True).start()
    Thread(target=listen_sysmon, daemon=True).start()
    Thread(target=listen_sysmon_registry, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
