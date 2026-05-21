# Crypto Price Monitoring Telegram Bot

An asynchronous Telegram bot built with **Aiogram 3** and **SQLAlchemy 2.0**. It allows users to check current cryptocurrency prices and subscribe to custom price alerts (both for growth and drops). The background monitor runs periodically to check active subscriptions and notify users instantly when their target price is hit.

---

## 🚀 Features

* **Asynchronous Architecture:** Built using `asyncio` and `aiogram` to handle multiple user requests efficiently without blocking the event loop.
* **Database Integration:** Uses **PostgreSQL** with `asyncpg` as an asynchronous dialect and **SQLAlchemy ORM** for safe data persistence.
* **Custom Subscriptions:** Users can set target price alerts using simple text commands (e.g., `/subscribe bitcoin 75000`).
* **Efficient Background Monitoring:** A periodic background task fetches live prices from the CoinGecko API, filters triggered subscriptions entirely on the database side using optimized SQL queries, and sends bulk-deleted alerts to avoid race conditions.
* **Clean Code Structure:** Separated into distinct layers (`bot handlers`, `database models`, `core configuration`, and `background services`).

---

## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Framework:** Aiogram 3.x (Telegram Bot API)
* **ORM:** SQLAlchemy 2.0 (Async)
* **Database Driver:** asyncpg (PostgreSQL)
* **HTTP Client:** aiohttp / httpx (for async API requests)
* **Containerization:** Docker & Docker Compose

---

## 📂 Project Structure

``` text
Telegram Bot Monitoring/
├── bot/
│   ├── __init__.py
│   └── handlers.py         # Command handlers (/start, /crypto, /subscribe)
├── core/
│   ├── __init__.py
│   └── config.py           # Environment variables & configuration
├── db/
│   ├── engine.py           # Async engine and session local setup
│   └── models.py           # SQLAlchemy database models (User, Subscription)
├── services/
│   ├── __init__.py
│   ├── api_client.py       # CoinGecko API integration
│   └── monitor.py          # Background tracking loop
├── .env.example            # Sample configuration file
├── .gitignore              # Git ignore rules
├── docker-compose.yml      # Docker multi-container setup
├── main.py                 # Bot entry point
└── requirements.txt        # Project dependencies
```
1. Clone the repository
Bash
git clone [https://github.com/yourusername/crypto-monitor-bot.git](https://github.com/yourusername/crypto-monitor-bot.git)
cd crypto-monitor-bot
2. Configure Environment Variables
Copy the sample environment file and fill in your actual Telegram Bot Token and Database credentials:

Bash
cp .env.example .env
3. Install Dependencies
Create a virtual environment and install the required packages:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
4. Run the Application
Bash
python main.py
🤖 Bot Commands
/start - Register the user in the database and display a welcome message.

/crypto - Fetch and display the current live Bitcoin price.

/subscribe [ticker] [target_price] - Create a price alert. Example: /subscribe bitcoin 82500


