import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()


def get_eth_balance(address, node_url):
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        # "latest" can be replaced with the block number
        "params": [address, "latest"],
        "id": 1
    }

    response = requests.post(node_url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("result"):
            # The balance will be in Wei, and as a hex string
            balance_wei = int(data["result"], 16)
            balance_eth = balance_wei / 1e18  # Convert Wei to Ether
            return balance_eth
        else:
            print("Error fetching balance.")
            return None
    else:
        print(
            f"Failed to retrieve balance. Status code: {response.status_code}, Response: {response.text}")
        return None


# Fetch environment variables for address and node_url
address = os.getenv("address")
node_url = os.getenv("nodeurl")

if not address or not node_url:
    raise ValueError(
        "Environment variables for 'address' or 'nodeurl' are not set.")

balance_eth = get_eth_balance(address, node_url)
if balance_eth is not None:
    print(f"Balance: {balance_eth} ETH")
else:
    print("Failed to retrieve balance.")
