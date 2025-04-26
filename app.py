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
api_id = 21830452
api_hash = '2852cd53b42fc0e57bdcf9e29f0ae71e'
phone = '+923271343743'  # Telefon numarasını buraya sabitleyin
client = TelegramClient(f'{phone}_session', api_id, api_hash)

source_channel_ids = [
    -1002500350398, -1001963997401, -1001662061478, -1001722849883,
    # … istediğin diğer kanallar
]
DESTINATION_CHANNEL_ID = -1002436534012

keywords = ['ECA', 'eca', 'Launching', 'Soon', 'Prelaunch',
            'Pre-Launch', 'PreCall', 'Pre', 'Tomorrow']
bad_words = ['Launched', 'Called', 'Pinksale', 'Ethereum', 'SOL', 'solana']

@client.on(events.NewMessage(chats=source_channel_ids))
async def handler(event):
    text = event.raw_text
    # Kötü kelime filtresi
    if any(re.search(rf'\b{re.escape(w)}\b', text, re.IGNORECASE) for w in bad_words):
        print(f"{datetime.datetime.now()} ❌ Bad word in {event.chat_id}")
        return
    # Anahtar kelime kontrolü
    for kw in keywords:
        if re.search(rf'\b{re.escape(kw)}\b', text, re.IGNORECASE):
            print(f"{datetime.datetime.now()} ✅ Found “{kw}” in {event.chat_id}")
            await event.forward_to(DESTINATION_CHANNEL_ID)
            return
    print(f"{datetime.datetime.now()} ℹ️ No keyword in {event.chat_id}")

def run_bot():
    client.start()
    print("🤖 Bot started, listening…")
    client.run_until_disconnected()

if __name__ == '__main__':
    # 1) Flask’ı arka planda ayağa kaldır
    port = int(os.environ.get('PORT', 8000))
    threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False),
        daemon=True
    ).start()

    # 2) Telegram botu çalıştır
    run_bot()
