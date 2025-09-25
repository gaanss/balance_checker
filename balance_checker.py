"""
Balance checker module.
Contains utilities for checking and formatting balances across networks.
"""

from typing import Dict, List, Optional
from decimal import Decimal, getcontext
import time
from etherscan_client import EtherscanClient
from config import SUPPORTED_NETWORKS, DEFAULT_NETWORKS, DEFAULT_ADDRESS
from wallet_reader import WalletReader

# Set precision for decimal calculations
getcontext().prec = 50


class BalanceChecker:
    """Main class for checking balances across multiple networks."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize balance checker.
        
        Args:
            api_key: Etherscan API key
        """
        self.client = EtherscanClient(api_key)
        self.wallet_reader = WalletReader()
    
    def wei_to_ether(self, wei_amount: str) -> Decimal:
        """
        Convert Wei to Ether.
        
        Args:
            wei_amount: Amount in Wei as string
            
        Returns:
            Amount in Ether as Decimal
        """
        wei = Decimal(wei_amount)
        ether = wei / Decimal(10**18)
        return ether
    
    def format_balance(self, wei_amount: str, decimals: int = 6) -> str:
        """
        Format balance for display.
        
        Args:
            wei_amount: Amount in Wei as string
            decimals: Number of decimal places to show
            
        Returns:
            Formatted balance string
        """
        if wei_amount is None:
            return "N/A"
        
        ether = self.wei_to_ether(wei_amount)
        
        if ether == 0:
            return "0.000000"
        
        # Format with specified decimal places
        formatted = f"{ether:.{decimals}f}"
        
        # Remove trailing zeros
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
        
        return formatted
    
    def check_balance(self, address: str, chain_id: int) -> Dict:
        """
        Check balance for a single address on a single chain.
        
        Args:
            address: Ethereum address to check
            chain_id: Chain ID of the network
            
        Returns:
            Dictionary with balance information
        """
        network_name = SUPPORTED_NETWORKS.get(chain_id, f"Unknown Network ({chain_id})")
        
        success, balance_wei, error = self.client.get_balance(address, chain_id)
        
        result = {
            'chain_id': chain_id,
            'network_name': network_name,
            'address': address,
            'success': success,
            'balance_wei': balance_wei,
            'balance_ether': self.format_balance(balance_wei) if success else None,
            'error': error
        }
        
        return result
    
    def check_balances(self, address: str, chain_ids: Optional[List[int]] = None) -> List[Dict]:
        """
        Check balance for an address across multiple chains.
        
        Args:
            address: Ethereum address to check
            chain_ids: List of chain IDs to check. If None, uses default networks.
            
        Returns:
            List of dictionaries with balance information for each chain
        """
        if chain_ids is None:
            chain_ids = DEFAULT_NETWORKS
        
        results = []
        
        for chain_id in chain_ids:
            result = self.check_balance(address, chain_id)
            results.append(result)
        
        return results
    
    def print_results(self, results: List[Dict], show_zero_balances: bool = True) -> None:
        """
        Print balance results in a formatted table.
        
        Args:
            results: List of balance results
            show_zero_balances: Whether to show chains with zero balance
        """
        print("\n" + "="*90)
        print("🔍 BALANCE CHECK RESULTS")
        print("="*90)
        
        # Filter results based on show_zero_balances
        filtered_results = results
        if not show_zero_balances:
            filtered_results = [
                r for r in results 
                if r['success'] and r['balance_ether'] and Decimal(r['balance_ether']) > 0
            ]
        
        if not filtered_results:
            print("❌ No balances found.")
            return
        
        # Group results by network name for better organization
        network_totals = {}
        successful_checks = 0
        
        # Print header
        print(f"{'🌐 Network':<35} {'💰 Balance (ETH)':<20} {'📊 Status':<15}")
        print("-" * 90)
        
        # Print results
        for result in filtered_results:
            network = result['network_name']
            
            if result['success']:
                balance = result['balance_ether']
                status = "✅ Success"
                successful_checks += 1
                
                # Add to network totals
                if network not in network_totals:
                    network_totals[network] = Decimal('0')
                if balance and Decimal(balance) > 0:
                    network_totals[network] += Decimal(balance)
            else:
                balance = "❌ Error"
                status = f"❌ {result['error']}"
            
            print(f"{network:<35} {balance:<20} {status:<15}")
        
        print("-" * 90)
        
        # Network totals
        if network_totals:
            print("\n📈 NETWORK TOTALS:")
            for network, total in sorted(network_totals.items()):
                print(f"  {network:<35} {total:.6f} ETH")
        
        # Overall summary
        total_balance = sum(network_totals.values())
        print(f"\n📊 SUMMARY:")
        print(f"  ✅ Successful checks: {successful_checks}/{len(results)}")
        print(f"  💰 Total balance: {total_balance:.6f} ETH")
        print("="*90)
    
    def check_multiple_wallets(self, addresses: List[str], chain_ids: Optional[List[int]] = None) -> Dict[str, List[Dict]]:
        """
        Check balances for multiple addresses across multiple chains.
        
        Args:
            addresses: List of Ethereum addresses to check
            chain_ids: List of chain IDs to check. If None, uses default networks.
            
        Returns:
            Dictionary with address as key and list of balance results as value
        """
        if chain_ids is None:
            chain_ids = DEFAULT_NETWORKS
        
        all_results = {}
        
        for address in addresses:
            print(f"Checking address: {address}")
            results = self.check_balances(address, chain_ids)
            all_results[address] = results
        
        return all_results
    
    def check_wallets_from_file(self, file_path: str, chain_ids: Optional[List[int]] = None) -> Dict[str, List[Dict]]:
        """
        Check balances for wallets read from a file.
        
        Args:
            file_path: Path to file containing wallet addresses
            chain_ids: List of chain IDs to check. If None, uses default networks.
            
        Returns:
            Dictionary with address as key and list of balance results as value
        """
        try:
            addresses = self.wallet_reader.read_wallets_from_file(file_path)
            print(f"Found {len(addresses)} valid wallet addresses in {file_path}")
            return self.check_multiple_wallets(addresses, chain_ids)
        except Exception as e:
            print(f"Error reading wallet file: {e}")
            return {}
    
    def print_multiple_wallet_results(self, all_results: Dict[str, List[Dict]], show_zero_balances: bool = True) -> None:
        """
        Print results for multiple wallets in a formatted way.
        
        Args:
            all_results: Dictionary with address as key and balance results as value
            show_zero_balances: Whether to show chains with zero balance
        """
        if not all_results:
            print("No results to display.")
            return
        
        print("\n" + "="*110)
        print("👥 MULTIPLE WALLET BALANCE CHECK RESULTS")
        print("="*110)
        
        total_wallets = len(all_results)
        total_balance_all_wallets = Decimal('0')
        wallets_with_balance = 0
        all_network_totals = {}
        
        for i, (address, results) in enumerate(all_results.items(), 1):
            print(f"\n[{i}/{total_wallets}] 💼 Wallet: {address}")
            print("-" * 90)
            
            # Filter results based on show_zero_balances
            filtered_results = results
            if not show_zero_balances:
                filtered_results = [
                    r for r in results 
                    if r['success'] and r['balance_ether'] and Decimal(r['balance_ether']) > 0
                ]
            
            if not filtered_results:
                print("❌ No balances found for this wallet.")
                continue
            
            # Print header for this wallet
            print(f"{'🌐 Network':<35} {'💰 Balance (ETH)':<20} {'📊 Status':<15}")
            print("-" * 90)
            
            wallet_total_balance = Decimal('0')
            wallet_network_totals = {}
            
            # Print results for this wallet
            for result in filtered_results:
                network = result['network_name']
                
                if result['success']:
                    balance = result['balance_ether']
                    status = "✅ Success"
                    if balance and Decimal(balance) > 0:
                        wallet_total_balance += Decimal(balance)
                        
                        # Add to wallet network totals
                        if network not in wallet_network_totals:
                            wallet_network_totals[network] = Decimal('0')
                        wallet_network_totals[network] += Decimal(balance)
                        
                        # Add to global network totals
                        if network not in all_network_totals:
                            all_network_totals[network] = Decimal('0')
                        all_network_totals[network] += Decimal(balance)
                else:
                    balance = "❌ Error"
                    status = f"❌ {result['error']}"
                
                print(f"{network:<35} {balance:<20} {status:<15}")
            
            # Wallet network totals
            if wallet_network_totals:
                print(f"\n📈 Wallet Network Totals:")
                for network, total in sorted(wallet_network_totals.items()):
                    print(f"  {network:<35} {total:.6f} ETH")
            
            # Summary for this wallet
            successful_checks = [r for r in results if r['success']]
            print(f"\n📊 Wallet Summary:")
            print(f"  💰 Wallet total: {wallet_total_balance:.6f} ETH")
            print(f"  ✅ Successful checks: {len(successful_checks)}/{len(results)}")
            
            if wallet_total_balance > 0:
                wallets_with_balance += 1
                total_balance_all_wallets += wallet_total_balance
        
        # Overall summary
        print("\n" + "="*110)
        print("🏆 OVERALL SUMMARY")
        print("="*110)
        
        # Global network totals
        if all_network_totals:
            print("\n📈 GLOBAL NETWORK TOTALS:")
            for network, total in sorted(all_network_totals.items()):
                print(f"  {network:<35} {total:.6f} ETH")
        
        print(f"\n📊 FINAL STATISTICS:")
        print(f"  👥 Total wallets checked: {total_wallets}")
        print(f"  💰 Wallets with balance: {wallets_with_balance}")
        print(f"  🏦 Total balance across all wallets: {total_balance_all_wallets:.6f} ETH")
        print("="*110)
    
    def export_to_html(self, all_results: Dict[str, List[Dict]], filename: str = "balance_report.html") -> None:
        """
        Export balance results to HTML format.
        
        Args:
            all_results: Dictionary with address as key and balance results as value
            filename: Output HTML filename
        """
        if not all_results:
            print("No results to export.")
            return
        
        # Collect all unique networks
        all_networks = set()
        for results in all_results.values():
            for result in results:
                if result['success']:
                    all_networks.add(result['network_name'])
        
        all_networks = sorted(list(all_networks))
        
        # Generate HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Balance Check Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .summary {{
            background-color: #e8f4fd;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        tr:hover {{
            background-color: #e6f3ff;
        }}
        .wallet-address {{
            font-family: monospace;
            font-size: 0.9em;
            max-width: 200px;
            word-break: break-all;
        }}
        .balance {{
            text-align: right;
            font-weight: bold;
        }}
        .zero-balance {{
            color: #999;
        }}
        .total-row {{
            background-color: #4CAF50 !important;
            color: white;
            font-weight: bold;
        }}
        .network-totals {{
            margin-top: 30px;
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Balance Check Report</h1>
        
        <div class="summary">
            <h3>📊 Summary</h3>
            <p><strong>Total wallets checked:</strong> {len(all_results)}</p>
            <p><strong>Networks checked:</strong> {', '.join(all_networks)}</p>
            <p><strong>Generated:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>💼 Wallet Address</th>
"""
        
        # Add network columns
        for network in all_networks:
            html_content += f'                    <th>🌐 {network}</th>\n'
        
        html_content += """                    <th>💰 Total</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Calculate totals
        network_totals = {network: Decimal('0') for network in all_networks}
        grand_total = Decimal('0')
        
        # Add wallet rows
        for address, results in all_results.items():
            html_content += f'                <tr>\n'
            html_content += f'                    <td class="wallet-address">{address}</td>\n'
            
            wallet_total = Decimal('0')
            wallet_balances = {}
            
            # Get balances for this wallet
            for result in results:
                if result['success'] and result['balance_ether']:
                    network = result['network_name']
                    balance = Decimal(result['balance_ether'])
                    wallet_balances[network] = balance
                    if balance > 0:
                        wallet_total += balance
            
            # Add balance for each network
            for network in all_networks:
                if network in wallet_balances:
                    balance = wallet_balances[network]
                    if balance > 0:
                        html_content += f'                    <td class="balance">{balance:.6f}</td>\n'
                        network_totals[network] += balance
                    else:
                        html_content += f'                    <td class="balance zero-balance">0.000000</td>\n'
                else:
                    html_content += f'                    <td class="balance zero-balance">-</td>\n'
            
            # Add wallet total
            html_content += f'                    <td class="balance">{wallet_total:.6f}</td>\n'
            grand_total += wallet_total
            
            html_content += f'                </tr>\n'
        
        # Add totals row
        html_content += """                <tr class="total-row">
                    <td><strong>📈 TOTALS</strong></td>
"""
        
        for network in all_networks:
            html_content += f'                    <td><strong>{network_totals[network]:.6f}</strong></td>\n'
        
        html_content += f'                    <td><strong>{grand_total:.6f}</strong></td>\n'
        html_content += '                </tr>\n'
        
        html_content += """            </tbody>
        </table>
        
        <div class="network-totals">
            <h3>📈 Network Totals</h3>
            <ul>
"""
        
        for network in all_networks:
            html_content += f'                <li><strong>{network}:</strong> {network_totals[network]:.6f} ETH</li>\n'
        
        html_content += f"""            </ul>
            <p><strong>Grand Total:</strong> {grand_total:.6f} ETH</p>
        </div>
    </div>
</body>
</html>"""
        
        # Write HTML file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\n📄 HTML report exported to: {filename}")
        except Exception as e:
            print(f"❌ Error exporting HTML report: {e}")
