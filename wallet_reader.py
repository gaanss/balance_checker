"""
Wallet reader module.
Handles reading wallet addresses from files.
"""

import os
from typing import List, Set
import re


class WalletReader:
    """Class for reading wallet addresses from files."""
    
    def __init__(self):
        """Initialize wallet reader."""
        # Ethereum address regex pattern
        self.address_pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
    
    def is_valid_address(self, address: str) -> bool:
        """
        Check if address is a valid Ethereum address.
        
        Args:
            address: Address string to validate
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.address_pattern.match(address.strip()))
    
    def read_wallets_from_file(self, file_path: str) -> List[str]:
        """
        Read wallet addresses from a text file.
        
        Args:
            file_path: Path to the file containing wallet addresses
            
        Returns:
            List of valid wallet addresses
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If no valid addresses found
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Wallet file not found: {file_path}")
        
        addresses = []
        invalid_lines = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Check if line contains a valid address
                    if self.is_valid_address(line):
                        addresses.append(line)
                    else:
                        invalid_lines.append(f"Line {line_num}: {line}")
        
        except Exception as e:
            raise ValueError(f"Error reading wallet file: {e}")
        
        if not addresses:
            raise ValueError("No valid wallet addresses found in file")
        
        # Remove duplicates while preserving order
        unique_addresses = list(dict.fromkeys(addresses))
        
        if invalid_lines:
            print(f"Warning: Found {len(invalid_lines)} invalid lines in {file_path}:")
            for invalid_line in invalid_lines[:10]:  # Show first 10 invalid lines
                print(f"  {invalid_line}")
            if len(invalid_lines) > 10:
                print(f"  ... and {len(invalid_lines) - 10} more")
        
        return unique_addresses
    
    def create_sample_wallet_file(self, file_path: str = "wallets.txt") -> None:
        """
        Create a sample wallet file with example addresses.
        
        Args:
            file_path: Path where to create the sample file
        """
        sample_addresses = [
            "# Sample wallet addresses file",
            "# Add one address per line",
            "# Lines starting with # are comments and will be ignored",
            "",
            "0xb5d85cbf7cb3ee0d56b3bb207d5fc4b82f43f511",
            "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
            "0x8ba1f109551bD432803012645Hac136c",
            "",
            "# You can add more addresses here"
        ]
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(sample_addresses))
            print(f"Sample wallet file created: {file_path}")
        except Exception as e:
            print(f"Error creating sample file: {e}")
    
    def get_wallet_count(self, file_path: str) -> int:
        """
        Get the number of valid wallet addresses in a file.
        
        Args:
            file_path: Path to the wallet file
            
        Returns:
            Number of valid addresses
        """
        try:
            addresses = self.read_wallets_from_file(file_path)
            return len(addresses)
        except Exception:
            return 0
