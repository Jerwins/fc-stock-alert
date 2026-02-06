# FirstCry Stock Monitor Bot

Monitors [Hot Wheels Second Story Lorry](https://www.firstcry.com/hot-wheels/hot-wheels-second-story-lorry-die-cast-free-wheel-car-transport-truck-red/22159210/product-detail) on FirstCry and sends WhatsApp notifications to your group when it comes back in stock.

Runs in the cloud via **GitHub Actions** (free) — checks every 5 minutes.

---

## Setup

### Step 1 — Each group member gets a CallMeBot API key

Every person who wants notifications must do this once:

1. Save **+34 644 31 89 93** in your phone contacts.
2. Send this WhatsApp message to that contact:
   ```
   I allow callmebot to send me messages
   ```
3. You'll get a reply with your **API key**. Save it.

### Step 2 — Add the secret to GitHub

Go to this repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.

Create a secret named `WHATSAPP_MEMBERS` with this JSON format:

```json
[
  { "phone": "+919876543210", "apikey": "123456" },
  { "phone": "+919876543211", "apikey": "789012" }
]
```

Add one entry per person in your group.

### Step 3 — Enable the workflow

Go to the **Actions** tab and enable workflows. Click **Run workflow** to test.

---

## How it works

- GitHub Actions runs the script every **5 minutes**.
- If the product is **in stock**, every member listed in `WHATSAPP_MEMBERS` gets a WhatsApp message with the product name, time (IST), and buy link.
- If it's **out of stock**, nothing happens.
- Disable the workflow from the Actions tab once you've bought the product.
