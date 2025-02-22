import requests
import time
import csv
from datetime import datetime, timezone

# 🔥 Replace with your Etherscan API Key
API_KEY = "your_etherscan_api_key"

# 🔥 Replace with the wallet address you want to track
WALLET_ADDRESS = "0x1Db92e2EeBC8E0c075a02BeA49a2935BcD2dFCF4"

# 🔥 Minimum ETH value to filter transactions
MIN_ETH = 10  

# 🔥 Date filter: Only show transactions from this date (format: YYYY-MM-DD)
FILTER_DATE = "2025-02-21"  # CHANGE THIS TO YOUR DESIRED DATE

# Etherscan API URL
url = f"https://api.etherscan.io/api?module=account&action=txlist&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"

# Convert Wei to Ether
def wei_to_ether(wei):
    return int(wei) / 10**18

# Fetch transactions
response = requests.get(url)
data = response.json()

if data["status"] == "1":
    with open("eth_transactions_filtered.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Timestamp", "From", "To", "Value (ETH)", "Transaction Hash", "Block Number"])  # CSV Headers

        print(f"🔍 Tracking Transactions for: {WALLET_ADDRESS}\n")

        for tx in data["result"]:
            eth_value = wei_to_ether(tx['value'])
            
            # ✅ Fixed timestamp conversion (No more warning!)
            tx_time = datetime.fromtimestamp(int(tx['timeStamp']), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

            # Filter: Only transactions over MIN_ETH & matching FILTER_DATE
            if eth_value >= MIN_ETH and tx_time.startswith(FILTER_DATE):
                output = (
                    f"📅 Timestamp: {tx_time}\n"
                    f"🔹 From: {tx['from']}\n"
                    f"🔹 To: {tx['to']}\n"
                    f"💰 Value: {eth_value} ETH\n"
                    f"🔗 Transaction Hash: {tx['hash']}\n"
                    f"🔢 Block Number: {tx['blockNumber']}\n"
                    f"{'-' * 50}\n"
                )
                print(output)  # Print to terminal
                
                # Write to CSV
                csvwriter.writerow([tx_time, tx['from'], tx['to'], eth_value, tx['hash'], tx['blockNumber']])

    print(f"\n✅ Transactions saved in 'eth_transactions_filtered.csv'!")

else:
    print("❌ Error:", data["message"])
