import requests
import os

api_key = os.getenv("apiKey")

def get_eth_balance(address, api_key):
    base_url = "https://api-sepolia.etherscan.io/api"
    parameters = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": api_key
    }

    response = requests.get(base_url, params=parameters)
    if response.status_code == 200:
        data = response.json()
        print(data)
        # Convert balance from Wei to Ether
        balance = int(data["result"]) / 1e18
        return balance
    else:
        print(
            f"Failed to retrieve balance. Status code: {response.status_code}")
        return None


address = os.getenv("address")
api_key = os.getenv("apiKey")

balance = get_eth_balance(address, api_key)
if balance is not None:
    print(f"Balance for {address}: {balance} ETH")
