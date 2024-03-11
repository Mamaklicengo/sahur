from telethon.sync import TelegramClient, events
import requests
from bs4 import BeautifulSoup
from datetime import datetime

api_id = '21119132'
api_hash = 'c0a90d0ba66e6bdea356894a55f4856e'
bot_token = '6531499751:AAGHzxki3QsflZqnh3wnk_1qF-yZE5YJxtw'

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern='/sahur'))
async def sahur_handler(event):
    il = event.raw_text.split('/sahur ')[1]
    imsakiye_url = f'https://www.mynet.com/ramazan/imsakiye/{il}'
    response = requests.get(imsakiye_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    sahur_time = soup.find('div', class_='İmsak').text
    await event.reply(f"Sahur saati {sahur_time}")

@client.on(events.NewMessage(pattern='/iftar'))
async def iftar_handler(event):
    il = event.raw_text.split('/iftar ')[1]
    imsakiye_url = f'https://www.mynet.com/ramazan/imsakiye/{il}'
    response = requests.get(imsakiye_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    iftar_time = soup.find('div', class_='Akşam').text
    await event.reply(f"Iftar saati {iftar_time}")

client.start(bot_token=bot_token)
client.run_until_disconnected()
