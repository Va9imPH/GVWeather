import requests
import telebot
import config # the file config.py is not publicly available
from config import weather_key
from telebot import types

bot = telebot.TeleBot(config.token)

# start command
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.last_name == None:
        text_message = f'Привет, {message.from_user.first_name}! Я могу сказать вам погоду на сегодня! Вам просто нужно спросить меня об этом и назвать свой город. Но я знаю только большие города, а если ты живешь в маленьком городе, то просто введи ближайший к тебе большой город. Если вы хотите узнать больше о моих командах, введите /help.'
    elif message.from_user.first_name == None:
        text_message = f'Привет, {message.from_user.last_name} !Я могу сказать вам погоду на сегодня! Вам просто нужно спросить меня об этом и назвать свой город. Но я знаю только большие города, а если ты живешь в маленьком городе, то просто введи ближайший к тебе большой город. Если вы хотите узнать больше о моих командах, введите /help.'
    else:
        text_message = f'Привет, {message.from_user.first_name} Я могу сказать вам погоду на сегодня! Вам просто нужно спросить меня об этом и назвать свой город. Но я знаю только большие города, а если ты живешь в маленьком городе, то просто введи ближайший к тебе большой город. Если вы хотите узнать больше о моих командах, введите /help.'

    bot.send_message(message.chat.id, text_message, parse_mode="html")

# get weather
@bot.message_handler(commands=['weather'])
def city(message):
    sent = bot.send_message(message.chat.id, "Введите название города(на английском)")
    bot.register_next_step_handler(sent, weather)

def weather(message):
    # get weather data
    try:
        city = message.text
        
        response = requests.get(
            url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}&units=metric"
        ).json()

        city_name = response['name']
        main = response['weather'][0]['main']
        temp = int(response['main']['temp']) // 1
        min_temp = int(response['main']['temp_min']) // 1
        max_temp = int(response['main']['temp_max']) // 1
        feels_like = int(response['main']['feels_like']) // 1
        pressure = response['main']['pressure']
        humidity = response['main']['humidity']
        wind_speed = response['wind']['speed']

        weather_data = f'🌇Погода в {city_name}\n\n             {main} {temp}℃\n\n❄️Мин. Температура: {min_temp}℃\n🔥Макс. Температура: {max_temp}℃\n🌂Ощущается как: {feels_like}℃\n💨Скорость Ветра: {wind_speed} m/s\n⏲Давление: {pressure}\n💦Влажность: {humidity}'

        bot.send_message(message.chat.id, weather_data, parse_mode="html")
    except Exception as ex:
        bot.send_message(message.chat.id, "😔Я не знаю такого города", parse_mode="html")

@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather_btn = types.KeyboardButton("/weather")
    start_btn = types.KeyboardButton("/start")
    help_btn = types.KeyboardButton("/help")

    markup.add(weather_btn, start_btn, help_btn)

    help_text = "Вот все мои команды:\n/start - запустить меня\n/help - все команды\n/weather - показать погоду по названию города"
    bot.send_message(message.chat.id, help_text, reply_markup=markup)

bot.polling(none_stop=True)
