# FirstCry Stock Monitor Bot

Monitors [Hot Wheels Second Story Lorry](https://www.firstcry.com/hot-wheels/hot-wheels-second-story-lorry-die-cast-free-wheel-car-transport-truck-red/22159210/product-detail) on FirstCry and sends a **Telegram group** notification when it comes back in stock.

---

## How It Works

This bot runs entirely in the cloud using **GitHub Actions** — no server, no computer needs to be on.

### Workflow

1. **Every 5 minutes**, GitHub Actions automatically triggers the script (that's **288 checks per day**, 24/7).
2. The script **fetches the FirstCry product page** and scans the page content.
3. It looks for out-of-stock signals like `"out of stock"`, `"sold out"`, `"notify me"`, or `"currently unavailable"`.
4. **If the product is still out of stock** → it logs "Still out of stock" and does nothing. No message, no spam.
5. **If the product is back in stock** → it sends a Telegram message to your group with:
   - Product name
   - Detection time (IST)
   - Direct buy link

### Monitoring Schedule

| Detail             | Value                        |
|--------------------|------------------------------|
| Check interval     | Every 5 minutes              |
| Checks per hour    | 12                           |
| Checks per day     | 288                          |
| Runs 24/7          | Yes (GitHub Actions cron)    |
| Cost               | Free (GitHub free tier)      |

> **Note:** GitHub Actions cron jobs may occasionally have a delay of 1–5 minutes beyond the scheduled time. This is normal.

---

## Setup (one-time, ~5 minutes)

### Step 1 — Create a Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather).
2. Send `/newbot`, pick a name and username (must end in `bot`).
3. BotFather replies with your **Bot Token** — copy it.

### Step 2 — Create a group and get the Chat ID

1. Create a Telegram group and add your bot to it.
2. Send a message in the group tagging the bot: `@your_bot_username hello`
3. Open this URL in your browser (replace `YOUR_TOKEN` with your actual token):
   ```
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
   ```
4. In the JSON response, find `"chat":{"id":-100XXXXXXXXXX}` — that negative number is your **Chat ID**.

> **Tip:** If the result is empty, go to [@BotFather](https://t.me/BotFather) → `/mybots` → your bot → **Bot Settings** → **Group Privacy** → **Turn off**. Then remove and re-add the bot to the group, send a message, and try again.

### Step 3 — Add secrets to GitHub

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| Secret Name          | Value                                    |
|----------------------|------------------------------------------|
| `TELEGRAM_BOT_TOKEN` | Token from BotFather                     |
| `TELEGRAM_CHAT_ID`   | Group chat ID (e.g. `-1001234567890`)    |

### Step 4 — Enable and test the workflow

1. Go to the **Actions** tab in your repo and enable workflows.
2. Click **"FirstCry Stock Monitor"** → **"Run workflow"**.
3. Tick the **"Send a test message"** checkbox to verify Telegram is working.
4. Click the green **"Run workflow"** button.

You should receive a test message in your Telegram group within a minute.

---

## Disabling the Bot

Once you've bought the product, go to **Actions** → **"FirstCry Stock Monitor"** → click the **⋯** menu → **Disable workflow**.
