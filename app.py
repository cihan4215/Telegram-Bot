from telethon import TelegramClient, events
import datetime
import re

# Telegram API bilgilerin
api_id = 26294863
api_hash = '4d2eb4aa34d63fb07fc0bb94d51c682d'
phone = '+923331704687'

# Telegram Client başlat
client = TelegramClient(phone, api_id, api_hash)

# Takip edilecek kaynak kanal ID'leri
source_channel_ids = [
    -1002500350398, -1001963997401, -1001662061478, -1001722849883,
    # ... Diğerlerini buraya ekleyebilirsin ...
]

# Hedef kanal ID'si (mesajların gönderileceği kanal)
DESTINATION_CHANNEL_ID = -1001835842902

# Anahtar kelimeler
keywords = ['ECA', 'eca', 'Launching', 'Soon', 'Prelaunch', 'Pre-Launch', 'PreCall', 'Pre', 'Tomorrow']

# Engellenen kelimeler
bad_words = ['Launched', 'Called', 'Pinksale', 'Ethereum', 'SOL', 'solana']

@client.on(events.NewMessage(chats=source_channel_ids))
async def handler(event):
    # Önce kötü kelime içeriyor mu kontrol et
    if any(re.search(r'\b' + re.escape(bad_word) + r'\b', event.raw_text, re.IGNORECASE) for bad_word in bad_words):
        print(f"{datetime.datetime.now()} - Kötü kelime içeriyor: {event.chat_id}")
        return

    # Anahtar kelime içeriyor mu kontrol et
    for keyword in keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', event.raw_text, re.IGNORECASE):
            print(f"{datetime.datetime.now()} - Anahtar kelime bulundu: {keyword} - {event.chat_id}")
            await event.forward_to(DESTINATION_CHANNEL_ID)
            return

    print(f"{datetime.datetime.now()} - Anahtar kelime bulunamadı: {event.chat_id}")

# Client başlat
client.start()
print("✅ Bot çalışıyor... Gelen mesajları dinliyor.")
client.run_until_disconnected()
