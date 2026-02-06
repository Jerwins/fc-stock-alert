# FirstCry Stock Monitor Bot

Monitors [Hot Wheels Second Story Lorry](https://www.firstcry.com/hot-wheels/hot-wheels-second-story-lorry-die-cast-free-wheel-car-transport-truck-red/22159210/product-detail) on FirstCry and sends a **Telegram group** notification when it comes back in stock.

Runs free in the cloud via **GitHub Actions** — checks every 5 minutes.

---

## Setup (one-time, ~5 minutes)

### Step 1 — Create a Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather).
2. Send `/newbot`, pick a name and username.
3. BotFather replies with your **Bot Token** — copy it.

### Step 2 — Create a group and get the Chat ID

1. Create a Telegram group and add your bot to it.
2. Send any message in the group.
3. Open this URL in your browser (replace `BOT_TOKEN` with your token):
   ```
   https://api.telegram.org/botBOT_TOKEN/getUpdates
   ```
4. In the JSON response, find `"chat":{"id":-100XXXXXXXXXX}` — that negative number is your **Chat ID**.

### Step 3 — Add secrets to GitHub

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| Secret Name          | Value                              |
|----------------------|------------------------------------|
| `TELEGRAM_BOT_TOKEN` | Token from BotFather               |
| `TELEGRAM_CHAT_ID`   | Group chat ID (e.g. `-1001234567890`) |

### Step 4 — Enable the workflow

Go to the **Actions** tab, enable workflows, and click **Run workflow** to test.

---

## How it works

- GitHub Actions runs the script every **5 minutes**.
- If the product is **in stock**, the bot sends a message to your Telegram group with the product name, buy link, and time (IST).
- If it's **out of stock**, nothing happens (no spam).
- Disable the workflow from the Actions tab once done.
