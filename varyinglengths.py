import os
import json
import time
import random
import string
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()

# Setup and connection
node_url = os.getenv("nodeurl")
w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Function to generate random string


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to send transaction


def send_transaction(string_length):
    from_address = Web3.to_checksum_address(os.getenv("address"))
    private_key = os.getenv("privkey")
    to_address = Web3.to_checksum_address(
        "0xFe6Be457E482CE2B7b8c3BE7BCe32064713f4c5e")

    data = generate_random_string(string_length)
    nonce = w3.eth.get_transaction_count(from_address)
    transaction = {
        'to': to_address,
        'value': w3.to_wei(0.005, 'ether'),
        'nonce': nonce,
        'gas': 24000000,
        'data': w3.to_hex(text=data),
        'maxFeePerGas': w3.to_wei(36, 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei(2, 'gwei'),
        'chainId': w3.eth.chain_id
    }

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_sent_time = time.time()
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    tx_confirmed_time = time.time()

    confirmation_time = tx_confirmed_time - tx_sent_time
    gas_used = tx_receipt.gasUsed

    print(
        f"Transaction confirmed after {confirmation_time} seconds with gas {gas_used}.")

    # Append transaction details to JSON file
    tx_details = {
        'tx_hash': tx_hash.hex(),
        'string_length': string_length,
        'confirmation_time': confirmation_time,
        'gas_used': gas_used,
    }

    with open("transaction_details.json", "a") as file:
        file.write(json.dumps(tx_details) + "\n")

# Function to plot string length vs confirmation time


def plot_data():
    with open("transaction_details.json", "r") as file:
        lines = file.readlines()
        data = [json.loads(line) for line in lines]

    lengths = [d['string_length'] for d in data]
    times = [d['confirmation_time'] for d in data]

    plt.scatter(lengths, times)
    plt.title('String Length vs Confirmation Time')
    plt.xlabel('String Length')
    plt.ylabel('Confirmation Time (seconds)')
    plt.show()


# Example usage
if __name__ == "__main__":
    if w3.is_connected():
        print("Connected to Ethereum node.")
    else:
        print("Failed to connect to Ethereum node.")
        exit()
    for length in range(500, 1001, 100):
        send_transaction(length)
    plot_data()
