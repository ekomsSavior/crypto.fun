import requests
import time
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

# Function to fetch Bitcoin price
def get_bitcoin_price():
    try:
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        data = response.json()
        return f"BTC: ${data['bpi']['USD']['rate']}"
    except Exception as e:
        return "Error fetching price"

# Function to update the tray icon title
def update_icon(icon):
    while icon.visible:
        price = get_bitcoin_price()
        icon.title = price
        time.sleep(60)  # Update every 60 seconds

# Function to create an icon image
def create_image():
    size = (64, 64)
    image = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, *size), fill="black")
    return image

# Function to quit the app
def quit_app(icon, item):
    icon.stop()

# Menu and icon setup
menu = Menu(MenuItem("Quit", quit_app))
icon = Icon("Bitcoin Price", create_image(), menu=menu)

# Start the app
icon.run(setup=lambda: update_icon(icon))