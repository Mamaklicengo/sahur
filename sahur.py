from datetime import datetime, timedelta
from functools import reduce
from re import DOTALL, sub

from bs4 import BeautifulSoup
from requests import get

from telegram.ext import Updater, CommandHandler

# Sadece Adana şehrini ekliyoruz, diğer şehirleri istediğiniz gibi ekleyebilirsiniz
sehirler = ['01 Adana 9146']

# Diyanet Namaz Vakitleri web sitesinden şehre göre namaz vakitlerini al
def get_prayer_times(city):
    url = f"https://namazvakitleri.diyanet.gov.tr/tr-TR/{city}"
    response = get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

# Şehir adına göre il kodunu bul
def find_location(city):
    city = city.lower().capitalize()  # Büyük harfle başlat
    for item in sehirler:
        if city in item:
            return item.split()[0]  # İl kodunu döndür
    return None

# Namaz vakitlerini ve sahur, iftar saatlerini göster
def show_prayer_times(update, context):
    if len(context.args) < 2:
        update.message.reply_text("Lütfen bir şehir adı ve komutu belirtin. Örneğin: /namaz istanbul")
        return

    city = context.args[0]
    command = context.args[1].lower()

    if command not in ["sahur", "iftar", "ezan"]:
        update.message.reply_text("Geçersiz komut. Lütfen 'sahur', 'iftar' veya 'ezan' komutlarını kullanın.")
        return

    location_code = find_location(city)
    if not location_code:
        update.message.reply_text("Belirtilen şehir bulunamadı.")
        return

    prayer_times = get_prayer_times(location_code)
    if not prayer_times:
        update.message.reply_text("Namaz vakitleri alınamadı. Lütfen daha sonra tekrar deneyin.")
        return

    soup = BeautifulSoup(prayer_times, "html.parser")
    prayer_table = soup.find("table", {"class": "table m-0"})

    if not prayer_table:
        update.message.reply_text("Namaz vakitleri bulunamadı. Lütfen daha sonra tekrar deneyin.")
        return

    rows = prayer_table.find_all("tr")
    times = {}

    for row in rows:
        columns = row.find_all("td")
        if columns:
            vakit = columns[0].text.strip()
            saat = columns[1].text.strip()
            times[vakit] = saat

    if command == "ezan":
        message = f"**{city.capitalize()} Ezan Vakitleri**\n\n"
        for vakit, saat in times.items():
            message += f"{vakit}: {saat}\n"
    else:
        target_time = None
        if command == "sahur":
            target_time = times.get("Sahur")
        elif command == "iftar":
            target_time = times.get("İftar")

        if not target_time:
            update.message.reply_text(f"{city.capitalize()} için {command} vakiti bulunamadı.")
            return

        target_datetime = datetime.strptime(target_time, "%H:%M")
        current_datetime = datetime.now()
        if current_datetime > target_datetime:
            target_datetime += timedelta(days=1)

        remaining_time = target_datetime - current_datetime
        hours_left = remaining_time.seconds // 3600
        minutes_left = (remaining_time.seconds % 3600) // 60

        message = f"**{city.capitalize()} {command.capitalize()} Saati ve Kalan Süre**\n"
        message += f"{target_time}: {hours_left} saat {minutes_left} dakika kaldı."

    update.message.reply_text(message)

# Botu başlat
def main():
    updater = Updater("6704245576:AAGqYQrMMuH2yt2sHJ9Zhk7q2wtNrDA_Eow", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("namaz", show_prayer_times))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
