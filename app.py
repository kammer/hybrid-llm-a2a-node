import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

public_address = os.getenv("MY_PUBLIC_ADDRESS")
# This URL points your script specifically to the Base Sepolia network
RPC_URL = "https://sepolia.base.org"

# Connect to the RPC node
w3 = Web3(Web3.HTTPProvider(RPC_URL))
print(f"Connected to Base Sepolia: {w3.is_connected()}")

# Fetch your balance
balance_wei = w3.eth.get_balance(public_address)
balance_eth = w3.from_wei(balance_wei, 'ether')

print(f"Agent Address: {public_address}")
print(f"Agent Compute Balance: {balance_eth} Testnet ETH")
