import telebot
import requests

bot = telebot.TeleBot('12345678:AAH-aAaAaaaAaaAaaaAaa')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши /pogoda')


# Получаем погоду
temp = ""
temp_min = ""
temp_max = ""
s_city = "Naro-Fominsk,RU"
city_id = 0
appid = "deeedf2ac93b814785e5c147aa7f6b57"
try:
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = res.json()
    cities = ["{} ({})".format(d['name'], d['sys']['country'])
              for d in data['list']]
    print("city:", cities)
    city_id = data['list'][0]['id']
    print('city_id=', city_id)
except Exception as e:
    print("Exception (find):", e)
    pass
try:
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    print("conditions:", data['weather'][0]['description'])
    print("temp:", data['main']['temp'])
    print("temp_min:", data['main']['temp_min'])
    print("temp_max:", data['main']['temp_max'])
except Exception as e:
    print("Exception (weather):", e)
    pass

temp = data['main']['temp']
temp_min = data['main']['temp_min']
temp_max = data['main']['temp_max']
conditions = data['weather'][0]['description']


# ключ погоды = deeedf2ac93b814785e5c147aa7f6b57
# Получение сообщений от юзера
@bot.message_handler(commands=["pogoda"])
def handle_text(message):
    bot.send_message(message.chat.id, 'В Наро-Фоминске: '
                     + '\n' + 'Сейчас: ' + str(conditions)
                     + '\n' + 'Средняя Температура: ' + str(temp)
                     + '\n' + 'Наименьшая температура: ' + str(temp_min)
                     + '\n' + 'Наибольшая температура: ' + str(temp_max)
                     )


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Напиши /pogoda')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
