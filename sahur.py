from datetime import datetime
import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient, events, Filters

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

def get_prayer_times(city):
    url = f'https://namazvakitleri.diyanet.gov.tr/tr-TR/{city}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    prayer_times = []
    for time in soup.find_all('span', class_='vakit-title'):
        prayer_times.append(time.text.strip())
    return prayer_times

@client.on(events.NewMessage(pattern='/iftar'))
async def iftar_handler(event):
    city = event.raw_text.split(' ')[1]
    prayer_times = get_prayer_times(city)
    iftar_time = prayer_times[5]  # Iftar time is at index 5
    await event.respond(f'Iftar time in {city}: {iftar_time}')

@client.on(events.NewMessage(pattern='/ezan'))
async def ezan_handler(event):
    city = event.raw_text.split(' ')[1]
    prayer_times = get_prayer_times(city)
    ezan_time = prayer_times[0]  # Fajr time is at index 0
    await event.respond(f'Ezan time in {city}: {ezan_time}')

@client.on(events.NewMessage(pattern='/sahur'))
async def sahur_handler(event):
    city = event.raw_text.split(' ')[1]
    prayer_times = get_prayer_times(city)
    sahur_time = prayer_times[0]  # Fajr time is at index 0
    await event.respond(f'Sahur time in {city}: {sahur_time}')

client.run_until_disconnected()
