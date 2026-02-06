import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

PRODUCT_URL = (
    "https://www.firstcry.com/hot-wheels/"
    "hot-wheels-second-story-lorry-die-cast-free-wheel-car-transport-truck-red/"
    "22159210/product-detail"
)
PRODUCT_NAME = "Hot Wheels Second Story Lorry Die Cast Free Wheel Car Transport Truck - Red"

IST = timezone(timedelta(hours=5, minutes=30))

GREEN_API_URL = os.environ.get("GREEN_API_URL", "")
GREEN_API_ID = os.environ.get("GREEN_API_ID", "")
GREEN_API_TOKEN = os.environ.get("GREEN_API_TOKEN", "")
WHATSAPP_GROUP_ID = os.environ.get("WHATSAPP_GROUP_ID", "")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def check_stock() -> bool:
    response = requests.get(PRODUCT_URL, headers=HEADERS, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(separator=" ").lower()

    out_of_stock_signals = [
        "out of stock",
        "sold out",
        "currently unavailable",
        "notify me",
    ]
    for signal in out_of_stock_signals:
        if signal in page_text:
            return False

    add_to_cart = soup.find("button", string=lambda t: t and "add to" in t.lower())
    if add_to_cart:
        return True

    return False


def send_whatsapp_group(message: str):
    url = (
        f"{GREEN_API_URL}/waInstance{GREEN_API_ID}"
        f"/sendMessage/{GREEN_API_TOKEN}"
    )
    payload = {
        "chatId": WHATSAPP_GROUP_ID,
        "message": message,
    }
    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code == 200:
        print("WhatsApp group message sent!")
    else:
        print(f"Failed: {resp.status_code} — {resp.text}")
        sys.exit(1)


def main():
    missing = []
    if not GREEN_API_URL:
        missing.append("GREEN_API_URL")
    if not GREEN_API_ID:
        missing.append("GREEN_API_ID")
    if not GREEN_API_TOKEN:
        missing.append("GREEN_API_TOKEN")
    if not WHATSAPP_GROUP_ID:
        missing.append("WHATSAPP_GROUP_ID")
    if missing:
        print(f"ERROR: Missing secrets: {', '.join(missing)}")
        sys.exit(1)

    now = datetime.now(IST)
    print(f"[{now:%Y-%m-%d %I:%M:%S %p} IST] Checking: {PRODUCT_NAME}")

    try:
        in_stock = check_stock()
    except Exception as e:
        print(f"Error checking stock: {e}")
        sys.exit(1)

    if in_stock:
        print("IN STOCK! Sending group alert …")
        message = (
            f"🟢 *STOCK ALERT!*\n\n"
            f"*{PRODUCT_NAME}*\n"
            f"is now *IN STOCK* on FirstCry!\n\n"
            f"🕐 Time: {now:%d-%b-%Y %I:%M:%S %p} IST\n\n"
            f"🔗 Buy now:\n{PRODUCT_URL}"
        )
        send_whatsapp_group(message)
    else:
        print("Still out of stock.")


if __name__ == "__main__":
    main()
