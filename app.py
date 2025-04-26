import os
import threading
import datetime
from flask import Flask
from telethon import TelegramClient, events

# Flask server setup
app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Bot is running!'

# Telegram bot settings
api_id = 26294863  # Your Telegram API ID
api_hash = '4d2eb4aa34d63fb07fc0bb94d51c682d'  # Your Telegram API Hash
phone = '+923331704687'  # Your Telegram phone number

# Define the session file location
session_file = 'my_telegram_session.session'  # Ensure this file is on Render's environment

# Telegram Client
client = TelegramClient(session_file, api_id, api_hash)

source_channel_ids = [
    -1002500350398, -1002130943146, -1001662061478, -1001722849883,
    # Add more channels here
]
DESTINATION_CHANNEL_ID = -1001835842902  # The channel where messages will be forwarded

keywords = ['ECA', 'eca', 'Launching', 'Soon', 'Prelaunch', 'Pre-Launch', 'PreCall', 'Pre', 'Mc', 'Tomorrow']
bad_words = ['Launched', 'Called', 'Pinksale', 'Ethereum', 'SOL', 'solana']

# Telegram event handler
@client.on(events.NewMessage(chats=source_channel_ids))
async def handler(event):
    text = event.raw_text
    # Bad word filter
    if any(word in text.lower() for word in bad_words):
        print(f"{datetime.datetime.now()} ❌ Bad word in {event.chat_id}")
        return
    # Keyword check
    for kw in keywords:
        if kw.lower() in text.lower():
            print(f"{datetime.datetime.now()} ✅ Found '{kw}' in {event.chat_id}")
            await event.forward_to(DESTINATION_CHANNEL_ID)
            return
    print(f"{datetime.datetime.now()} ℹ️ No keyword in {event.chat_id}")

# Bot start function
def run_bot():
    if not os.path.exists(session_file):
        print("Session file not found, starting Telegram authentication...")
        # Start the Telegram client without needing input()
        client.start(phone=phone)  # This triggers authentication without waiting for input
        print("Authentication successful!")
    else:
        print("Session file found, starting bot directly.")
    
    client.run_until_disconnected()

# Run Flask and Telegram bot together
if __name__ == '__main__':
    # Set the port for Flask server (Render/Heroku automatically assign this)
    port = int(os.environ.get('PORT', 8000))

    # Run Flask server in the background
    threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=port),
        daemon=True
    ).start()

    # Start the Telegram bot
    run_bot()
