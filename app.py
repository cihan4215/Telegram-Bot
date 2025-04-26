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
api_id = 21830452  # Telegram API ID'nizi buraya girin
api_hash = '2852cd53b42fc0e57bdcf9e29f0ae71e'  # Telegram API Hash'inizi buraya girin
phone = '+923271343743'  # Telegram telefon numaranız
client = TelegramClient(phone, api_id, api_hash)

source_channel_ids = [
    -1002500350398, -1002130943146, -1001662061478, -1001722849883,
    # … istediğiniz diğer kanallar
]
DESTINATION_CHANNEL_ID = -1001835842902  # Mesajları göndereceğiniz kanal ID'si

keywords = ['ECA', 'eca', 'Launching', 'Soon', 'Prelaunch',
            'Pre-Launch', 'PreCall', 'Pre', 'Mc', 'Tomorrow']
bad_words = ['Launched', 'Called', 'Pinksale', 'Ethereum', 'SOL', 'solana']

# Telegram event handler
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

# Bot başlatma fonksiyonu
def run_bot():
    session_file = f'{phone}.session'

    # Eğer session dosyası varsa, eski session dosyasını silelim
    if os.path.exists(session_file):
        print("Eski session dosyası bulunuyor, siliniyor...")
        os.remove(session_file)

    # Eğer session dosyası yoksa, doğrulama işlemi başlatılacak
    if not os.path.exists(session_file):
        print("Session dosyası bulunamadı, Telegram doğrulaması başlatılıyor...")
        client.start()  # Bu komut, kullanıcıyı doğrulama işlemi için yönlendirecektir
        print("Doğrulama başarılı!")
    else:
        print("Session dosyası mevcut, doğrudan botu başlatıyoruz.")
    
    client.run_until_disconnected()

# Flask server'ı ve Telegram botunu paralel çalıştır
if __name__ == '__main__':
    # Flask server'ı için port numarasını belirleyin (Render/Heroku gibi platformlarda otomatik alır)
    port = int(os.environ.get('PORT', 8000))

    # Flask server'ı arka planda çalıştır
    threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=port),
        daemon=True
    ).start()

    # Telegram botunu çalıştır
    run_bot()
