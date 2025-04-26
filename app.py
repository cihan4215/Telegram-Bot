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
api_id = 26294863  # Telegram API ID'niz
api_hash = '4d2eb4aa34d63fb07fc0bb94d51c682d'  # Telegram API Hash'iniz
phone = '+923331704687'  # Telefon numaranız

# Session dosyası
session_file = '+923331704687.session'  # Lokal session dosyanızın ismi

# Telegram Client
client = TelegramClient(session_file, api_id, api_hash)

# Takip edilecek kanallar
source_channel_ids = [
    -1002500350398, -1002130943146, -1001662061478, -1001722849883,
    # ... diğer kanallar
]
DESTINATION_CHANNEL_ID = -1001835842902  # Mesajları ileteceğin kanal ID'si

# Kelime filtreleri
keywords = ['ECA', 'eca', 'Launching', 'Soon', 'Prelaunch', 'Pre-Launch', 'PreCall', 'Pre', 'Mc', 'Tomorrow']
bad_words = ['Launched', 'Called', 'Pinksale', 'Ethereum', 'SOL', 'solana']

# Yeni mesaj geldiğinde çalışacak
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

# Botu başlat
def run_bot():
    if not os.path.exists(session_file):
        print("Session dosyası bulunamadı! Giriş yapman lazım.")
    else:
        print("Session dosyası bulundu, client bağlanıyor...")
    
    client.connect()
    if not client.is_user_authorized():
        print("Kullanıcı giriş yapmamış. Lütfen önce lokalde doğrulama yap.")
        exit(1)
    
    client.run_until_disconnected()

# Flask server ve bot paralel çalışacak
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True).start()
    run_bot()
