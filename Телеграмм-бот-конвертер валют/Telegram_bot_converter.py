import telebot
import mysql.connector as mysql
import datetime
import requests


bot = telebot.TeleBot('5935478269:AAGBcry4uYLJCnYtLeLwUg3sWg_7iISSrK0')

try:
    connection = mysql.connect(
        host='localhost',
        user='root',
        password='1234567Ab',
        database='mysql',
    )

    cursor = connection.cursor(buffered=True)

    cursor.execute('CREATE TABLE IF NOT EXISTS black_list('
                   'id int PRIMARY KEY NOT NULL AUTO_INCREMENT,'
                   'chat_id varchar(255))')

    cursor.execute('CREATE TABLE IF NOT EXISTS USERS15('
                   'id int PRIMARY KEY NOT NULL AUTO_INCREMENT,'
                   'chat_id varchar(255),'
                   'name varchar(255),'
                   'username varchar(255),'
                   'start_date varchar(255))')

    cursor.execute('CREATE TABLE IF NOT EXISTS cur_pair('
                   'id int PRIMARY KEY NOT NULL AUTO_INCREMENT,'
                   'cur1 varchar(255),'
                   'cur2 varchar(255))')
    connection.commit()
except Exception as e:
    print(e)

password = '123'
cur1 = ""
cur2 = ""

def get_password(message):
    if password == message.text:

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

        keyboard.add(telebot.types.InlineKeyboardButton('Информация о пользователях', callback_data='user_info'))

        keyboard.add(telebot.types.InlineKeyboardButton('Сделать рассылку', callback_data='send_message'))
        keyboard.add(telebot.types.InlineKeyboardButton('Сделать валютную пару', callback_data='add_pair'))

        bot.send_message(message.chat.id, 'Добро пожаловать в админку', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Пароль неверный. Попробуйте еще раз нажать команду /admin')


def all_users(message):
    cursor.execute('select chat_id from USERS15')
    chats = cursor.fetchall()
    for i in chats:
        bot.send_message(i[0], message.text)

def check_cur(message):
    if len(message.text) == 3:
        resp = requests.get(f'https://api.nbrb.by/exrates/rates/{message.text}?parammode=2')
        if resp == 200:
            return True
    return False

def get_cur(message):
    global cur1
    if check_cur(message):
        cur1 = message.text
        msg = bot.send_message(message.chat.id, 'Введите вторую валюту')
        bot.register_next_step_handler(msg, get_cur)
    else:
        msg = bot.send_message(message.chat.id, 'Валюта неверная, попробуйте заново')
        bot.register_next_step_handler(msg, get_cur)

def get_cur1(message):
    global cur2, cur1
    try:
        if check_cur(message):
            cur2 = message.text
            bot.send_message(message.chat.id, '')
            cursor.execute(f"""INSERT INTO cur_pair (cur1, cur2)
                                        values ('{cur1}', '{cur2}')""")
            connection.commit()
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Попробуйте еще раз')
    else:
        msg = bot.send_message(message.chat.id, 'Валюта неверная, попробуйте заново')
        bot.register_next_step_handler(msg, get_cur1)




@bot.message_handler()
def start(message):
    cursor.execute(f"""select * from black_list where chat_id = {message.chat.id}""")
    if message.text == '/start' and len(cursor.fetchall()) == 0:
        cursor.execute(f"""select * from USERS15 where chat_id = '{message.chat.id}'""")
        u = cursor.fetchall()
        if len(u) == 0:
            try:
                cursor.execute(f"""INSERT INTO USERS15 (chat_id, name, username, start_date) 
        values ('{message.chat.id}', '{message.from_user.first_name}', '{message.from_user.username}',
        '{datetime.datetime.now()}')""")
                connection.commit()
                bot.send_message(message.chat.id, 'Добро пожаловать в бота')
            except Exception as e:
                print(e)
                bot.send_message(message.chat.id, 'Произошла ошибка. Попробуйте позже')

    if message.text == '/admin':
        msg = bot.send_message(message.chat.id, 'Введите пароль для админки')

        bot.register_next_step_handler(msg, get_password)


@bot.callback_query_handler(func= lambda call: True)
def handle(callback):
    cursor.execute(f"""select * from USERS15 where chat_id = '{callback.message.chat.id}'""")
    u = cursor.fetchall()
    if len(u) > 0:
        if callback.data == 'user_info':
            cursor.execute('select * from USERS15')
            u = cursor.fetchall()

            for i in u:
                keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(telebot.types.InlineKeyboardButton
                             ('Удалить пользователя', callback_data=f'delete_{i[1]}'))
                keyboard.add(telebot.types.InlineKeyboardButton
                             ('Заблокировать пользователя', callback_data=f'block_{i[1]}'))
                bot.send_message(callback.message.chat.id, f'Имя: {i[2]}\nЮзернейм: {i[3]}\n'
                                                           f'Телеграмм айди: {i[1]}\n{i[4].split(" ")[0]} {i[4].split(" ")[1][0:5]}',
                                 reply_markup=keyboard)
        elif callback.data == 'add_pair':
            msg = bot.send_message(callback.message.chat.id, f"Введите валюту из которой будем конвертировать")
            bot.register_next_step_handler(msg, get_cur)

        elif callback.data.startswith('delete'):
            try:
                cursor.execute(f"""DELETE FROM USERS15 where chat_id = '{callback.data.split('_')[1]}'""")
                bot.delete_message(callback.message.chat.id, callback.message.id)
            except Exception:
                bot.send_message(callback.message.chat.id, 'Произошла ошибка')
        elif callback.data.startswith('block'):
            try:
                cursor.execute(f"""DELETE FROM USERS15 where chat_id = '{callback.data.split('_')[1]}'""")
                bot.delete_message(callback.message.chat.id, callback.message.id)
                cursor.execute(f"""insert into black_list (chat_id) values ('{callback.data.split('_')[1]}')""")
            except Exception:
                bot.send_message(callback.message.chat.id, 'Произошла ошибка')
        elif callback.data == 'send_message':
            msg = bot.send_message(callback.message.chat.id, 'Отправьте сообщение, которое увидят все пользователи!')
            bot.register_next_step_handler(msg, all_users)


bot.polling()