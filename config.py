"""
Configuration module for balance checker.
Contains network configurations and API settings.
"""

import os
import yaml
from typing import Optional

# Supported networks with their chain IDs
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

# Default networks to check (from user's request)
DEFAULT_NETWORKS = [42161, 43114, 56, 10, 137, 204]

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
