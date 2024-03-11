from telethon import TelegramClient, events
import requests
from bs4 import BeautifulSoup
import datetime

bot_token = '6531499751:AAGHzxki3QsflZqnh3wnk_1qF-yZE5YJxtw' # Bot Tokeni
api_id = '21119132' # Api ID
api_hash = 'c0a90d0ba66e6bdea356894a55f4856e' # Api Hash

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('👋 Merhaba ben Telegramın eğlence botuyum\n\n İşte sana yapabildiğim herşeyi tek tek yazıyorum🤭\n\nBurç yorumu için yorumunu almak istediğiniz burcu başına / koyarak yazın örnek: /burc Koc\n\nEros aşkın oku /ask komutu ile grubundaki iki kişiyi birbirine shipler🏹👩‍❤️‍👨\n\nSayı tahmin oyunu komutu /sayi oyunu durdurmak için /tahminbitir komutlarını kullanabilirsiniz🔢\n\ndoğruluk ve cesaretlilik sorusu alabilirsiniz\n komutlar: \n/d = doğruluk sorusu sorar.\n/c = Cesaret sorusu sorar.\n\nEğer bir sorun oluşursa 👨‍💻 @yoodelidegilim kişisi ile iletişime geçebilirsiniz📞\n\nDiğer botlarımız için kanalımızı ziyaret edebilirsiniz ⚙ @Mamaklibots')

@bot.on(events.NewMessage(pattern='/sahur'))
async def get_horoscope(event):
    burclar = ['Ankara', 'Boga', 'Ikizler', 'Yengec', 'Aslan', 'Basak', 'Terazi', 'Akrep', 'Yay', 'Oglak', 'Kova', 'Balik']
    message = event.raw_text.split(' ')[1].lower()
    if message.capitalize() in burclar:
        await event.respond(get_horoscope(message))
    else:
        await event.respond('Geçerli bir burç giriniz.')

def get_horoscope(burc):
    url = f'https://www.mynet.com/ramazan/imsakiye/{burc.lower()}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    horoscope = soup.find(class_='detail-content-box')
    date = datetime.date.today().strftime('%d.%m.%Y')
    horoscope_text = horoscope.get_text()
    message_lines = horoscope_text.split('\n')
    selected_lines = message_lines[10:110]
    selected_text = '\n'.join(selected_lines)
    return f'{date} tarihli {burc.capitalize()} burcu yorumu:\n\n{selected_text}'

bot.run_until_disconnected()
