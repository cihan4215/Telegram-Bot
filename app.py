import os
import threading
import datetime
import re
from flask import Flask
from telethon import TelegramClient, events

# ——— Flask “keep-alive” server ———
app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Bot is running!'

# ——— Telegram bot ayarları ———
api_id = 26294863  # Telegram API ID
api_hash = '4d2eb4aa34d63fb07fc0bb94d51c682d'  # Telegram API Hash
phone = '+923331704687'  # Telefon numarası

# Telegram Client (session ismi 'session')
client = TelegramClient('session', api_id, api_hash)

# Kanal ayarları
source_channel_ids = [
    -1002500350398, -1002130943146, -1001662061478, -1001722849883,
    # … diğer kanallar
]
DESTINATION_CHANNEL_ID = -1001835842902  # Hedef kanal ID

keywords = ['ECA', 'eca', 'Launching', 'Soon', 'Prelaunch',
            'Pre-Launch', 'PreCall', 'Pre', 'Mc', 'Tomorrow']
bad_words = ['Launched', 'Called', 'Pinksale', 'Ethereum', 'SOL', 'solana']

# Telegram event handler
@client.on(events.NewMessage(chats=source_channel_ids))
async def handler(event):
    text = event.raw_text
    if any(re.search(rf'\b{re.escape(w)}\b', text, re.IGNORECASE) for w in bad_words):
        print(f"{datetime.datetime.now()} ❌ Bad word in {event.chat_id}")
        return
    for kw in keywords:
        if re.search(rf'\b{re.escape(kw)}\b', text, re.IGNORECASE):
            print(f"{datetime.datetime.now()} ✅ Found “{kw}” in {event.chat_id}")
            await event.forward_to(DESTINATION_CHANNEL_ID)
            return
    print(f"{datetime.datetime.now()} ℹ️ No keyword in {event.chat_id}")

# Bot başlatma fonksiyonu
def run_bot():
    print("Starting Telegram client...")
    client.start(phone=phone)  # Render'da login olduktan sonra tekrar login olmana gerek yok
    client.run_until_disconnected()

# Flask server ve Telegram botu paralel çalıştır
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=port),
        daemon=True
    ).start()
    run_bot()
