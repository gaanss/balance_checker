"""
Etherscan API client module.
Handles communication with Etherscan API for balance checking.
"""

import os
import requests
import time
from typing import Dict, Optional, Tuple
from config import ETHERSCAN_API_BASE_URL, API_KEY_ENV_VAR


class EtherscanClient:
    """Client for interacting with Etherscan API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Etherscan client.
        
        Args:
            api_key: Etherscan API key. If not provided, will try to get from environment.
        """
        self.api_key = api_key or os.getenv(API_KEY_ENV_VAR)
        if not self.api_key:
            raise ValueError(f"API key not provided. Set {API_KEY_ENV_VAR} environment variable or pass api_key parameter.")
        
        self.base_url = ETHERSCAN_API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BalanceChecker/1.0'
        })
        
        # Rate limiting: 3 requests per second
        self.rate_limit_delay = 1.0 / 3.0  # 0.333 seconds between requests
        self.last_request_time = 0
    
    def _enforce_rate_limit(self):
        """Enforce rate limiting by waiting if necessary."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def get_balance(self, address: str, chain_id: int) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Get balance for an address on a specific chain.
        
        Args:
            address: Ethereum address to check
            chain_id: Chain ID of the network
            
        Returns:
            Tuple of (success, balance_wei, error_message)
        """
        # Enforce rate limiting
        self._enforce_rate_limit()
        
        params = {
            'chainid': chain_id,
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest',
            'apikey': self.api_key
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == '1':
                balance_wei = data.get('result', '0')
                return True, balance_wei, None
            else:
                error_msg = data.get('message', 'Unknown error')
                return False, None, error_msg
                
        except requests.exceptions.RequestException as e:
            return False, None, f"Network error: {str(e)}"
        except Exception as e:
            return False, None, f"Unexpected error: {str(e)}"
    
    def get_multiple_balances(self, address: str, chain_ids: list, delay: float = None) -> Dict[int, Dict]:
        """
        Get balances for an address across multiple chains.
        
        Args:
            address: Ethereum address to check
            chain_ids: List of chain IDs to check
            delay: Additional delay between requests in seconds (rate limiting is automatic)
            
        Returns:
            Dictionary with chain_id as key and balance info as value
        """
        results = {}
        
        for chain_id in chain_ids:
            success, balance, error = self.get_balance(address, chain_id)
            
            results[chain_id] = {
                'success': success,
                'balance_wei': balance,
                'error': error
            }
            
            # Add additional delay if specified (rate limiting is already enforced in get_balance)
            if delay and delay > 0:
                time.sleep(delay)
        
        return results
