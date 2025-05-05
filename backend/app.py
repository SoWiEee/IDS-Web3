from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from blockchain_writer import write_event_to_contract
from web3 import Web3
import os, json, time
from threading import Thread
from etw_listener import start_etw_listener
from config import GANACHE_URL, CONTRACT_ADDRESS

app = Flask(__name__)
CORS(app)  # allow vue call API
logs = []

with open(os.path.join(os.path.dirname(__file__), "contract_abi.json")) as f:
    abi = json.load(f)

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
sender_address = w3.eth.accounts[0]


@app.route("/")
def index():
    return "Backend API is running."


@app.route("/api/record_event", methods=["POST"])
def record_event():
    data = request.json

    try:
        required_fields = ["event_type", "timestamp", "image", "command_line", "pid", "user", "integrity_level"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        tx_hash = write_event_to_contract(
            data["event_type"],
            int(data["timestamp"]),
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
    log_count = contract.functions.getLogCount().call()
    logs = []
    for i in range(log_count):
        event = contract.functions.getLog(i).call()
        logs.append({
            "event_type": event[0],
            "timestamp": event[1],
            "image": event[2],
            "command_line": event[3],
            "pid": event[4],
            "user": event[5],
            "integrity_level": event[6],
        })
    return jsonify(logs)

if __name__ == "__main__":
    Thread(target=start_etw_listener, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
