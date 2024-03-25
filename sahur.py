from datetime import datetime, timedelta
from functools import reduce
from re import DOTALL, sub

from bs4 import BeautifulSoup
from requests import get

from telegram.ext import Updater, CommandHandler

sehirler = {
    'Adana': '9146',
    'Adıyaman': '9158',
    'Afyonkarahisar': '9167',
    'Ağrı': '9185',
    'Amasya': '9198',
    # Diğer şehirleri buraya ekleyebilirsiniz
}

def get_prayer_times(city):
    url = f"https://namazvakitleri.diyanet.gov.tr/tr-TR/{city}"
    response = get(url)
    if response.status_code == 200:
        return response.content

def find_location(city):
    return sehirler.get(city.capitalize())

def show_prayer_times(update, context):
    if len(context.args) < 1:
        update.message.reply_text("Lütfen bir şehir adı belirtin. Örneğin: /sahur adana")
        return

    city = context.args[0]
    if city.lower() not in sehirler:
        update.message.reply_text("Belirtilen şehir bulunamadı.")
        return

    location_code = sehirler[city.lower()]
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

    if context.args[1].lower() == "sahur":
        target_time = times.get("Sahur")
        command = "sahur"
    elif context.args[1].lower() == "iftar":
        target_time = times.get("İftar")
        command = "iftar"
    else:
        update.message.reply_text("Geçersiz komut. Lütfen 'sahur' veya 'iftar' komutlarını kullanın.")
        return

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

def main():
    updater = Updater("6704245576:AAGqYQrMMuH2yt2sHJ9Zhk7q2wtNrDA_Eow", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("sahur", show_prayer_times, pass_args=True))
    dp.add_handler(CommandHandler("iftar", show_prayer_times, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
