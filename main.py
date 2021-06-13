from telebot import TeleBot,types
import config
import base
import test
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="https://developers.google.com/maps/")
bot = TeleBot(config.token)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row(types.KeyboardButton('🏠Kvartira Izlash'),types.KeyboardButton('🧳Ijarachi Izlash'))
markup.row(types.KeyboardButton('📋Kvartira Kerak'),types.KeyboardButton('📄Ijarachi Kerak'))
markup.row(types.KeyboardButton('👨‍💻Admin bilan bog`lanish'),types.KeyboardButton('🤖Haqida'))
keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
reg_button = types.KeyboardButton(text="📱Telefon Raqamini Ulashish", request_contact=True,)
keyboard.add(reg_button)
otiotmadi = ''
ism = ''
tel = ''
answer = ''
izoh = ''
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    global tel
    tel=message.contact.phone_number
    base.addusers(message.from_user.id, ism, message.from_user.username, tel)
    bot.send_message(message.from_user.id, "<b>Rahmat ma'lumotlaringiz qo`shildi.\n\n                   👉 /start 👈     </b>",parse_mode='html')

@bot.message_handler(commands=['start'])
def start(message):
    global otiotmadi
    if base.search_user(message.from_user.id):
        tel = base.search_user(message.from_user.id)[0][3]
        ism = base.search_user(message.from_user.id)[0][0]
        bot.send_message(message.from_user.id,"Tanlang",reply_markup=markup)
    else:
        bot.send_message(message.from_user.id,"<b>Ismingizni to`liq yuboring.</b>", parse_mode='html')
        otiotmadi="ism soraldi"
@bot.message_handler(content_types=['text'])
def text(message):
    global otiotmadi
    global ism
    global tel
    global answer
    global izoh
    if otiotmadi=="ism soraldi" and not base.search_user(message.from_user.id):
        ism = message.text
        bot.send_message(message.chat.id,
                         "<i><b>Iltimos Telefon Raqamingizni ulashing👇🏻</b></i>",parse_mode='html',
                         reply_markup=keyboard)
        otiotmadi="tel soraldi"
    elif message.text in ['🏠Kvartira Izlash','🧳Ijarachi Izlash','📋Kvartira Kerak','📄Ijarachi Kerak']:
        if message.text == '📄Ijarachi Kerak':
            bot.send_message(message.from_user.id, "Kvartira haqida izoh yuboring...(comment kalit so`zi bilan)")
        elif message.text == '🏠Kvartira Izlash':
            bot.send_message(message.from_user.id, "lokatsiyangizni yuboring...")
        elif message.text == '📋Kvartira Kerak':
            bot.send_message(message.from_user.id, "Izohni yuboring...(comment kalit so`zi bilan)")
        elif message.text == '🧳Ijarachi Izlash':
            bot.send_message(message.from_user.id, "Kvartirangiz lokatsiyasini yuboring...")
        answer = message.text
    elif message.text == '👨‍💻Admin bilan bog`lanish':
        bot.send_message(message.from_user.id, "*Admin:* [Diyorbek Ismoilov](https://t.me/DiyorbekIsmoilovbot)", parse_mode='Markdown')
    elif message.text == '🤖Haqida':
        bot.send_message(message.from_user.id, f"*Ushbu* [{bot.get_me().first_name}](https://t.me/{bot.get_me().username}) *sizga ijaraga uy topishingizda yordam beradi ,\nIjarachi topishda ham.*",parse_mode='Markdown')
    elif message.text[:7]=="comment":
        bot.send_message(message.from_user.id, "Lokatsiyani yuboring: ")
        izoh = message.text[7:]
    else:
        print("tugadi....///")
    izoh = str(izoh).replace("'", "ʻ")
@bot.message_handler(content_types=['location'])
def location(message):
    if answer == '📄Ijarachi Kerak':
        tel = base.search_user(message.from_user.id)[0][3]
        ism = base.search_user(message.from_user.id)[0][0]
        base.add("places",ism,message.from_user.id,message.from_user.username,tel,message.location.latitude,message.location.longitude,f"{izoh}")
        bot.send_message(message.from_user.id, "Rahmat ma`lumotlaringiz qo`shildi...")
    elif answer == '📋Kvartira Kerak':
        tel = base.search_user(message.from_user.id)[0][3]
        ism = base.search_user(message.from_user.id)[0][0]
        base.add("search_place",ism,message.from_user.id,message.from_user.username,tel,message.location.latitude,message.location.longitude,f"{izoh}")
        bot.send_message(message.from_user.id, "Rahmat ma`lumotlaringiz qo`shildi...")
    elif answer == '🏠Kvartira Izlash':
        for i in test.taqqos(message.location.latitude,message.location.longitude,base.search("places")):
            bot.send_location(message.from_user.id, i[1][1][0],i[1][1][1])
            locationc = geolocator.reverse(f"{i[1][1][0]},{i[1][1][1]}")
            info = base.search_place_info('places',i[1][1][0], i[1][1][1])
            bot.send_message(message.from_user.id,f"<b>Manzil: {locationc}</b>\n\nOraliq masofa {i[0]} kilometr\nIzoh: {base.search_place_info('places',i[1][1][0],i[1][1][1])[0][6]}\nIsm: {info[0][0]}\nUsername: {info[0][2]}\nTel: {info[0][3]}\n@{bot.get_me().username}",parse_mode='html')
    elif answer == '🧳Ijarachi Izlash':
        for i in test.taqqos(message.location.latitude,message.location.longitude,base.search("search_place")):
            bot.send_location(message.from_user.id, i[1][1][0],i[1][1][1])
            locationc = geolocator.reverse(f"{i[1][1][0]},{i[1][1][1]}")
            info = base.search_place_info('search_place',i[1][1][0], i[1][1][1])
            bot.send_message(message.from_user.id,f"<b>Manzil: {locationc}</b>\n\nOraliq masofa {i[0]} kilometr\nIzoh: {base.search_place_info('search_place', i[1][1][0], i[1][1][1])[0][6]}\nIsm: {info[0][0]}\nUsername: {info[0][2]}\nTel: {info[0][3]}\n@{bot.get_me().username}",parse_mode='html')
print('running')
bot.polling()
