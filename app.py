import os
import asyncio
import aiohttp  # async HTTP requests
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '7595003208:AAFBlTgzSsssGWyTHza4Z49KwABOLUU-KQ8'  # Your Telegram bot token here

app = Flask(__name__)

# === Telegram Bot Handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! This bot sends crypto price alerts.\n"
        "Use /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/price - Get current Bitcoin price\n"
        "/subscribe - Subscribe for premium alerts (coming soon)\n"
    )

# Function to get Bitcoin price from CoinGecko API
async def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data['bitcoin']['usd']

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price_usd = await get_btc_price()
        await update.message.reply_text(f"Bitcoin price is ${price_usd} USD.")
    except Exception as e:
        await update.message.reply_text("Sorry, I couldn't fetch the price right now.")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Placeholder for Stripe subscription integration
    await update.message.reply_text(
        "Subscription feature is coming soon! Stay tuned."
    )

# === Flask routes ===

@app.route('/')
def index():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    # Run async bot update processing in sync route
    asyncio.run(app.application.process_update(update))
    return "OK"

# === Main section to start the bot and Flask app ===

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}")

    # Build the bot application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("subscribe", subscribe))

    # Save the bot and application objects on Flask app for webhook use
    app.bot = application.bot
    app.application = application

    # Run Flask app (development server)
    app.run(host="0.0.0.0", port=port)
