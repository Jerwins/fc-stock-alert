import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from urllib.parse import quote

PRODUCT_URL = (
    "https://www.firstcry.com/hot-wheels/"
    "hot-wheels-second-story-lorry-die-cast-free-wheel-car-transport-truck-red/"
    "22159210/product-detail"
)
PRODUCT_NAME = "Hot Wheels Second Story Lorry Die Cast Free Wheel Car Transport Truck - Red"

IST = timezone(timedelta(hours=5, minutes=30))

WHATSAPP_MEMBERS = os.environ.get("WHATSAPP_MEMBERS", "")

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


def send_whatsapp(phone: str, apikey: str, message: str):
    encoded_msg = quote(message)
    url = (
        f"https://api.callmebot.com/whatsapp.php"
        f"?phone={phone}"
        f"&text={encoded_msg}"
        f"&apikey={apikey}"
    )
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        print(f"  -> Sent to {phone}")
    else:
        print(f"  -> FAILED for {phone}: {resp.status_code} — {resp.text}")


def notify_group(message: str):
    members = json.loads(WHATSAPP_MEMBERS)
    print(f"Notifying {len(members)} group member(s) …")
    for member in members:
        send_whatsapp(member["phone"], member["apikey"], message)


def main():
    if not WHATSAPP_MEMBERS:
        print("ERROR: WHATSAPP_MEMBERS secret is not set.")
        sys.exit(1)

    now = datetime.now(IST)
    print(f"[{now:%Y-%m-%d %I:%M:%S %p} IST] Checking stock for: {PRODUCT_NAME}")

    try:
        in_stock = check_stock()
    except Exception as e:
        print(f"Error checking stock: {e}")
        sys.exit(1)

    if in_stock:
        print("IN STOCK! Sending WhatsApp alerts …")
        message = (
            f"🟢 *STOCK ALERT!*\n\n"
            f"*{PRODUCT_NAME}*\n"
            f"is now *IN STOCK* on FirstCry!\n\n"
            f"🕐 Time: {now:%d-%b-%Y %I:%M:%S %p} IST\n\n"
            f"🔗 Buy now:\n{PRODUCT_URL}"
        )
        notify_group(message)
    else:
        print("Still out of stock.")


if __name__ == "__main__":
    main()
