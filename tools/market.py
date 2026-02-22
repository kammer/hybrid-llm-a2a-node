"""
tools/market.py
Reads the ETH/USD price from the Chainlink oracle contract on Base Sepolia.
Pure read — no wallet or private key required.
"""

from web3 import Web3

# --- Config -----------------------------------------------------------

RPC_URL = "https://sepolia.base.org"

# Chainlink ETH/USD price feed on Base Sepolia
# https://docs.chain.link/data-feeds/price-feeds/addresses?network=base&page=1
CHAINLINK_ETH_USD = "0x4aDC67696bA383F43DD60A9e78F2C97Fbbfc7cb1"

# Minimal ABI — only the functions we need
AGGREGATOR_ABI = [
    {
        "inputs": [],
        "name": "latestRoundData",
        "outputs": [
            {"name": "roundId",         "type": "uint80"},
            {"name": "answer",          "type": "int256"},
            {"name": "startedAt",       "type": "uint256"},
            {"name": "updatedAt",       "type": "uint256"},
            {"name": "answeredInRound", "type": "uint80"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "description",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# --- Core -------------------------------------------------------------

def get_eth_usd_price() -> dict:
    """
    Fetch the latest ETH/USD price from Chainlink on Base Sepolia.

    Returns a dict:
        {
            "pair":        "ETH / USD",
            "price_usd":   float,
            "updated_at":  int   (unix timestamp),
            "round_id":    int,
        }
    """
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to RPC: {RPC_URL}")

    feed = w3.eth.contract(
        address=Web3.to_checksum_address(CHAINLINK_ETH_USD),
        abi=AGGREGATOR_ABI,
    )

    decimals        = feed.functions.decimals().call()
    description     = feed.functions.description().call()
    round_id, answer, _, updated_at, _ = feed.functions.latestRoundData().call()

    price_usd = answer / (10 ** decimals)

    return {
        "pair":       description,
        "price_usd":  price_usd,
        "updated_at": updated_at,
        "round_id":   round_id,
    }


# --- Entry point (standalone test) ------------------------------------

if __name__ == "__main__":
    import datetime

    data = get_eth_usd_price()
    ts   = datetime.datetime.utcfromtimestamp(data["updated_at"]).strftime("%Y-%m-%d %H:%M:%S UTC")

    print(f"Pair:       {data['pair']}")
    print(f"Price:      ${data['price_usd']:,.2f}")
    print(f"Updated:    {ts}")
    print(f"Round ID:   {data['round_id']}")
