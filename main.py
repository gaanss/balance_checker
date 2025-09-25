#!/usr/bin/env python3
"""
Main script for checking balances across multiple blockchain networks.
Usage: python main.py [address] [--networks chain_id1,chain_id2,...] [--api-key YOUR_API_KEY]
"""

import argparse
import sys
import os
from typing import List, Optional

from balance_checker import BalanceChecker
from config import SUPPORTED_NETWORKS, DEFAULT_NETWORKS, get_api_key
from wallet_reader import WalletReader


def parse_chain_ids(networks_str: str) -> List[int]:
    """
    Parse comma-separated chain IDs from string.
    
    Args:
        networks_str: Comma-separated chain IDs
        
    Returns:
        List of chain IDs
    """
    try:
        chain_ids = [int(chain_id.strip()) for chain_id in networks_str.split(',')]
        
        # Validate chain IDs
        invalid_chains = [cid for cid in chain_ids if cid not in SUPPORTED_NETWORKS]
        if invalid_chains:
            print(f"Warning: Unsupported chain IDs: {invalid_chains}")
            print("Available chain IDs:")
            for cid, name in sorted(SUPPORTED_NETWORKS.items()):
                print(f"  {cid}: {name}")
        
        return chain_ids
    except ValueError as e:
        print(f"Error parsing chain IDs: {e}")
        sys.exit(1)


def main():
    """Main function to run the balance checker."""
    parser = argparse.ArgumentParser(
        description="Check Ethereum address balance across multiple blockchain networks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check wallets from wallets.txt file (default behavior)
  python main.py
  
  # Check specific address
  python main.py 0x1234...5678
  
  # Check wallets from custom file
  python main.py --wallet-file my_wallets.txt
  
  # Check specific networks
  python main.py --networks 1,137,42161
  
  # Create sample wallet file
  python main.py --create-sample-wallet-file
  
  # List all supported networks
  python main.py --list-networks
  
  # Use custom API key
  python main.py --api-key YOUR_API_KEY
  
  # Export results to HTML
  python main.py --export-html report.html
        """
    )
    
    parser.add_argument(
        'address',
        nargs='?',
        default=None,
        help='Ethereum address to check (if not provided, will check wallets from file)'
    )
    
    parser.add_argument(
        '--networks',
        type=str,
        help=f'Comma-separated chain IDs to check (default: {",".join(map(str, DEFAULT_NETWORKS))})'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='Etherscan API key (can also be set via ETHERSCAN_API_KEY environment variable)'
    )
    
    parser.add_argument(
        '--show-zero',
        action='store_true',
        help='Show networks with zero balance'
    )
    
    parser.add_argument(
        '--list-networks',
        action='store_true',
        help='List all supported networks and exit'
    )
    
    parser.add_argument(
        '--wallet-file',
        type=str,
        default='wallets.txt',
        help='Path to file containing wallet addresses (default: wallets.txt)'
    )
    
    parser.add_argument(
        '--create-sample-wallet-file',
        action='store_true',
        help='Create a sample wallet file and exit'
    )
    
    parser.add_argument(
        '--export-html',
        type=str,
        help='Export results to HTML file (specify filename)'
    )
    
    args = parser.parse_args()
    
    # List networks if requested
    if args.list_networks:
        print("Supported Networks:")
        print("=" * 50)
        for chain_id, name in sorted(SUPPORTED_NETWORKS.items()):
            print(f"{chain_id:>8}: {name}")
        return
    
    # Create sample wallet file if requested
    if args.create_sample_wallet_file:
        wallet_reader = WalletReader()
        wallet_reader.create_sample_wallet_file(args.wallet_file)
        return
    
    # Parse chain IDs
    if args.networks:
        chain_ids = parse_chain_ids(args.networks)
    else:
        chain_ids = DEFAULT_NETWORKS
    
    try:
        # Get API key from settings.yaml or command line
        api_key = args.api_key or get_api_key()
        
        # Initialize balance checker
        checker = BalanceChecker(api_key=api_key)
        
        # Determine if checking single address or multiple wallets from file
        if args.address:
            # Single address mode
            if not args.address.startswith('0x') or len(args.address) != 42:
                print("Error: Invalid Ethereum address format")
                sys.exit(1)
            
            print(f"Checking balance for address: {args.address}")
            print(f"Networks to check: {len(chain_ids)}")
            print("Starting balance check...")
            
            # Check balances
            results = checker.check_balances(args.address, chain_ids)
            
            # Print results
            checker.print_results(results, show_zero_balances=args.show_zero)
        
        else:
            # Multiple wallets from file mode
            print(f"Checking wallets from file: {args.wallet_file}")
            print(f"Networks to check: {len(chain_ids)}")
            print("Starting balance check...")
            
            # Check wallets from file
            all_results = checker.check_wallets_from_file(args.wallet_file, chain_ids)
            
            # Print results
            checker.print_multiple_wallet_results(all_results, show_zero_balances=args.show_zero)
            
            # Export to HTML if requested
            if args.export_html:
                checker.export_to_html(all_results, args.export_html)
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nTo get an API key:")
        print("1. Visit https://etherscan.io/apis")
        print("2. Create an account and generate an API key")
        print("3. Set the ETHERSCAN_API_KEY environment variable or use --api-key")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
