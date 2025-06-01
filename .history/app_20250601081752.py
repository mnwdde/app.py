from flask import Flask, request
import os
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = '7595003208:AAFBlTgzSsssGWyTHza4Z49KwABOLUU-KQ8'  # Put your real token here

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, None, workers=0)

app = Flask(__name__)

# Define your handlers here (start command, messages, etc.)
def start(update, context):
    update.message.reply_text("Hello! Bot is running.")

dp.add_handler(CommandHandler("start", start))

@app.route('/')
def index():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
