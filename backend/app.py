from flask import Flask, request, jsonify, render_template
from blockchain_writer import write_event_to_contract
from web3 import Web3
import os, json
from threading import Thread
from etw_listener import start_etw_listener
from config import GANACHE_URL, CONTRACT_ADDRESS

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), "contract_abi.json")) as f:
    abi = json.load(f)

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
sender_address = w3.eth.accounts[0]

@app.route('/')
def index():
    log_count = contract.functions.getLogCount().call()
    logs = []

    for i in range(log_count):
        event_type, timestamp = contract.functions.getLog(i).call()
        logs.append({"event_type": event_type, "timestamp": timestamp})
    
    return render_template('index.html', logs=logs)

@app.route("/record_event", methods=["POST"])
def record_event():
    data = request.json
    event_type = data.get("event_type")
    timestamp = data.get("timestamp")

    if not event_type or not timestamp:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        tx_hash = write_event_to_contract(event_type, int(timestamp))
        return jsonify({"status": "success", "tx_hash": tx_hash})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/log_event", methods=["POST"])
def log_event():
    try:
        data = request.json     # Get JSON data from POST request
        event_type = data.get("event_type")
        timestamp = data.get("timestamp")
        
        if not event_type or not timestamp:
            return jsonify({"error": "Missing event_type or timestamp"}), 400
        
        event_data = {
            "event_type": event_type,
            "timestamp": timestamp
        }

        return jsonify({"status": "success", "message": "Event recorded"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_logs", methods=["GET"])
def get_logs():
    try:
        log_count = contract.functions.getLogCount().call()
        logs = []

        # Loop through the logs and fetch them
        for i in range(log_count):
            event_type, timestamp = contract.functions.getLog(i).call()
            logs.append({
                "event_type": event_type,
                "timestamp": timestamp
            })

        return jsonify(logs)
    except Exception as e:
        print(f"[!] Error calling getLogCount: {e}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    Thread(target=start_etw_listener, daemon=True).start()
    app.run(debug=True)
