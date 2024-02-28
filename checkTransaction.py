import requests
import os

api_key = os.getenv("apiKey")

def get_transaction_data(txhash, api_key):
    base_url = "https://api-sepolia.etherscan.io/api"
    parameters = {
        "module": "proxy",
        "action": "eth_getTransactionByHash",
        "txhash": txhash,
        "apikey": api_key
    }

    response = requests.get(base_url, params=parameters)
    if response.status_code == 200:
        data = response.json()
        if data["result"]:
            # Assuming 'result' contains the transaction details
            transaction_details = data["result"]
            return transaction_details
        else:
            print("Transaction data not found.")
            return None
    else:
        print(
            f"Failed to retrieve transaction data. Status code: {response.status_code}")
        return None


def from_hex(hex_string):
    return bytes.fromhex(hex_string[2:]).decode('utf-8')


txhash = "0x59ac8814e09b6a413969b1e6c0189da82937996e4ce8e94b50eab66c61b96fd6"
txhash = "0x204fb69834247d1151b322447e81c79e87f10425062bf37a68c389fcd7935864"
txhash = "0x3af6f95a6cae715f01b92452dd988e7866bd03d86e016c1ece245c56e6ffc234"

api_key = "5BQGA5ESDDFAIWD8E42HSW6SHSDBDBUW5R"
transaction_data = get_transaction_data(txhash, api_key)
if transaction_data is not None:
    print("Transaction data retrieved successfully:")
    print(transaction_data)
