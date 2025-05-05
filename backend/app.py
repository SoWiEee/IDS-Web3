from flask import Flask, request, jsonify, render_template
from blockchain_writer import write_event_to_contract
from web3 import Web3
import os, json, time
from threading import Thread
from etw_listener import start_etw_listener
from config import GANACHE_URL, CONTRACT_ADDRESS

app = Flask(__name__)
logs = []

with open(os.path.join(os.path.dirname(__file__), "contract_abi.json")) as f:
    abi = json.load(f)

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
sender_address = w3.eth.accounts[0]

@app.route('/')
def index():
    log_count = contract.functions.getLogCount().call()

    for i in range(log_count):
        log = contract.functions.getLog(i).call()
        logs.append({
            "event_type": log[0],
            "timestamp": log[1],
            "image": log[2],
            "command_line": log[3],
            "pid": log[4],
            "user": log[5],
            "integrity_level": log[6],
            "parent_image": log[7],
            "hashes": log[8]
        })
    
    return render_template('index.html', logs=logs)

@app.route("/record_event", methods=["POST"])
def record_event():
    data = request.json
    try:
        required_fields = ["event_type", "timestamp", "image", "command_line", "pid", "user", "integrity_level", "parent_image", "hashes"]
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
            data["integrity_level"],
            data["parent_image"],
            data["hashes"]
        )
        return jsonify({"status": "success", "tx_hash": tx_hash})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

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
