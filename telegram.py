'''Import telegram module'''
import telebot
import datetime
import helpers

from telebot import types


database = {}

API_TOKEN = "6323367624:AAEIxW6eUbY3PitAeJ2xXB6zZjqBVfMd8Bo"

bot = telebot.TeleBot(API_TOKEN)


'''Greeting block'''
@bot.message_handler(commands=['start'])
def tele_start_func(message):
    first_message = f"Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>!\n\nI'm WeatherBot\n\n\
Please, input city name to get the weather forecast"
    with open('images/start.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=first_message, parse_mode='html')
    bot.register_next_step_handler_by_chat_id(message.chat.id, tele_get_city)


'''Get city name block'''
def tele_get_city(message):
    city = message.text.lstrip().rstrip()
    if helpers.get_city(city) == 0:
        correction_message = "Server is offline. Please try later."
        bot.send_message(message.chat.id, correction_message, parse_mode='html')
    elif helpers.get_city(city) == 1:
        correction_message = "I'm sorry, I don't know that city, or there is a mistake.\nPlease try to type the city name again"
        bot.send_message(message.chat.id, correction_message, parse_mode='html')
        bot.register_next_step_handler_by_chat_id(message.chat.id, tele_get_city_2)
    elif helpers.get_city(city) == 2:
        city = city.capitalize().title()
        tele_get_date(message)
        database.update({message.chat.id: {'city': city}})

def tele_get_city_2(message):
    city = message.text.lstrip().rstrip()
    if helpers.get_city(city) == 0:
        correction_message = "Server is offline. Please try later."
        bot.send_message(message.chat.id, correction_message, parse_mode='html')
    elif helpers.get_city(city) == 1:
        correction_message = "I'm sorry, I don't know that city, or there is a mistake.\nPlease try to type the city name again"
        bot.send_message(message.chat.id, correction_message, parse_mode='html')
        bot.register_next_step_handler_by_chat_id(message.chat.id, tele_get_city)
    elif helpers.get_city(city) == 2:
        city = city.capitalize().title()
        tele_get_date(message)
        database.update({message.chat.id: {'city': city}})


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
    if call.data == "today":
        dates = [datetime.date.today().isoformat()]
        database[call.message.chat.id]['dates'] = dates
        output(call.message)
    elif call.data == "tomorrow":
        today = datetime.date.today()
        plus1 = today + datetime.timedelta(days=1)
        dates = [plus1.isoformat()]
        database[call.message.chat.id]['dates'] = dates
        output(call.message)
    elif call.data == "week":
        today = datetime.date.today()
        plus7 = [today.isoformat()]
        for i in range(1, 7):
            plus7.append((today + datetime.timedelta(days=i)).isoformat())
        dates = plus7
        database[call.message.chat.id]['dates'] = dates
        output(call.message)


'''Manage info with outout form'''
def output(message):
    latitude = helpers.get_coordinates(database[message.chat.id]['city'])[0]
    longitude = helpers.get_coordinates(database[message.chat.id]['city'])[1]
    database[message.chat.id]['latitude'] = latitude
    database[message.chat.id]['longitude'] = longitude

    if len(database[message.chat.id]['dates']) == 7:
        output_message = ""
        for i in database[message.chat.id]['dates']:
            output_message = output_message + f"{i}\nTemperature: {round((helpers.get_weather(i, database[message.chat.id]['latitude'], database[message.chat.id]['longitude'])[0] + helpers.get_weather(i, database[message.chat.id]['latitude'], database[message.chat.id]['longitude'])[1] / 2), 1)}°C\n\n"
        output_message = f"<b>{database[message.chat.id]['city']}</b>\n\n" + output_message
    else:
        output_message = f"<b>{database[message.chat.id]['city']}</b>\n\n\
{database[message.chat.id]['dates'][0]}\n\n\
Min temperature: {helpers.get_weather(database[message.chat.id]['dates'], database[message.chat.id]['latitude'], database[message.chat.id]['longitude'])[0]}°C\n\
Max temperature: {helpers.get_weather(database[message.chat.id]['dates'], database[message.chat.id]['latitude'], database[message.chat.id]['longitude'])[1]}°C\n\
Precipitation: {helpers.get_weather(database[message.chat.id]['dates'], database[message.chat.id]['latitude'], database[message.chat.id]['longitude'])[2]} mm"

    bot.send_message(message.chat.id, output_message, parse_mode='html')

bot.polling(none_stop=True, interval=0)