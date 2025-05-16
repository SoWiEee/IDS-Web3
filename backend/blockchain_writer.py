from web3 import Web3
import json, os
from config import GANACHE_URL, PRIVATE_KEY, CONTRACT_ADDRESS

with open(os.path.join(os.path.dirname(__file__), "contract_abi.json")) as f:
        abi = json.load(f)

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
sender_address = w3.eth.accounts[0]


def write_logs_to_contract(event_type, timestamp, image, command_line, pid, user, integrity_level):
    tx = contract.functions.recordEvent(
        event_type,
        timestamp,
        image,
        command_line,
        pid,
        user,
        integrity_level
    ).build_transaction({
        "from": sender_address,
        "nonce": w3.eth.get_transaction_count(sender_address),
        "gas": 3000000,
        "gasPrice": w3.to_wei("20", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"[+] Event recorded, tx hash: {w3.to_hex(tx_hash)}")
    return tx_hash.hex()


def get_logs_from_contract():
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
    return logs


def write_maliciousLogs_to_contract(payload):
    try:
        tx = contract.functions.addMaliciousLog(
            payload.get("event_type", ""),
            int(payload.get("timestamp", 0)),
            payload.get("image", ""),
            payload.get("command_line", ""),
            payload.get("pid", ""),
            payload.get("user", ""),
            payload.get("integrity_level", ""),
            payload.get("detail", "")
        ).build_transaction({
            "from": sender_address,
            "nonce": w3.eth.get_transaction_count(sender_address),
            "gas": 3000000,
            "gasPrice": w3.to_wei("20", "gwei")
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"[+] Malicious log recorded, tx hash: {w3.to_hex(tx_hash)}")
        return tx_hash.hex()

    except Exception as e:
        print(f"[!] Failed to write malicious log to contract: {e}")
        return None

