import requests
import telebot
import config
from config import weather_key
from telebot import types

bot = telebot.TeleBot(config.token)

# start command
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.last_name == None:
        text_message = f'Hey, {message.from_user.first_name}! I can tell you the weather for today! You just need to ask me about it and name your city. But I only know large cities, and if you live in a small city, then just enter the closest big city to you. If you want to know more about my commands enter /help.'
    elif message.from_user.first_name == None:
        text_message = f'Hey, {message.from_user.last_name}! I can tell you the weather for today! You just need to ask me about it and name your city. But I only know large cities, and if you live in a small city, then just enter the closest big city to you. If you want to know more about my commands enter /help.'
    else:
        text_message = f'Hey, {message.from_user.first_name} {message.from_user.last_name}! I can tell you the weather for today! You just need to ask me about it and name your city. But I only know large cities, and if you live in a small city, then just enter the closest big city to you. If you want to know more about my commands enter /help.'

    bot.send_message(message.chat.id, text_message, parse_mode="html")

# get weather
@bot.message_handler(commands=['weather'])
def city(message):
    sent = bot.send_message(message.chat.id, "Enter the name of the city")
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

        weather_data = f'🌇Weather in {city_name}\n\n             {main} {temp}℃\n\n❄️Min Temp: {min_temp}℃\n🔥Max Temp: {max_temp}℃\n🌂Feels Like: {feels_like}℃\n💨Wind Speed: {wind_speed} m/s\n⏲Pressure: {pressure}\n💦Humidity: {humidity}'

        bot.send_message(message.chat.id, weather_data, parse_mode="html")
    except Exception as ex:
        bot.send_message(message.chat.id, "😔I do not know this city", parse_mode="html")

@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather_btn = types.KeyboardButton("/weather")
    start_btn = types.KeyboardButton("/start")
    help_btn = types.KeyboardButton("/help")

    markup.add(weather_btn, start_btn, help_btn)

    help_text = "Here are all my commands:\n/start - start me\n/help - all comands\n/weather - show weather by city name"
    bot.send_message(message.chat.id, help_text, reply_markup=markup)

bot.polling(none_stop=True)