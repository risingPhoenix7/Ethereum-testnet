from web3 import Web3
import os
from web3.middleware import geth_poa_middleware
import time  # To measure confirmation time
# import secrets as secrets
# Example of connecting to Sepolia via Infura.
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into the environment

node_url = os.getenv("nodeurl")
w3 = Web3(Web3.HTTPProvider(node_url))

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check connection
if w3.is_connected():
    print("Connected to Ethereum node.")
else:
    print("Failed to connect to Ethereum node.")

address = os.getenv("address")
api_key = os.getenv("apiKey")

# Sender's details
from_address = Web3.to_checksum_address(
    address)
private_key = os.getenv("privKey")

# Recipient address (example)
to_address = Web3.to_checksum_address(
    "0xFe6Be457E482CE2B7b8c3BE7BCe32064713f4c5e")

# Transaction details
value = w3.to_wei(0.005, 'ether')  # Sending 0.01 Ether
nonce = w3.eth.get_transaction_count(from_address)
# print(nonce)

# EIP-1559 transaction parameters
transaction = {
    'to': to_address,
    'value': value,
    'nonce': nonce,
    'gas': 240000,
    'data': w3.to_hex(text="Hello, Sepolia!"),
    'maxFeePerGas': w3.to_wei(36, 'gwei'),
    'maxPriorityFeePerGas': w3.to_wei(2, 'gwei'),
    'chainId': w3.eth.chain_id
}

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction and record the current time
tx_sent_time = time.time()
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Output the transaction hash
print(f"Transaction hash: {tx_hash.hex()}")

# Wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Record the time when the transaction was confirmed
tx_confirmed_time = time.time()

# Calculate the confirmation time
confirmation_time = tx_confirmed_time - tx_sent_time
print(f"Transaction confirmed after {confirmation_time} seconds.")

# Connected to Ethereum node.
# Transaction hash: 0x59ac8814e09b6a413969b1e6c0189da82937996e4ce8e94b50eab66c61b96fd6
# Transaction confirmed after 7.226428031921387 seconds.
