import requests
import time

# 🔥 Replace this with your Etherscan API Key
API_KEY = "your_etherscan_api_key"

# 🔥 Replace this with the wallet you want to track
WALLET_ADDRESS = "0x1Db92e2EeBC8E0c075a02BeA49a2935BcD2dFCF4"

# Etherscan API URL
url = f"https://api.etherscan.io/api?module=account&action=txlist&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"

# Convert Wei to Ether
def wei_to_ether(wei):
    return int(wei) / 10**18

# Fetch transactions
response = requests.get(url)
data = response.json()

if data["status"] == "1":
    with open("eth_transactions.txt", "w") as f:
        print(f"Tracking Transactions for: {WALLET_ADDRESS}\n")
        f.write(f"Tracking Transactions for: {WALLET_ADDRESS}\n\n")
        for tx in data["result"][:10]:  # Shows only the last 10 transactions
            output = (
                f"From: {tx['from']}\n"
                f"To: {tx['to']}\n"
                f"Value: {wei_to_ether(tx['value'])} ETH\n"
                f"Transaction Hash: {tx['hash']}\n"
                f"Block Number: {tx['blockNumber']}\n"
                f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(tx['timeStamp'])))}\n"
                f"{'-' * 40}\n"
            )
            print(output)  # Print to terminal
            f.write(output)  # Save to file
else:
    print("Error:", data["message"])
