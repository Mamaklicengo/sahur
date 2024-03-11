city_ids = {
    'Artvin': 1, 'Aydın': 2, 'Balıkesir': 3, 'Bartın': 4, 'Batman': 5, 'Bayburt': 6,
    'Bilecik': 7, 'Bingöl': 8, 'Bitlis': 9, 'Bolu': 10, 'Burdur': 11, 'Bursa': 12,
    'Çanakkale': 13, 'Çankırı': 14, 'Çorum': 15, 'Denizli': 16, 'Diyarbakır': 17,
    'Düzce': 18, 'Edirne': 19, 'Elazığ': 20, 'Erzincan': 21, 'Erzurum': 22, 'Eskişehir': 23,
    'Gaziantep': 24, 'Giresun': 25, 'Gümüşhane': 26, 'Hakkari': 27, 'Hatay': 28, 'Iğdır': 29,
    'Isparta': 30, 'İstanbul': 31, 'İzmir': 32, 'Kocaeli': 33, 'Kahramanmaraş': 34,
    'Karabük': 35, 'Karaman': 36, 'Kars': 37, 'Kastamonu': 38, 'Kayseri': 39, 'Kırıkkale': 40,
    'Kırklareli': 41, 'Kırşehir': 42, 'Kilis': 43, 'Konya': 44, 'Kütahya': 45, 'Malatya': 46,
    'Manisa': 47, 'Mardin': 48, 'Mersin': 49, 'Muğla': 50, 'Muş': 51, 'Nevşehir': 52,
    'Niğde': 53, 'Ordu': 54, 'Osmaniye': 55, 'Rize': 56, 'Samsun': 57, 'Siirt': 58,
    'Sinop': 59, 'Sivas': 60,'Şanlıurfa': 61, 'Şırnak': 62, 'Tekirdağ': 63, 'Tokat': 64,
    'Trabzon': 65, 'Tunceli': 66,'Uşak': 67,'Van':68,'Yalova':69,'Yozgat':70,'Zonguldak':71,
    'Adana':72,'Sakarya':73,'Adıyaman':74,'Afyonkarahisar' :75,'Ağrı' :76,'Aksaray' :77,
    'Amasya' :78,'Ankara' :79,'Antalya' :80,'Ardahan' :81
}

from pyrogram import Client, filters
import requests

api_url = "https://www.fazilettakvimi.com/api/imsakiye/index/{city_id}"

app = Client("my_bot", api_id=21119132, api_hash="c0a90d0ba66e6bdea356894a55f4856e", bot_token="6531499751:AAGHzxki3QsflZqnh3wnk_1qF-yZE5YJxtw")

def get_prayer_times(city_id):
    response = requests.get(f"{api_url}")
    data = response.json()
    return data

@app.on_message(filters.command(["sahur"]))
def sahur_command(client, message):
    city_name = message.text.split(" ")[1]
    city_id = city_ids.get(city_name)
    if city_id:
        prayer_times = get_prayer_times(city_id)
        sahur_time = prayer_times["Imsak"]
        client.send_message(message.chat.id, f"Sahur vakti {sahur_time}")
    else:
        client.send_message(message.chat.id, "Geçersiz şehir adı")

@app.on_message(filters.command(["iftar"]))
def iftar_command(client, message):
    city_name = message.text.split(" ")[1]
    city_id = city_ids.get(city_name)
    if city_id:
        prayer_times = get_prayer_times(city_id)
        iftar_time = prayer_times["Iftar"]
        client.send_message(message.chat.id, f"Iftar vakti {iftar_time}")
    else:
        client.send_message(message.chat.id, "Geçersiz şehir adı")

     app.run()
