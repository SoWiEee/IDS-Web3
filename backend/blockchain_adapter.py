from web3 import Web3
import json, os
from config import GANACHE_URL, PRIVATE_KEY, CONTRACT_ADDRESS

# load contract ABI
with open("contract_abi.json", "r") as f:
    abis = json.load(f)
    event_logger_abi = abis["EventLogger"]
    malicious_logger_abi = abis["MaliciousLogger"]

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
normal_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=event_logger_abi)
malicious_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=malicious_logger_abi)
sender_address = w3.eth.accounts[0]


def write_logs_to_contract(event_type, timestamp, image, command_line, pid, user, integrity_level):
    tx = normal_contract.functions.recordEvent(
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
    log_count = normal_contract.functions.getLogCount().call()
    logs = []
    for i in range(log_count):
        event = normal_contract.functions.getLog(i).call()
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
        tx = malicious_contract.functions.addMaliciousLog({
            "event_type": payload["event_type"],
            "timestamp": int(payload["timestamp"]),
            "image": payload["image"],
            "command_line": payload["command_line"],
            "pid": payload["pid"],
            "user": payload["user"],
            "integrity_level": payload["integrity_level"],
            "detail": payload["detail"]
        }).build_transaction({
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


def get_malicious_logs_from_contract():
    try:
        logs_count = malicious_contract.functions.getMaliciousLogCount().call()
        logs = []
        for i in range(logs_count):
            log = malicious_contract.functions.getMaliciousLog(i).call()
            logs.append({
                "event_type": log[0],
                "timestamp": log[1],
                "image": log[2],
                "command_line": log[3],
                "pid": log[4],
                "user": log[5],
                "integrity_level": log[6],
                "detail": log[7]
            })
        return logs
    except Exception as e:
        print(f"[!] Failed to fetch malicious logs: {e}")
        return None
