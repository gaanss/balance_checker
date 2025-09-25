"""
Configuration module for balance checker.
Contains network configurations and API settings.
"""

import os
import yaml
from typing import Optional

# Supported networks with their chain IDs and native currencies
SUPPORTED_NETWORKS = {
    1: "Ethereum Mainnet",
    11155111: "Sepolia Testnet",
    17000: "Holesky Testnet",
    560048: "Hoodi Testnet",
    2741: "Abstract Mainnet",
    11124: "Abstract Sepolia Testnet",
    33111: "ApeChain Curtis Testnet",
    33139: "ApeChain Mainnet",
    42170: "Arbitrum Nova Mainnet",
    42161: "Arbitrum One Mainnet",
    421614: "Arbitrum Sepolia Testnet",
    43114: "Avalanche C-Chain",
    43113: "Avalanche Fuji Testnet",
    8453: "Base Mainnet",
    84532: "Base Sepolia Testnet",
    80094: "Berachain Mainnet",
    80069: "Berachain Bepolia Testnet",
    199: "BitTorrent Chain Mainnet",
    1029: "BitTorrent Chain Testnet",
    81457: "Blast Mainnet",
    168587773: "Blast Sepolia Testnet",
    56: "BNB Smart Chain Mainnet",
    97: "BNB Smart Chain Testnet",
    44787: "Celo Alfajores Testnet",
    42220: "Celo Mainnet",
    25: "Cronos Mainnet",
    252: "Fraxtal Mainnet",
    2522: "Fraxtal Testnet",
    100: "Gnosis",
    999: "HyperEVM Mainnet",
    59144: "Linea Mainnet",
    59141: "Linea Sepolia Testnet",
    5000: "Mantle Mainnet",
    5003: "Mantle Sepolia Testnet",
    43521: "Memecore Testnet",
    1287: "Moonbase Alpha Testnet",
    10143: "Monad Testnet",
    1284: "Moonbeam Mainnet",
    1285: "Moonriver Mainnet",
    10: "OP Mainnet",
    11155420: "OP Sepolia Testnet",
    137: "Polygon Mainnet",
    80002: "Polygon Amoy Testnet",
    747474: "Katana Mainnet",
    737373: "Katana Bokuto Testnet",
    1329: "Sei Mainnet",
    1328: "Sei Testnet",
    534352: "Scroll Mainnet",
    534351: "Scroll Sepolia Testnet",
    14601: "Sonic Testnet",
    146: "Sonic Mainnet",
    50104: "Sophon Mainnet",
    531050104: "Sophon Sepolia Testnet",
    1923: "Swellchain Mainnet",
    1924: "Swellchain Testnet",
    167000: "Taiko Mainnet",
    167012: "Taiko Hoodi Testnet",
    130: "Unichain Mainnet",
    1301: "Unichain Sepolia Testnet",
    480: "World Mainnet",
    4801: "World Sepolia Testnet",
    51: "XDC Apothem Testnet",
    50: "XDC Mainnet",
    324: "zkSync Mainnet",
    300: "zkSync Sepolia Testnet",
    204: "opBNB Mainnet",
    5611: "opBNB Testnet"
}

# Native currencies for each network
NATIVE_CURRENCIES = {
    1: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    11155111: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    17000: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    560048: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    2741: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    11124: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    33111: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    33139: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    42170: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    42161: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    421614: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    43114: {"symbol": "AVAX", "name": "Avalanche", "decimals": 18},
    43113: {"symbol": "AVAX", "name": "Avalanche", "decimals": 18},
    8453: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    84532: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    80094: {"symbol": "BERA", "name": "Berachain", "decimals": 18},
    80069: {"symbol": "BERA", "name": "Berachain", "decimals": 18},
    199: {"symbol": "BTT", "name": "BitTorrent", "decimals": 18},
    1029: {"symbol": "BTT", "name": "BitTorrent", "decimals": 18},
    81457: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    168587773: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    56: {"symbol": "BNB", "name": "BNB", "decimals": 18},
    97: {"symbol": "BNB", "name": "BNB", "decimals": 18},
    44787: {"symbol": "CELO", "name": "Celo", "decimals": 18},
    42220: {"symbol": "CELO", "name": "Celo", "decimals": 18},
    25: {"symbol": "CRO", "name": "Cronos", "decimals": 18},
    252: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    2522: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    100: {"symbol": "XDAI", "name": "Gnosis", "decimals": 18},
    999: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    59144: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    59141: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    5000: {"symbol": "MNT", "name": "Mantle", "decimals": 18},
    5003: {"symbol": "MNT", "name": "Mantle", "decimals": 18},
    43521: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    1287: {"symbol": "MOVR", "name": "Moonriver", "decimals": 18},
    10143: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    1284: {"symbol": "GLMR", "name": "Moonbeam", "decimals": 18},
    1285: {"symbol": "MOVR", "name": "Moonriver", "decimals": 18},
    10: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    11155420: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    137: {"symbol": "MATIC", "name": "Polygon", "decimals": 18},
    80002: {"symbol": "MATIC", "name": "Polygon", "decimals": 18},
    747474: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    737373: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    1329: {"symbol": "SEI", "name": "Sei", "decimals": 18},
    1328: {"symbol": "SEI", "name": "Sei", "decimals": 18},
    534352: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    534351: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    14601: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    146: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    50104: {"symbol": "SOPH", "name": "Sophon", "decimals": 18},
    531050104: {"symbol": "SOPH", "name": "Sophon", "decimals": 18},
    1923: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    1924: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    167000: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    167012: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    130: {"symbol": "UNI", "name": "Unichain", "decimals": 18},
    1301: {"symbol": "UNI", "name": "Unichain", "decimals": 18},
    480: {"symbol": "WLD", "name": "World", "decimals": 18},
    4801: {"symbol": "WLD", "name": "World", "decimals": 18},
    51: {"symbol": "XDC", "name": "XDC", "decimals": 18},
    50: {"symbol": "XDC", "name": "XDC", "decimals": 18},
    324: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    300: {"symbol": "ETH", "name": "Ethereum", "decimals": 18},
    204: {"symbol": "BNB", "name": "BNB", "decimals": 18},
    5611: {"symbol": "BNB", "name": "BNB", "decimals": 18}
}

# Default networks to check (from user's request)
DEFAULT_NETWORKS = [8453, 56, 5611]

# Etherscan API configuration
ETHERSCAN_API_BASE_URL = "https://api.etherscan.io/v2/api"

# Default address to check (from user's request)
DEFAULT_ADDRESS = "0xb5d85cbf7cb3ee0d56b3bb207d5fc4b82f43f511"

# API key placeholder - should be set via environment variable
API_KEY_ENV_VAR = "ETHERSCAN_API_KEY"


def load_api_key() -> Optional[str]:
    """
    Load API key from settings.yaml file.
    
    Returns:
        API key string or None if not found
    """
    try:
        with open('settings.yaml', 'r', encoding='utf-8') as file:
            settings = yaml.safe_load(file)
            return settings.get('etherscan', {}).get('api_key')
    except (FileNotFoundError, yaml.YAMLError, KeyError):
        return None


def get_api_key() -> Optional[str]:
    """
    Get API key from settings.yaml or environment variable.
    
    Returns:
        API key string or None if not found
    """
    # First try to load from settings.yaml
    api_key = load_api_key()
    if api_key:
        return api_key
    
    # Fallback to environment variable
    return os.getenv(API_KEY_ENV_VAR)
