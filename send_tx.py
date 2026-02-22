import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

public_address = os.getenv("MY_PUBLIC_ADDRESS")
private_key = os.getenv("MY_PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))

print("Building transaction...")

# 1. Get your "Nonce" (This prevents replay attacks. It's just the count of txs you've ever sent)
nonce = w3.eth.get_transaction_count(public_address)

# 2. Build the transaction dictionary (The JSON payload)
tx_payload = {
    'nonce': nonce,
    'to': public_address, # We are just sending it to yourself as a test
    'value': w3.to_wei(0.00001, 'ether'), # The amount to send
    'gas': 21000, # Standard compute limit for a simple transfer
    'gasPrice': w3.eth.gas_price, # Ask the network what the current compute fee is
    'chainId': 84532 # 84532 is the official ID for Base Sepolia Testnet
}

# 3. SIGN the payload with your Private Key (This happens entirely locally on your machine!)
signed_tx = w3.eth.account.sign_transaction(tx_payload, private_key)

# 4. Broadcast the signed payload to the network
print("Broadcasting to the network...")
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

# 5. Get the unique transaction ID
hex_hash = w3.to_hex(tx_hash)
print("\n✅ Transaction Successful!")
print(f"View it live on the block explorer: https://sepolia.basescan.org/tx/{hex_hash}")
