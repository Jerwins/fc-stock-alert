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

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

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


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code == 200:
        print("Telegram notification sent!")
    else:
        print(f"Failed: {resp.status_code} — {resp.text}")
        sys.exit(1)


def main():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("ERROR: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID secrets are not set.")
        sys.exit(1)

    now = datetime.now(IST)
    print(f"[{now:%Y-%m-%d %I:%M:%S %p} IST] Checking: {PRODUCT_NAME}")

    try:
        in_stock = check_stock()
    except Exception as e:
        print(f"Error checking stock: {e}")
        sys.exit(1)

    if TEST_MODE:
        print("TEST MODE — sending test message …")
        message = (
            f"✅ *TEST — Bot is working!*\n\n"
            f"Monitoring: *{PRODUCT_NAME}*\n"
            f"Status: {'IN STOCK ✅' if in_stock else 'Out of stock ❌'}\n"
            f"🕐 Time: {now:%d-%b-%Y %I:%M:%S %p} IST"
        )
        send_telegram(message)
    elif in_stock:
        print("IN STOCK! Sending Telegram alert …")
        message = (
            f"🟢 *STOCK ALERT!*\n\n"
            f"*{PRODUCT_NAME}*\n"
            f"is now *IN STOCK* on FirstCry!\n\n"
            f"🕐 Time: {now:%d-%b-%Y %I:%M:%S %p} IST\n\n"
            f"🔗 [Buy now]({PRODUCT_URL})"
        )
        send_telegram(message)
    else:
        print("Still out of stock.")


if __name__ == "__main__":
    main()
