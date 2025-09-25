# 🔍 Balance Checker

A powerful Python tool for checking Ethereum wallet balances across multiple blockchain networks using the Etherscan API.

## ✨ Features

- 🌐 **Multi-Network Support**: Check balances across 70+ blockchain networks
- 📁 **Batch Processing**: Check multiple wallets from a text file
- 🎨 **Beautiful Output**: Formatted console output with emojis and clear tables
- 📊 **HTML Reports**: Export results to beautiful HTML reports
- ⚡ **Rate Limiting**: Built-in 3 requests/second rate limiting
- 🔧 **Easy Configuration**: Simple YAML configuration file
- 🛡️ **Error Handling**: Comprehensive error handling and validation

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd balance_checker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `settings.yaml` file with your Etherscan API key:

```yaml
# Balance Checker Settings
etherscan:
  api_key: "YOUR_ETHERSCAN_API_KEY"
```

Get your API key from [Etherscan APIs](https://etherscan.io/apis).

### 3. Add Wallets

Create a `wallets.txt` file with wallet addresses (one per line):

```
# My wallet addresses
0xb5d85cbf7cb3ee0d56b3bb207d5fc4b82f43f511
0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
0x8ba1f109551bD432803012645Hac136c
```

### 4. Run

```bash
# Check all wallets from wallets.txt
python main.py

# Check specific networks
python main.py --networks 1,137,42161

# Export to HTML report
python main.py --export-html report.html
```

## 📖 Usage Examples

### Basic Usage

```bash
# Check wallets from default file (wallets.txt)
python main.py

# Check specific address
python main.py 0x1234567890123456789012345678901234567890

# Check specific networks
python main.py --networks 1,137,42161,8453
```

### Advanced Usage

```bash
# Use custom wallet file
python main.py --wallet-file my_wallets.txt

# Show only non-zero balances
python main.py --show-zero

# Export results to HTML
python main.py --export-html balance_report.html

# Create sample wallet file
python main.py --create-sample-wallet-file

# List all supported networks
python main.py --list-networks
```

## 🌐 Supported Networks

The tool supports all networks available in the Etherscan API, including:

| Network | Chain ID | Network | Chain ID |
|---------|----------|---------|----------|
| Ethereum Mainnet | 1 | Polygon Mainnet | 137 |
| Arbitrum One | 42161 | Base Mainnet | 8453 |
| OP Mainnet | 10 | Scroll Mainnet | 534352 |
| Blast Mainnet | 81457 | Avalanche C-Chain | 43114 |
| BNB Smart Chain | 56 | zkSync Mainnet | 324 |

And many more! Use `python main.py --list-networks` to see the complete list.

## 📊 Output Examples

### Console Output

```
==========================================================================================
🔍 BALANCE CHECK RESULTS
==========================================================================================
🌐 Network                           💰 Balance (ETH)      📊 Status
------------------------------------------------------------------------------------------
Arbitrum One Mainnet                0.031222             ✅ Success
Base Mainnet                        1.322353             ✅ Success
OP Mainnet                          0.032416             ✅ Success
Scroll Mainnet                      0.000000             ✅ Success
Blast Mainnet                       0.000000             ✅ Success
------------------------------------------------------------------------------------------

📈 NETWORK TOTALS:
  Arbitrum One Mainnet                0.031222 ETH
  Base Mainnet                        1.322353 ETH
  OP Mainnet                          0.032416 ETH

📊 SUMMARY:
  ✅ Successful checks: 5/5
  💰 Total balance: 1.385991 ETH
==========================================================================================
```

### HTML Report

The HTML export creates a beautiful, responsive table with:
- 📋 Wallet addresses in rows
- 🌐 Network balances in columns
- 📊 Network totals and grand total
- 🎨 Professional styling with hover effects

## ⚙️ Configuration

### settings.yaml

```yaml
# Balance Checker Settings
etherscan:
  api_key: "YOUR_ETHERSCAN_API_KEY"
```

### wallets.txt Format

```
# Comments start with #
0xb5d85cbf7cb3ee0d56b3bb207d5fc4b82f43f511
0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6

# Empty lines are ignored
0x8ba1f109551bD432803012645Hac136c
```

## 🏗️ Project Structure

```
balance_checker/
├── main.py                 # Main script
├── balance_checker.py      # Core balance checking logic
├── etherscan_client.py     # Etherscan API client
├── wallet_reader.py        # Wallet file reader
├── config.py              # Configuration management
├── settings.yaml          # API key configuration
├── wallets.txt            # Wallet addresses file
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 API Rate Limiting

The tool automatically enforces a 3 requests/second rate limit to comply with Etherscan API limits. This ensures reliable operation without hitting rate limits.

## 🛠️ Development

### Running Tests

```bash
# Test API responses
python test_api_response.py

# Test HTML export
python test_html_export.py
```

### Adding New Networks

Networks are defined in `config.py`. To add support for new networks, add them to the `SUPPORTED_NETWORKS` dictionary.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. Always verify balances through official blockchain explorers for critical operations.

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ for the crypto community
