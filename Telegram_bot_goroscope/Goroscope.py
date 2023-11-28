import telebot
import requests
from zodiac import zodiac_dates
from bs4 import BeautifulSoup

bot = telebot.TeleBot('5935478269:AAGBcry4uYLJCnYtLeLwUg3sWg_7iISSrK0')

@bot.message_handler()
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Добро пожаловать в бота!\nПривет! Я бот, который поможет тебе узнать гороскоп.\nДля начала,  напиши свое имя.')
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text
    bot.send_message(message.chat.id,
                     "Хорошо! Теперь введи свою дату рождения в формате ДД.ММ.ГГГГ (например, 01.01.2000).")
    bot.register_next_step_handler(message, get_birthdate)

def determine_zodiac_sign(day, month):
    global zodiac
    for (start_month, start_day), zodiac_sign in zodiac_dates.items():
        if (month == start_month and day >= start_day) or (month == start_month+1 and day <= start_day):
                zodiac = zodiac_sign


def get_birthdate(message):
    birthdate = message.text

    try:
        day, month, year = map(int, birthdate.split('.'))
        birthdate = f"{year}-{month}-{day}"
        determine_zodiac_sign(day, month)




        response = requests.get(f'https://horo.mail.ru/prediction/{zodiac}/today/')

        soup = BeautifulSoup(response.content, 'html.parser')

        elements = soup.find_all(class_='article__item article__item_alignment_left article__item_html')
        for element in elements:
            print(element.get_text())
            bot.send_message(message.chat.id, f"Твой знак зодиака: {zodiac} \n Вот твой гороскоп: {element.get_text()}")

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка. Попробуй ещё раз.")
        bot.register_next_step_handler(message, get_birthdate)


bot.polling()