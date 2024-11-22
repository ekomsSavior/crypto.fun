import requests
import time
import tkinter as tk

# Function to fetch Bitcoin price
def get_bitcoin_price():
    try:
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=5)
        data = response.json()
        return f"BTC: ${data['bpi']['USD']['rate']}"
    except Exception as e:
        return f"Error: {e}"

# Function to update the price in the window
def update_price():
    try:
        price = get_bitcoin_price()
        print(f"Fetched price: {price}")  # Debugging output
        label.config(text=price)
    except Exception as e:
        print(f"Error updating price: {e}")
    finally:
        root.after(60000, update_price)  # Update every 60 seconds

# Create the GUI window
root = tk.Tk()
root.title("Bitcoin Price")
root.geometry("300x100")

label = tk.Label(root, text="Fetching price...", font=("Helvetica", 16))
label.pack(pady=20)

# Start updating the price
update_price()

# Run the app
try:
    print("Starting GUI...")
    root.mainloop()
except KeyboardInterrupt:
    print("Script interrupted.")


