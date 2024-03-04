'''Import telegram module'''
import telebot
import datetime
import requests
import helpers

from telebot import types

city = ""
dates = ""
longitude = ""
latitude = ""

API_TOKEN = "6323367624:AAEIxW6eUbY3PitAeJ2xXB6zZjqBVfMd8Bo"

bot = telebot.TeleBot(API_TOKEN)


'''Greeting block'''
@bot.message_handler(commands=['start'])
def tele_start_func(message):

    first_message = f"Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>!\nI'm WeatherBot"
    bot.send_message(message.chat.id, first_message, parse_mode='html')

    second_message = "Please, input city name to get the weather forecast"
    bot.send_message(message.chat.id, second_message, parse_mode='html')
    
    bot.register_next_step_handler(message, tele_get_city)


'''Get city name block'''
def tele_get_city(message):
    global city
    city = message.text.lstrip().rstrip()
    if helpers.get_city(city) == 0:
        correction_message = "Server is offline. Please try later."
        bot.send_message(message.chat.id, correction_message, parse_mode='html')
    elif helpers.get_city(city) == 1:
        correction_message = "I'm sorry, I don't know that city, or there is a mistake.\nPlease try to type the city name again"
        bot.send_message(message.chat.id, correction_message, parse_mode='html')
        bot.register_next_step_handler(message, tele_get_city_2)
    elif helpers.get_city(city) == 2:
        city = city.capitalize().title()
        tele_get_date(message)

def tele_get_city_2(message):
    global city
    city = message.text.lstrip().rstrip()
    if helpers.get_city(city) == 0:
        correction_message = "Server is offline. Please try later."
        bot.send_message(message.chat.id, correction_message, parse_mode='html')
    elif helpers.get_city(city) == 1:
        correction_message = "I'm sorry, I don't know that city, or there is a mistake.\nPlease try to type the city name again"
        bot.send_message(message.chat.id, correction_message, parse_mode='html')
        bot.register_next_step_handler(message, tele_get_city)
    elif helpers.get_city(city) == 2:
        city = city.capitalize().title()
        tele_get_date(message)



'''Get the date/interval block'''
def tele_get_date(message):
    first_message = "Please, choose the date"
    markup = types.InlineKeyboardMarkup()
    button_today = types.InlineKeyboardButton(text = 'Today', callback_data='today')
    button_tomorrow = types.InlineKeyboardButton(text = 'Tomorrow', callback_data='tomorrow')
    button_week = types.InlineKeyboardButton(text = 'Week', callback_data='week')
    markup.add(button_today, button_tomorrow, button_week)

    bot.send_message(message.chat.id, first_message, parse_mode='html',  reply_markup=markup)
    


@bot.callback_query_handler(func=lambda call:True)
def tele_get_date_func(call):
    global dates
    if call.data == "today":
        dates = [datetime.date.today().isoformat()]
    elif call.data == "tomorrow":
        today = datetime.date.today()
        plus1 = today + datetime.timedelta(days=1)
        dates = [plus1.isoformat()]
    elif call.data == "week":
        today = datetime.date.today()
        plus7 = [today.isoformat()]
        for i in range(1, 7):
            plus7.append((today + datetime.timedelta(days=i)).isoformat())
        dates = plus7
     



@bot.message_handler(commands=['end'])
def output(message):
    global latitude
    global longitude
    latitude = helpers.get_coordinates(city)[0]
    longitude = helpers.get_coordinates(city)[1]

    min_temp_message = f"Min temperature: {helpers.get_weather(dates, latitude, longitude)[0]}°C"
    bot.send_message(message.chat.id, min_temp_message, parse_mode='html')

    max_temp_message = f"Max temperature: {helpers.get_weather(dates, latitude, longitude)[1]}°C"
    bot.send_message(message.chat.id, max_temp_message, parse_mode='html')

    precipitation_message = f"Precipitation: {helpers.get_weather(dates, latitude, longitude)[2]} mm\n"
    bot.send_message(message.chat.id, precipitation_message, parse_mode='html')




# @bot.message_handler(commands=['end'])
# def tele_answer(message):    
#     final_message = f"{city}\n{dates}"
#     bot.send_message(message.chat.id, final_message, parse_mode='html')



bot.polling(none_stop=True, interval=0)