from datetime import datetime
import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient, events
import requests
import datetime, pytz

api_id = '21119132'
api_hash = 'c0a90d0ba66e6bdea356894a55f4856e'
bot_token = '6531499751:AAGHzxki3QsflZqnh3wnk_1qF-yZE5YJxtw'

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
trSehirler = [
    'ADANA', 'ADIYAMAN', 'AFYONKARAHİSAR', 'AĞRI', 'AMASYA', 'ANKARA', 'ANTALYA', 'ARTVİN', 'AYDIN', 'BALIKESİR',
    'BİLECİK', 'BİNGÖL', 'BİTLİS', 'BOLU', 'BURDUR', 'BURSA', 'ÇANAKKALE', 'ÇANKIRI', 'ÇORUM', 'DENİZLİ',
    'DİYARBAKIR', 'EDİRNE', 'ELAZIĞ', 'ERZİNCAN', 'ERZURUM', 'ESKİŞEHIR', 'GAZİANTEP', 'GİRESUN', 'GÜMÜŞHANE',
    'HAKKARİ', 'HATAY', 'ISPARTA', 'MERSİN', 'İSTANBUL', 'İZMİR', 'KARS', 'KASTAMONU', 'KAYSERİ', 'KIRKLARELİ',
    'KIRŞEHİR', 'KOCAELİ', 'KONYA', 'KÜTAHYA', 'MALATYA', 'MANİSA', 'KAHRAMANMARAŞ', 'MARDİN', 'MUĞLA', 'MUŞ',
    'NEVŞEHİR', 'NİĞDE', 'ORDU', 'RİZE', 'SAKARYA', 'SAMSUN', 'SİİRT', 'SİNOP', 'SİVAS', 'TEKİRDAĞ', 'TOKAT',
    'TRABZON', 'TUNCELİ', 'ŞANLIURFA', 'UŞAK', 'VAN', 'YOZGAT', 'ZONGULDAK', 'AKSARAY', 'BAYBURT', 'KARAMAN',
    'KIRIKKALE', 'BATMAN', 'ŞIRNAK', 'BARTIN', 'ARDAHAN', 'IĞDIR', 'YALOVA', 'KARABÜK', 'KİLİS', 'OSMANİYE', 'DÜZCE'
]

faziletSozluk = {
    'Artvin': 1, 'Aydın': 2, 'Balıkesir': 3, 'Bartın': 4, 'Batman': 5, 'Bayburt': 6, 'Bilecik': 7, 'Bingöl': 8,
    'Bitlis': 9, 'Bolu': 10, 'Burdur': 11, 'Bursa': 12, 'Çanakkale': 13, 'Çankırı': 14, 'Çorum': 15, 'Denizli': 16,
    'Diyarbakır': 17, 'Düzce': 18, 'Edirne': 19, 'Elazığ': 20, 'Erzincan': 21, 'Erzurum': 22, 'Eskişehir': 23,
    'Gaziantep': 24, 'Giresun': 25, 'Gümüşhane': 26, 'Hakkari': 27, 'Hatay': 28, 'Iğdır': 29, 'Isparta': 30,
    'İstanbul': 31, 'İzmir': 32, 'Kocaeli': 33, 'Kahramanmaraş': 34, 'Karabük': 35, 'Karaman': 36, 'Kars': 37,
    'Kastamonu': 38, 'Kayseri': 39, 'Kırıkkale': 40, 'Kırklareli': 41, 'Kırşehir': 42, 'Kilis': 43, 'Konya': 44,
    'Kütahya': 45, 'Malatya': 46, 'Manisa': 47, 'Mardin': 48, 'Mersin': 49, 'Muğla': 50, 'Muş': 51, 'Nevşehir': 52,
    'Niğde': 53, 'Ordu': 54, 'Osmaniye': 55, 'Rize': 56, 'Samsun': 57, 'Siirt': 58, 'Sinop': 59, 'Sivas': 60,
    'Şanlıurfa': 61, 'Şırnak': 62, 'Tekirdağ': 63, 'Tokat': 64, 'Trabzon': 65, 'Tunceli': 66, 'Uşak': 67, 'Van': 68,
    'Yalova': 69, 'Yozgat': 70, 'Zonguldak': 71, 'Adana': 72, 'Sakarya': 73, 'Adıyaman': 74, 'Afyon': 75, 'Ağrı': 76,
    'Aksaray': 77, 'Amasya': 78, 'Ankara': 79, 'Antalya': 80, 'Ardahan': 81
}
def faziletAksam(il):
    ilNo = faziletSozluk[il]

    a = requests.get(f"https://www.fazilettakvimi.com/api/imsakiye/index/{ilNo}")
    b = a.json()

    ramazan = b['ramazanin_kaci'] - 1

    return f"{b['vakitler'][ramazan]['miladi_tarih']}|{b['vakitler'][ramazan]['aksam']}"

def faziletSabah(il):
    ilNo = faziletSozluk[il]

    a = requests.get(f"https://www.fazilettakvimi.com/api/imsakiye/index/{ilNo}")
    b = a.json()

    ramazan = b['ramazanin_kaci'] - 1

    return f"{b['vakitler'][ramazan]['miladi_tarih']}|{b['vakitler'][ramazan]['imsak']}"

turkiyeSaati = datetime.datetime.now(pytz.timezone("Turkey")).strftime("%H:%M")

def vakitHesabi(vakit, hangiZaman, simdikiZaman=turkiyeSaati):
    
    "Zaman bilgisinin saat ve dakikalarını ayıralım"
    hangiZamanSaat, hangiZamanDK = hangiZaman.split(':')
    simdikiZamanSaat, simdikiZamanzamanDK = simdikiZaman.split(':')

    "Tüm zamanı dakikaya çevirelim"
    hangiAyrim = int(hangiZamanSaat)*60 + int(hangiZamanDK)
    simdikiZamanAyrim = int(simdikiZamanSaat)*60 + int(simdikiZamanzamanDK)

    dakikaFarki = hangiAyrim - simdikiZamanAyrim

    tamSaat = dakikaFarki // 60                 # Küsüratı almamak için "//" | `4.58` için yalnız 4 lazım
    tamDakika = dakikaFarki - (tamSaat * 60)

    if tamSaat < 0:
        tamSaat += 24
    elif tamDakika < 0:
        tamDakika += 60

    if tamSaat and tamDakika > 0:
        return f"**{vakit}**'a Kalan Süre;\n\n\t**{tamSaat}** Saat **{tamDakika}** dakika.."
    elif tamDakika > 0:
        return f"**{vakit}**'a Kalan Süre;\n\n\t**{tamDakika}** dakika.."
    elif tamDakika == 0 and not tamSaat == 0:
        return f"**{vakit}**'a Kalan Süre;\n\n\t**{tamSaat}** Saat.."
    elif tamSaat == 0:
        return f"**{vakit}** Geldi :)\n\n\t__Hayırlı {vakit}'lar..__"

sahuraKalan = lambda il : vakitHesabi('Sahur', faziletSabah(il).split('|')[1], turkiyeSaati)
iftaraKalan = lambda il : vakitHesabi('İftar', faziletAksam(il).split('|')[1], turkiyeSaati)

#print(sahuraKalan('Niğde'))
#print(iftaraKalan('Niğde'))
@client.on_message(Filters.command(['iftar'],['!','.','/']))
def iftar(client, message):
    cevaplanan_mesaj = message.reply_to_message
    if cevaplanan_mesaj is None:
        kekik = message.reply("Bekleyin..")
    else:
        kekik = message.reply("Bekleyin..", reply_to_message_id=cevaplanan_mesaj.message_id)

    girilen_yazi = message.text
    if len(girilen_yazi.split()) == 1:
        kekik.edit("Arama yapabilmek için `il` girmelisiniz")
        return

    il = " ".join(girilen_yazi.split()[1:2]).lower().capitalize().replace('I', 'İ')
    mesaj = f'**{il}** __ili için__ '

    try:
        mesaj += iftaraKalan(il)
    except:
        kekik.edit('Bulunamadı..')
        return

    try:
        kekik.edit(mesaj, disable_web_page_preview=True, parse_mode="Markdown")
    except Exception as hata_mesaji:
        kekik.edit(hata_mesaji)

@client.on_message(Filters.command(['sahur'],['!','.','/']))
def sahur(client, message):
    cevaplanan_mesaj = message.reply_to_message
    if cevaplanan_mesaj is None:
        kekik = message.reply("Bekleyin..")
    else:
        kekik = message.reply("Bekleyin..", reply_to_message_id=cevaplanan_mesaj.message_id)

    girilen_yazi = message.text
    if len(girilen_yazi.split()) == 1:
        kekik.edit("Arama yapabilmek için `il` girmelisiniz")
        return

    il = " ".join(girilen_yazi.split()[1:2]).lower().capitalize().replace('I', 'İ')
    mesaj = f'**{il}** __ili için__ '

    try:
        mesaj += sahuraKalan(il)
    except:
        kekik.edit('Bulunamadı..')
        return

    try:
        kekik.edit(mesaj, disable_web_page_preview=True, parse_mode="Markdown")
    except Exception as hata_mesaji:
        kekik.edit(hata_mesaji)
        client.run()
