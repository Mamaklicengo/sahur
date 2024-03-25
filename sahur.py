from datetime import datetime, timedelta
from functools import reduce
from re import DOTALL, sub

from bs4 import BeautifulSoup
from requests import get

from pyrogram import Client, filters

# Sehirlerin ID'leri ve isimleri
sehirler = {
    "Adana": 9146,
    "Osmaniye": 9788,
    "Duzce": 9414,
}

async def get_prayer_times(city_id: int):
    today = datetime.now().strftime("%d.%m.%Y")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    
    # Diyanet Namaz Vakitleri sayfasından verileri çekme
    response = get(f"https://namazvakitleri.diyanet.gov.tr/tr-TR/{city_id}")
    soup = BeautifulSoup(response.content, 'html.parser')
    table_rows = soup.find_all("tr")
    
    # Bugünkü ve yarının vakitlerini alma
    today_times = table_rows[1].find_all("td")
    tomorrow_times = table_rows[2].find_all("td")
    
    # Vakitlerin listeye eklenmesi
    today_prayer_times = [time.text.strip() for time in today_times]
    tomorrow_prayer_times = [time.text.strip() for time in tomorrow_times]
    
    return today_prayer_times, tomorrow_prayer_times

async def remaining_time(city_id: int, prayer_type: str):
    today_times, tomorrow_times = await get_prayer_times(city_id)
    
    # Vakitlerin alınması
    if prayer_type == "sahur":
        prayer_time = today_times[1]  # Sahur vakti
    elif prayer_type == "iftar":
        prayer_time = today_times[5]  # Iftar vakti
        
    # Şu anki zaman ve namaz vakti
    current_time = datetime.now()
    prayer_datetime = datetime.strptime(f"{today} {prayer_time}", "%d.%m.%Y %H:%M")
    
    # Eğer vakit geçmişse yarının vakitlerini al
    if current_time > prayer_datetime:
        if prayer_type == "sahur":
            prayer_time = tomorrow_times[1]  # Yarının sahur vakti
        elif prayer_type == "iftar":
            prayer_time = tomorrow_times[5]  # Yarının iftar vakti
    
    prayer_datetime = datetime.strptime(f"{today} {prayer_time}", "%d.%m.%Y %H:%M")
    remaining_time = prayer_datetime - current_time
    
    hours_left = remaining_time.seconds // 3600
    minutes_left = (remaining_time.seconds % 3600) // 60
    
    if hours_left == 0:
        return f"{prayer_time} ({minutes_left} dakika kaldı)"
    elif minutes_left == 0:
        return f"{prayer_time} ({hours_left} saat kaldı)"
    else:
        return f"{prayer_time} ({hours_left} saat {minutes_left} dakika kaldı)"

app = Client("Ramazan", bot_token="6704245576:AAGqYQrMMuH2yt2sHJ9Zhk7q2wtNrDA_Eow")

@app.on_message(filters.command(["iftar"]))
async def iftar_handler(_, message):
    try:
        params = message.text.split()[1:]
        if len(params) < 1:
            await message.reply_text("Hatalı Kullanım!\nDoğru Kullanım: /iftar Adana")
            return

        city = params[0].capitalize()
        city_id = sehirler.get(city)

        if city_id:
            remaining = await remaining_time(city_id, "iftar")
            await message.reply_text(f"{city} için bugünkü iftar saati: {remaining}\nAllah orucunu kabul etsin😌.")
        else:
            await message.reply_text("Belirtilen şehir bulunamadı.")
    except Exception as e:
        print(str(e))
        await message.reply_text("Bir hata oluştu.")

@app.on_message(filters.command(["sahur"]))
async def sahur_handler(_, message):
    try:
        params = message.text.split()[1:]
        if len(params) < 1:
            await message.reply_text("Hatalı Kullanım!\nDoğru Kullanım: /sahur Adana")
            return

        city = params[0].capitalize()
        city_id = sehirler.get(city)

        if city_id:
            remaining = await remaining_time(city_id, "sahur")
            await message.reply_text(f"{city} için bugünkü sahur saati: {remaining}\nNiyet etmeyi unutma☺.")
        else:
            await message.reply_text("Belirtilen şehir bulunamadı.")
    except Exception as e:
        print(str(e))
        await message.reply_text("Bir hata oluştu.")

app.run()
