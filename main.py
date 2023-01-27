import telebot
import requests
from datetime import datetime
import pytz
import time

bot = telebot.TeleBot('token here')
dnt1 = '𝔞𝔤𝔤𝔯𝔢𝔰𝔰𝔦𝔳𝔢𝔫𝔢𝔰𝔰 [ℝ𝕋]'
dnt2 = 'Пока что нету'
dnt3 = 'Если хочешь здесь'
dnt4 = 'Оказаться'
dnt5 = 'Задонать'

updates = 'Добавлена команда /stop, Добавлены логи в консоли, обновлен код на GitHub'

#Команда /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    user_id = message.from_user.id
    print('user_id: ' + str(user_id) + '\ncommand start started\n')
    bot.send_message(message.chat.id, 'Привет. Напиши /info')

#Проверка работоспособности команды /time. Также выводит в логи когда запущен скрипт по МСК.
tz_NY = pytz.timezone('Europe/Moscow')
datetime_NY = datetime.now(tz_NY)
print("Moscow time:", datetime_NY.strftime("%H:%M:%S"))
print("Checking of Time is Success!")

#Переменные к команде /weather
temp = ""
temp_min = ""
temp_max = ""
s_city = "Naro-Fominsk,RU"
city_id = 0
appid = "deeedf2ac93b814785e5c147aa7f6b57"
print("Started!")
print("Logs:\n")

#Команда /weather. Самая длинная команда и одна из самых сложных в данном проекте.
@bot.message_handler(commands=["pogoda", "weather", "pagoda"])
def pogoda(message):
    user_id = message.from_user.id
    print('user_id: ' + str(user_id) + '\ncommand pogoda started')
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
    bot.send_message(message.chat.id, 'В Наро-Фоминске: '
                     + '\n' + 'Сейчас: ' + str(conditions)
                     + '\n' + 'Средняя Температура: ' + str(temp)
                     + '\n' + 'Наименьшая температура: ' + str(temp_min)
                     + '\n' + 'Наибольшая температура: ' + str(temp_max)
                     )

#Команда /code
@bot.message_handler(commands=["mycode", "code", "github", "source_code"])
def my_code(message):
    user_id = message.from_user.id
    print('user_id: ' + str(user_id) + '\ncommand my_code started\n')
    bot.send_message(message.chat.id, 'Мой код:' + '\n' + 'https://github.com/VayLorm/Weather-Python-Bot.git')

#Команда /help
@bot.message_handler(commands=["help", "info"])
def help(message):
    user_id = message.from_user.id
    print('user_id: ' + str(user_id) + '\ncommand help started\n')
    bot.send_message(message.chat.id, 'Команды:'
                     + '\n' + '/help , /info - Показывает данное меню'
                     + '\n' + '/pogoda, /weather, /pagoda - Показывает погоду в Наро-Фоминске на текущее время'
                     + '\n' + '/mycode , /code , /github , /source_code - Мой исходный код (обновляется раз в неделю)'
                     + '\n' + '/donate , /donationalerts - Поддержка автора на DonationAlerts!'
                     + '\n' + '/topdonate , /topdonater - Топ поддержавших на DonationAlerts.'
                     + '\n' + '/credits , /author - Версия и Автор'
                     + '\n' + '/time , /msktime - Московское время'
                     )

#Команда /donate
@bot.message_handler(commands=["donate", "subscribe", "donationalerts"])
def donate(message):
    user_id = message.from_user.id
    print('user_id: ' + str(user_id) + '\ncommand donateurl started\n')
    bot.send_message(message.chat.id, "Если хочешь поддержать автора то вот DonationAlerts:" + "\n" + "https://www.donationalerts.com/r/vaylorm")

#Команда /credits
@bot.message_handler(commands=["author", "credits"])
def credits(message):
    user_id = message.from_user.id
    print('user_id: ' + str(user_id) + '\ncommand credits started\n')
    bot.send_message(message.chat.id, "Версия 0.8 (бета)" + "\n" + "Автор - @VayLorm" + "\n" + "Для помощи - /help или /info")

#Команда /time
@bot.message_handler(commands=["msktime", "time"])
def msktime(message):
    user_id = message.from_user.id
    print('user_id: ' + str(user_id) + '\ncommand msktime started')
    Moscow = pytz.timezone('Europe/Moscow')
    datetime_Moscow = datetime.now(Moscow)
    print(datetime_Moscow.strftime("%H:%M:%S"), '\n')
    bot.send_message(message.chat.id, "Время сейчас: " + datetime_Moscow.strftime("%H:%M:%S"))

#Команда /timer
@bot.message_handler(commands=["timer"])
def timer1(message):
    print('timer command started')
    msgv = bot.send_message(message.chat.id, 'Введите Время (в секундах):')
    bot.register_next_step_handler(msgv, timer2)

#Продолжение команды /timer
def timer2(message):
    print('timer2 started')
    try:
        sec = message.text
        sec = int(sec)
        cid = message.chat.id
        msg = bot.send_message(chat_id=cid, text='Осталось:')
        print('user_id: ', cid)
        print('time(sec): ', sec, '\n')
        while True:
            if sec > 0:
                minutes = sec // 60
                if minutes >= 60:
                    cid = message.chat.id
                    h = minutes // 60
                    min1 = minutes - h * 60
                    sec1 = sec - minutes * 60
                    msg_to_send = f'Осталось: {h} часов : {min1} минут : {sec1} секунд'
                    bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text=msg_to_send)
                    time.sleep(2)
                    sec = sec - 2
                else:
                    cid = message.chat.id
                    sec1 = sec - minutes * 60
                    msg_to_send2 = f'Осталось: {minutes} минут : {sec1} секунд'
                    bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text=msg_to_send2)
                    time.sleep(2)
                    sec = sec - 2
            else:
                bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text="Время окончилось!")
                print('time expired')
                break
    except Exception as e:
        msg = bot.send_message(message.chat.id, 'Ошибка: ' + str(e) +
                               '\n' + 'Скорее всего вы просто ввели не число, это так не работает.'
                                      '\n' + '\n' 'Просто введите число и я включу таймер и сам переведу секунды в '
                                             'минуты и '
                                             'минуты в часы если понадобится')
        bot.register_next_step_handler(msg, timer1)

'''
Временный кусок кода. Пока думаю доработать или убрать
Напоминаю - это БЕТА версия
GROUP_ID = -723366333
AUTHOR_ID = 1408266288
@bot.message_handler(func=lambda message: message.chat.id == AUTHOR_ID)
def tell(message):
    bot.send_message(GROUP_ID, message.text)
'''

#Команда /updates
#Для того чтобы работало с вашим id
#Поменяйте переменную author_id на свой id
@bot.message_handler(commands=["updates"])
def update(message):
    user_id = message.from_user.id
    author_id = 1408266288
    print(message.chat.id, user_id, '\n')
    if user_id == author_id:
        bot.send_message(message.chat.id, 'Текущее обновление:\n' + updates)
    else:
        bot.send_message(message.chat.id, "Только @VayLorm может вызывать данную команду!")

#Команда /topdonate
@bot.message_handler(commands=["topdonate" , "topdonater"])
def topdonater(message):
    bot.send_message(message.chat.id, "Топ донатеров: "
                     + '\n' + '1: ' + dnt1
                     + '\n' + '2: ' + dnt2
                     + '\n' + '3: ' + dnt3
                     + '\n' + '4: ' + dnt4
                     + '\n' + '5: ' + dnt5
                     )

#Команда /stop
@bot.message_handler(commands=["stop" , "kill"])
def stop(message):
    user_id = message.from_user.id
    author_id = 1408266288
    print(message.chat.id, user_id, '\n')
    print('stop command started')
    if user_id == author_id:
        bot.send_message(message.chat.id, 'Выключение...')
        bot.stop_bot()
    else:
        bot.send_message(message.chat.id, "Только @VayLorm может вызывать данную команду!")


# Запускаем бота
bot.polling(none_stop=True, interval=0)
