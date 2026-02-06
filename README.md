# FirstCry Stock Monitor Bot

Monitors [Hot Wheels Second Story Lorry](https://www.firstcry.com/hot-wheels/hot-wheels-second-story-lorry-die-cast-free-wheel-car-transport-truck-red/22159210/product-detail) on FirstCry and sends a WhatsApp **group** notification when it comes back in stock.

Runs in the cloud via **GitHub Actions** (free) — checks every 5 minutes.
Uses **GREEN-API** (free developer tier) to send messages directly to a WhatsApp group.

---

## Setup (one-time, ~10 minutes)

### Step 1 — Create a free GREEN-API account

1. Go to [https://console.green-api.com](https://console.green-api.com) and sign up.
2. Create an instance (free "Developer" plan).
3. Link your WhatsApp by scanning the QR code shown in the console.
4. From the instance dashboard, note down:
   - **API URL** (e.g. `https://api.green-api.com`)
   - **idInstance** (e.g. `1101234567`)
   - **apiTokenInstance** (e.g. `abc123def456...`)

### Step 2 — Get your WhatsApp Group ID

1. In the GREEN-API console, go to **API > Testing** or use Postman.
2. Call the `getContacts` endpoint — it lists all chats.
3. Find your group — its ID looks like `120363012345678901@g.us`.
4. Copy that Group ID.

Alternatively, use this API call:
```
GET {apiUrl}/waInstance{idInstance}/getContacts/{apiTokenInstance}
```
Look for entries with `@g.us` — those are groups.

### Step 3 — Add secrets to GitHub

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret** and add:

| Secret Name         | Value                                          |
|---------------------|-------------------------------------------------|
| `GREEN_API_URL`     | `https://api.green-api.com` (or your API URL)   |
| `GREEN_API_ID`      | Your idInstance (e.g. `1101234567`)              |
| `GREEN_API_TOKEN`   | Your apiTokenInstance                           |
| `WHATSAPP_GROUP_ID` | Your group chat ID (e.g. `120363...@g.us`)      |

### Step 4 — Enable the workflow

Go to the **Actions** tab in your repo, enable workflows, and click **Run workflow** to test.

---

## How it works

- GitHub Actions runs the script every **5 minutes**.
- If the product is **in stock**, a message is sent to your WhatsApp group with the product name, link, and time (IST).
- If it's **out of stock**, nothing happens.
- Disable the workflow from the Actions tab once you've bought the product.
