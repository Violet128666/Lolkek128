from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon import functions
import re
import asyncio
import sqlite3
import sys
import telebot
import os
import json
from datetime import datetime
import time
import requests
import subprocess
import random
from telebot import apihelper
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from telebot import types
import random
import os
import json


accounts = [
    
    {
        'api_id': '21333763',
        'api_hash': '70f581935d27a46f7d36ea0fb9e77ea1',
        'phone': '79232691811',
        'session_name': 'session_name_1121'},
{	'api_id': '27164998',
        'api_hash': 		'f557bd347d28b0892e9f504f7b392a7b',
        'phone': '79894845564',
        'session_name': 'session_name_1'
    }
    

]

allowed_users_file = 'allowed_users.json'
allowed_users = []
admin_ids = [6407049511]  # Список ID администраторов
admin_id = 6407049511
user_ids_file = 'user_ids.json'

#айди админов добавлять в обе переменные!


def init_db():
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            timestamp TEXT,
            target_username TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления записи в логи
def add_log(username, target_username):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO logs (username, timestamp, target_username) VALUES (?, ?, ?)
    ''', (username, timestamp, target_username))
    conn.commit()
    conn.close()

# Функция для получения логов
def get_logs():
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs ORDER BY id DESC')
    logs = cursor.fetchall()
    conn.close()
    return logs
  


def add_user_id(user_id):
    """Adds a user ID to the 'user_ids.json' file."""
    try:
        with open(user_ids_file, 'r') as file:
            user_ids = json.load(file)
    except FileNotFoundError:
        user_ids = {}
    user_ids[str(user_id)] = True  # Use True as a placeholder value
    with open(user_ids_file, 'w') as file:
        json.dump(user_ids, file, indent=4)


def load_allowed_users():
    global allowed_users
    try:
        with open(allowed_users_file, 'r') as f:
            data = json.load(f)
            allowed_users = data.get("allowed_users", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки пользователей: {e}")
        allowed_users = []  

def save_allowed_users():
    with open(allowed_users_file, 'w') as f:
        json.dump({"allowed_users": allowed_users}, f)

load_allowed_users()

BOT_TOKEN = '6780798896:AAFfNdOnMO8UiJBQNsatDHchGCw2ch95mR0'
bot = telebot.TeleBot(BOT_TOKEN)
last_request_time = {}


    
@bot.message_handler(commands=['list'])
def listapp(msg):
    # Подсчет количества аккаунтов
    count = len(accounts)

    # Создание клавиатуры
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton("⭐Создатель", url='https://t.me/+Jjvcy_gFSQQzYzky'),
        telebot.types.InlineKeyboardButton("💎Купить подписку", url='https://t.me/Vis1noser_bot?start=1')
    )
    
    # Отправка ответа на сообщение пользователя
    bot.reply_to(msg, f"Количество аккаунтов: {count}", reply_markup=keyboard)
    
    

@bot.callback_query_handler(func=lambda call: call.data == "show_logs")
def show_logs(call):
    logs = get_logs()
    if logs:
        response = "Жалобы:\n"
        for log in logs:
            response += f"Пользователь: {log[1]}, Время: {log[2]}, Цель: {log[3]}\n"
        bot.send_message(call.message.chat.id, response)
    else:
        bot.send_message(call.message.chat.id, "Нет записей о жалобах.")
        

@bot.message_handler(commands=['add'])
def add_allowed_user(message: telebot.types.Message):
    user_id = message.from_user.id

            
    if user_id in admin_ids:
        try:
                    
                    user_to_add = message.text.split()[1]
                    allowed_users.append(int(user_to_add))  # Добавляем новый ID в список
                    save_allowed_users()  # Сохраняем изменения
                    bot.reply_to(message, f"Пользователь с ID {user_to_add} был успешно добавлен.")
        except (IndexError, ValueError):
                    bot.reply_to(message, "Пожалуйста, укажите корректный ID пользователя для добавления.")
    else:
                bot.reply_to(message, "У вас нет прав на выполнение этой команды.")

@bot.message_handler(commands=['remove'])
def remove_allowed_user(message: telebot.types.Message):
    user_id = message.from_user.id

    if user_id in admin_ids:
        try:
            user_to_remove = message.text.split()[1]
            user_to_remove_id = int(user_to_remove)

            if user_to_remove_id in allowed_users:
                allowed_users.remove(user_to_remove_id)  # Удаляем ID из списка
                save_allowed_users()  # Сохраняем изменения
                bot.reply_to(message, f"Пользователь с ID {user_to_remove} был успешно удален.")
            else:
                bot.reply_to(message, f"Пользователь с ID {user_to_remove} не найден в списке разрешенных.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Пожалуйста, укажите корректный ID пользователя для удаления.")
    else:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    user_id = message.from_user.id
    if user_id in allowed_users:
        bot.send_video(message.chat.id, open("vid.mp4", 'rb'), caption="Подписка приобретена!\nЧтобы начать снос - /snos + ссылка на сообщение человека.\nПример: /snos https://t.me/группа/номерсообщения\nНе отправлять больше 5 жалоб если снос не происходит!\nОбновления/новости - https://t.me/+Jjvcy_gFSQQzYzky")
    else:  # This 'else' block is for users NOT in 'allowed_users'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Покупка подписки", url="https://t.me/+Jjvcy_gFSQQzYzky"))
        bot.send_video(message.chat.id, open("vid.mp4", 'rb'), caption="У вас нету подписки. Приобрести подписку вы можете ниже. Цена: 300₽/отдать аккаунт/$\nНовости/обновления - https://t.me/+Jjvcy_gFSQQzYzky", reply_markup=markup)
    add_user_id(message.chat.id)

@bot.message_handler(commands=['snos'])
def handle_link(message: telebot.types.Message):
    user_id = message.from_user.id
    current_time = time.time()

    # Check if the user is in allowed_users
    if user_id not in allowed_users:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Покупка", url="https://t.me/+Jjvcy_gFSQQzYzky"))
        bot.send_video(message.chat.id, open("vid.mp4", 'rb'), caption="У вас нету подписки. Приобрести подписку вы можете ниже. Цена: 300₽/отдать аккаунт/$\nНовости/обновления - https://t.me/+Jjvcy_gFSQQzYzky", reply_markup=markup)
        return

    # Check if one minute has passed since the last request
    if user_id in last_request_time:
        elapsed_time = current_time - last_request_time[user_id]
        if elapsed_time < 300:  # 60 seconds
            remaining_time = 300 - int(elapsed_time)
            bot.reply_to(message, f"Пожалуйста, подождите {remaining_time} секунд(ы) перед повторным запросом. Не спамьте!")
            return

    # Update the last request time
    last_request_time[user_id] = current_time

    # Process the link and add exception handling
    message_link = message.text
    try:
        asyncio.run(process_link(message.chat.id, message_link))  # Make sure process_link is a coroutine
    except sqlite3.OperationalError:
        bot.reply_to(message, "Ошибка! обратитесь к администратору!")
        # Restart the bot
        restart_bot()

async def process_link(chat_id, message_link):
    tasks = [report_spam(chat_id, account, message_link) for account in accounts]
    await asyncio.gather(*tasks)

async def report_spam(chat_id, account, message_link):
    client = TelegramClient(account['session_name'], account['api_id'], account['api_hash'])

    try:
        await client.start()
        await client.sign_in(phone=account['phone'])
    except SessionPasswordNeededError:
        # Запрашиваем пароль через Telegram бота
        password_msg = bot.send_message(chat_id, f'Введите пароль для {account["phone"]}: ')
        bot.register_next_step_handler(password_msg, lambda msg: handle_password(msg, account, message_link, client))
        return  # Завершаем выполнение, так как ожидаем ввод пароля

    print("Пытаемся извлечь данные из ссылки...")
    match = re.search(r't.me/([^/]+)/(\d+)', message_link)
    if match:
        group_username = match.group(1)
        message_id = int(match.group(2))

        print(f"Группа: {group_username}, Сообщение ID: {message_id}")

        # Отправляем сообщение о начале отправки жалобы
        report_message = bot.send_message(chat_id, "Отправка...")

        try:
            message = await client.get_messages(group_username, ids=message_id)
            sender_id = message.from_id  # Получаем ID отправителя сообщения
            if sender_id in admin_ids:
                bot.send_message(chat_id, "С#ука мы тебе хлеб с маслом а ты так")
                return
            
            await client(functions.messages.ReportSpamRequest(peer=message.peer_id))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=report_message.message_id,
                text="Отправлено!"
            )

        except sqlite3.OperationalError:
            bot.send_message(chat_id, "Ошибка! Обратитесь к администратору/повторите позже!")
            # Перезапускаем бота
            restart_bot()
            return
        except Exception as e:
            bot.send_message(chat_id, f"Ошибка при отправке жалобы: {e}")
            return

    else:
        bot.send_message(chat_id, "Не верная ссылка!")

def restart_bot():
    """Перезапускает бота."""
    os.execv(sys.executable, ['python'] + sys.argv)



def handle_password(msg, account, message_link, client):
    password = msg.text
    try:
        asyncio.run(client.sign_in(password=password))
        asyncio.run(report_spam(msg.chat.id, account, message_link, client))
    except Exception as e:
        bot.send_message(msg.chat.id, f"Ошибка при входе: {e}")


@bot.message_handler(commands=['send'])
def handle_broadcast(message):
    global broadcast_text, broadcast_photo  # Access global variables
    if message.from_user.id == admin_id:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Отмена", callback_data="cancel"))
        broadcast_text = ""  # Reset text
        broadcast_photo = None  # Reset photo
        msg = bot.send_message(message.chat.id, "Введите текст для рассылки:", reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_broadcast_text)
    else:
        bot.send_message(message.chat.id, "Ты не админ, не лезь!")
@bot.message_handler(func=lambda message: message.text == '/cancel')
def handle_cancel(message):
    global broadcast_text, broadcast_photo
    if message.from_user.id == admin_id:
        broadcast_text = ""
        broadcast_photo = None
        bot.send_message(message.chat.id, "Отмена рассылки.")
        panel(message)
        return

    else:
        bot.send_message(message.chat.id, "Ты не админ, не лезь!")
def process_broadcast_text(message):
    global broadcast_text, broadcast_photo
    if message.from_user.id == admin_id:
        if message.text == "/cancel":
            handle_cancel(message)  # Call the cancel handler
            return
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Отмена", callback_data="cancel"))
        broadcast_text = message.text
        msg = bot.send_message(message.chat.id, "Отправьте фото (или введите /next, чтобы отправить без фото):", reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_broadcast_photo)
def process_broadcast_photo(message):
    global broadcast_text, broadcast_photo
    if message.from_user.id == admin_id:
        if message.text == "/cancel":
            handle_cancel(message)  # Call the cancel handler
            return
        if message.photo:
            photo_file_id = message.photo[-1].file_id
            broadcast_photo = bot.get_file(photo_file_id)
            downloaded_photo = bot.download_file(broadcast_photo.file_path)
            with open('broadcast_photo.png', 'wb') as f:
                f.write(downloaded_photo)
        send_broadcast(message)
def send_broadcast(message):
    global broadcast_text, broadcast_photo
    try:
        with open(user_ids_file,  'r') as file:
            user_ids = json.load(file)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл с ID пользователей не найден.")
        return
    for user_id in user_ids:
        try:
            if broadcast_photo:
                bot.send_photo(int(user_id), photo=open('broadcast_photo.png', 'rb'), caption=broadcast_text, parse_mode="Markdown")
            else:
                bot.send_message(int(user_id), broadcast_text, parse_mode="Markdown")
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
    bot.send_message(message.chat.id, "*Рассылка завершена.*", parse_mode="Markdown")





broadcast_text = ""
broadcast_link = ""
button_text = ""
broadcast_photo = None
@bot.message_handler(commands=['send1'])
def handle_broadcast_button(message):
    global broadcast_text, broadcast_link, button_text, broadcast_photo
    if message.from_user.id == admin_id:

        broadcast_text = ""  # Reset text
        broadcast_link = ""  # Reset link
        button_text = ""  # Reset button text
        broadcast_photo = None  # Reset photo
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Отмена", callback_data="cancel"))
        msg = bot.send_message(message.chat.id, "Введите текст для рассылки:", reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_broadcast_button_text)
    else:
        bot.send_message(message.chat.id, "Ты не админ, не лезь!")
@bot.message_handler(func=lambda message: message.text == '/cancel')
def handle_cancel(message):
    global broadcast_text, broadcast_link, button_text, broadcast_photo
    if message.from_user.id == admin_id:
        broadcast_text = ""
        broadcast_link = ""
        button_text = ""
        broadcast_photo = None
        bot.send_message(message.chat.id, "Отмена рассылки.\nНажмите еще раз, чтобы вернуться в панель.")
    else:
        bot.send_message(message.chat.id, "Ты не админ, не лезь!")
def process_broadcast_button_text(message):
    global broadcast_text, broadcast_link, button_text, broadcast_photo
    if message.from_user.id == admin_id:
        if message.text == "/cancel":
            handle_cancel(message)
            return
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Отмена", callback_data="cancel"))
        broadcast_text = message.text
        msg = bot.send_message(message.chat.id, "Введите ссылку для кнопки:", reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_broadcast_button_link)
def process_broadcast_button_link(message):
    global broadcast_text, broadcast_link, button_text, broadcast_photo
    if message.from_user.id == admin_id:
        if message.text == "/cancel":
            handle_cancel(message)
            return
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Отмена", callback_data="cancel"))
        broadcast_link = message.text
        msg = bot.send_message(message.chat.id, "Введите текст для кнопки:", reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_broadcast_button_button_text)
def process_broadcast_button_button_text(message):
    global broadcast_text, broadcast_link, button_text, broadcast_photo
    if message.from_user.id == admin_id:
        if message.text == "/cancel":
            handle_cancel(message)
            return
        button_text = message.text
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("Отмена", callback_data="cancel"))
        msg = bot.send_message(message.chat.id, "Отправьте фото (или введите /nextstep, чтобы отправить без фото):", reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_broadcast_button_photo)
def process_broadcast_button_photo(message):
    global broadcast_text, broadcast_link, button_text, broadcast_photo
    if message.from_user.id == admin_id:
        if message.text == "/cancel":
            handle_cancel(message)
            return
        if message.photo:
            photo_file_id = message.photo[-1].file_id
            broadcast_photo = bot.get_file(photo_file_id)
            downloaded_photo = bot.download_file(broadcast_photo.file_path)
            with open('broadcast_photo.png', 'wb') as f:
                f.write(downloaded_photo)
        send_broadcast_button(message)
def send_broadcast_button(message):
    user_ids_file = 'user_ids.json'
    global broadcast_text, broadcast_link, button_text, broadcast_photo
    try:
        with open(user_ids_file, 'r') as file:
            user_ids = json.load(file)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл с ID пользователей не найден.")
        return
    for user_id in user_ids:
        try:
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text=button_text, url=broadcast_link)
            markup.add(button)
            if broadcast_photo:
                bot.send_photo(int(user_id), photo=open('broadcast_photo.png', 'rb'), caption=broadcast_text, reply_markup=markup, parse_mode="Markdown")
            else:
                bot.send_message(int(user_id), broadcast_text, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
    bot.send_message(message.chat.id, "*Рассылка с кнопкой завершена.*", parse_mode="Markdown")
# Function to generate a unique screenshot name

@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel(call):
    
    user_states.pop(call.message.chat.id, None)
    bot.send_message(call.message.chat.id, "*Действие отменено.*", parse_mode="Markdown")
    bot.clear_step_handler_by_chat_id(call.message.chat.id)

user_states = {}



    
if __name__ == "__main__":
    init_db()  # Проверяем или создаем базу данных и таблицу
    bot.polling()
