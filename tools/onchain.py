"""
tools/onchain.py
Reads the native ETH balance of a wallet from Base Sepolia.
Pure read — no private key required.
"""

from web3 import Web3

# --- Config -----------------------------------------------------------

RPC_URL        = "https://sepolia.base.org"
DEFAULT_WALLET = "0x072C12957983104891DCEB9C1C90dD94eda7Ca8C"  # Raimund Kammering

# --- Core -------------------------------------------------------------

def get_eth_balance(address: str = DEFAULT_WALLET) -> dict:
    """
    Fetch the native ETH balance of a wallet on Base Sepolia.

    Returns a dict:
        {
            "address": str,
            "balance_wei": int,
            "balance_eth": float,
            "network":     "Base Sepolia",
        }
    """
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to RPC: {RPC_URL}")

    checksum_address = Web3.to_checksum_address(address)
    balance_wei      = w3.eth.get_balance(checksum_address)
    balance_eth      = float(Web3.from_wei(balance_wei, "ether"))

    return {
        "address":     checksum_address,
        "balance_wei": balance_wei,
        "balance_eth": balance_eth,
        "network":     "Base Sepolia",
    }


def get_current_gas_price() -> dict:
    """
    Fetch the current gas price on Base Sepolia.
    Useful context when deciding whether to transact.

    Returns a dict:
        {
            "gas_price_wei":  int,
            "gas_price_gwei": float,
        }
    """
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to RPC: {RPC_URL}")

    gas_wei  = w3.eth.gas_price
    gas_gwei = float(Web3.from_wei(gas_wei, "gwei"))

    return {
        "gas_price_wei":  gas_wei,
        "gas_price_gwei": gas_gwei,
    }


# --- Entry point (standalone test) ------------------------------------

if __name__ == "__main__":
    print("=== Wallet Balance ===")
    balance = get_eth_balance()
    print(f"Address:  {balance['address']}")
    print(f"Network:  {balance['network']}")
    print(f"Balance:  {balance['balance_eth']:.6f} ETH")
    print(f"          ({balance['balance_wei']} wei)")

    print()
    print("=== Gas Price ===")
    gas = get_current_gas_price()
    print(f"Gas:      {gas['gas_price_gwei']:.4f} Gwei")
