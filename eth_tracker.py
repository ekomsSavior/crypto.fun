import requests
import time
import csv
from datetime import datetime, timezone

# 🔥 Replace with your API key
API_KEY = "your_etherscan_api_key"

# 🔥 Wallet address to track
WALLET_ADDRESS = "eth_wallet_address"

# 🔥 Minimum ETH to filter transactions
MIN_ETH = 10  

# 🔥 Date filter (YYYY-MM-DD)
FILTER_DATE = "2025-02-21"  # CHANGE THIS IF NEEDED

# Etherscan API URL
url = f"https://api.etherscan.io/api?module=account&action=txlist&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"

# Convert Wei to Ether
def wei_to_ether(wei):
    return int(wei) / 10**18

# Fetch transactions
response = requests.get(url)
data = response.json()

# 🔴 STEP 1: Print the raw response to see if it's working
print("\n🔍 API RAW RESPONSE:\n", data, "\n")

if data["status"] == "1":
    with open("eth_transactions_filtered.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Timestamp", "From", "To", "Value (ETH)", "Transaction Hash", "Block Number"])  # CSV Headers

        print(f"🔍 Tracking Transactions for: {WALLET_ADDRESS}\n")

        found_transactions = False  # Track if we found any matching transactions

        for tx in data["result"]:
            eth_value = wei_to_ether(tx['value'])
            
            # ✅ Fixed timestamp conversion
            tx_time = datetime.fromtimestamp(int(tx['timeStamp']), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

            # Filter transactions
            if eth_value >= MIN_ETH and tx_time.startswith(FILTER_DATE):
                found_transactions = True
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

        if not found_transactions:
            print("⚠️ No transactions met the filter criteria.")

    print(f"\n✅ Transactions saved in 'eth_transactions_filtered.csv'!")

else:
    print("❌ API Error:", data["message"])
