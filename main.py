import telebot
import requests


bot = telebot.TeleBot('7649262765:AAH4I7gvhFrutc8YaOlj1jay09XNGTobGy8')

name = ''

@bot.message_handler(content_types=['text'])
def start(message):
    # bot.reply('Привет, {0}! Я бот, который может определить погоду в различных городах, хочешь начать нашу работу?'.format(message.from_user.first_name))
    bot.send_message(message.from_user.id, 'Привет! Погода какого города вам интересна?')
    bot.register_next_step_handler(message, info_weather)

def info_weather(message):
    global name
    name = message.text
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid=4f536a32d323f6d385e6750d21e9c2ec&lang=ru').json()

        try:
            description = response['weather'][0]['description']
            temp = response['main']['temp']
            feels_like = response['main']['feels_like']
            bot.send_message(message.from_user.id, f'Погода в {name} {temp}, ощущается как {feels_like}, при этом на улице {description}!')
        except Exception as e:
            print('Ошибка, при некорректном городе ' + str(e))
            bot.send_message(message.from_user.id, 'Некорректный город! Попробуйте заново!')

    except Exception as e:
        print('Ошибка при исключении сервера ' + str(e))
        bot.send_message(message.from_user.id, 'Сервис недоступен, попробуйте позже...')

bot.polling(none_stop=True, interval=0)