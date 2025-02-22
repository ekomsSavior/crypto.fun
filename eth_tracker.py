import requests
import time

# 🔥 Replace this with your Etherscan API Key
API_KEY = "your_etherscan_api_key"

# 🔥 Replace this with the wallet you want to track
WALLET_ADDRESS = "eth_wallet_address"

# 🔥 Minimum ETH value to filter transactions (Change this for different searches)
MIN_ETH = 10  

# Etherscan API URL
url = f"https://api.etherscan.io/api?module=account&action=txlist&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"

# Convert Wei to Ether
def wei_to_ether(wei):
    return int(wei) / 10**18

# Fetch transactions
response = requests.get(url)
data = response.json()

if data["status"] == "1":
    with open("eth_transactions_filtered.txt", "w") as f:
        print(f"🔍 Tracking Transactions for: {WALLET_ADDRESS}\n")
        f.write(f"🔍 Tracking Transactions for: {WALLET_ADDRESS}\n\n")

        for tx in data["result"]:  # No limit, pulls all transactions
            eth_value = wei_to_ether(tx['value'])
            
            # Filter: Only show transactions over MIN_ETH
            if eth_value >= MIN_ETH:
                output = (
                    f"📅 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(tx['timeStamp'])))}\n"
                    f"🔹 From: {tx['from']}\n"
                    f"🔹 To: {tx['to']}\n"
                    f"💰 Value: {eth_value} ETH\n"
                    f"🔗 Transaction Hash: {tx['hash']}\n"
                    f"🔢 Block Number: {tx['blockNumber']}\n"
                    f"{'-' * 50}\n"
                )
                print(output)  # Print to terminal
                f.write(output)  # Save to file

    print(f"\n✅ Transactions saved in 'eth_transactions_filtered.txt'!")

else:
    print("❌ Error:", data["message"])
