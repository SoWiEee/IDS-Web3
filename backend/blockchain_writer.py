from web3 import Web3
import json, os
from config import GANACHE_URL, PRIVATE_KEY, CONTRACT_ADDRESS


with open(os.path.join(os.path.dirname(__file__), "contract_abi.json")) as f:
        abi = json.load(f)

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
sender_address = w3.eth.accounts[0]

def write_event_to_contract(event_type: str, timestamp: int):
    try:
        tx = contract.functions.logEvent(event_type, timestamp).build_transaction({
            'from': sender_address,
            'nonce': w3.eth.get_transaction_count(sender_address),
            'gas': 200000,
            'gasPrice': w3.to_wei('10', 'gwei')
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_str = w3.to_hex(tx_hash)

        print(f"[+] Event recorded, tx hash: {tx_hash_str}")

        return tx_hash_str
    except Exception as e:
        print(f"[-] Failed to write event: {e}")
        raise e

