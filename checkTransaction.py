
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

node_url = os.getenv("nodeurl")
headers = {
    "Content-Type": "application/json"
}


def get_transaction_data(txhash):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionByHash",
        "params": [txhash],
        "id": 1
    }

    response = requests.post(
        node_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("result"):
            transaction_details = data["result"]
            return transaction_details
        else:
            print("Transaction data not found.")
            return None
    else:
        print(
            f"Failed to retrieve transaction data. Status code: {response.status_code}")
        return None


txhash = "0x3af6f95a6cae715f01b92452dd988e7866bd03d86e016c1ece245c56e6ffc234"
transaction_data = get_transaction_data(txhash)
if transaction_data is not None:
    print("Transaction data retrieved successfully:")
    print(bytes.fromhex(transaction_data['input'][2:]).decode('utf-8'))
