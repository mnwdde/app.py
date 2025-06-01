'7595003208:AAFBlTgzSsssGWyTHza4Z49KwABOLUU-KQ8'  # Put your real token here

from flask import Flask, request
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '7595003208:AAFBlTgzSsssGWyTHza4Z49KwABOLUU-KQ8'

app = Flask(__name__)

# Define your /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Bot is running.')

# Create the bot application
application = ApplicationBuilder().token(TOKEN).build()

# Add handlers
application.add_handler(CommandHandler("start", start))

@app.route('/')
def index():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
