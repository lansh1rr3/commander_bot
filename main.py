import telebot
import os
import pyautogui
import threading
import time
import webbrowser
import subprocess
import ctypes
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from telebot import types
import sys

# Тут указать токен Telegram-бота
TOKEN = '8020811243:AAEOFHbUR2CFX4HuNAik2twtLoZNNTOHQJ8'
bot = telebot.TeleBot(TOKEN)


# Функция для выключения компьютера
def shutdown_computer():
    if os.name == 'nt':
        os.system('shutdown /s /t 0')
    else:
        os.system('shutdown now')


# Функция для перезагрузки компьютера
def restart_computer():
    if os.name == 'nt':
        os.system('shutdown /r /t 0')
    else:
        os.system('reboot')


# Функция для выключения компьютера через определенное время
def shutdown_after_delay(delay):
    time.sleep(delay)
    shutdown_computer()


# Функция для открытия сайтов
def open_website(url):
    webbrowser.open(url)


# Функция для запуска программ
def open_application(app_path):
    try:
        subprocess.Popen(app_path)
    except Exception as e:
        return str(e)
    return "Программа запущена."


# Функция для очистки корзины (Windows)
def empty_recycle_bin():
    if os.name == 'nt':
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
        return "Корзина очищена."
    else:
        return "Очистка корзины поддерживается только на Windows."


# Функция для записи звука с микрофона
def record_audio(filename="audio.wav", duration=5, fs=44100):
    try:
        # Установим количество каналов на 1 (моно)
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Ожидание завершения записи
        write(filename, fs, np.array(audio_data))
        return filename
    except Exception as e:
        return f"Ошибка при записи аудио: {e}"


# Функция для отправки сообщения на рабочий стол (Windows)
def show_message_box(title="Сообщение", text="Это сообщение на рабочем столе."):
    if os.name == 'nt':
        ctypes.windll.user32.MessageBoxW(0, text, title, 1)


# Функция для перевода компьютера в режим сна (Windows)
def sleep_computer():
    if os.name == 'nt':
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Компьютер переведен в режим сна."
    else:
        return "Режим сна поддерживается только на Windows."


# Функция для открытия диспетчера задач (Windows)
def open_task_manager():
    if os.name == 'nt':
        # Проверяем, есть ли у нас права администратора
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # Если прав нет, запрашиваем повышение прав
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit()
        else:
            # Если права есть, открываем Диспетчер задач
            subprocess.Popen('taskmgr')
            return "Диспетчер задач открыт."
    else:
        return "Открытие диспетчера задач поддерживается только на Windows."


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Главная клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_manage_pc = types.KeyboardButton('Управление ПК')
    btn_sites_programs = types.KeyboardButton('Сайты и программы')
    markup.add(btn_manage_pc, btn_sites_programs)

    bot.send_message(message.chat.id, "Привет! Я бот для управления компьютером. Выберите категорию:",
                     reply_markup=markup)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Управление ПК':
        # Клавиатура для управления ПК
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_screenshot = types.KeyboardButton('Сделать скриншот')
        btn_shutdown = types.KeyboardButton('Выключить компьютер')
        btn_restart = types.KeyboardButton('Перезагрузить компьютер')
        btn_shutdown_in = types.KeyboardButton('Выключить через время')
        btn_empty_bin = types.KeyboardButton('Очистить корзину')
        btn_record_audio = types.KeyboardButton('Записать звук')
        btn_show_message = types.KeyboardButton('Сообщение на рабочий стол')
        btn_sleep = types.KeyboardButton('Режим сна')
        btn_task_manager = types.KeyboardButton('Открыть диспетчер задач')
        btn_back = types.KeyboardButton('Назад')
        markup.add(btn_screenshot, btn_shutdown, btn_restart, btn_shutdown_in)
        markup.add(btn_empty_bin, btn_record_audio, btn_show_message)
        markup.add(btn_sleep, btn_task_manager, btn_back)

        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

    elif message.text == 'Сайты и программы':
        # Клавиатура для сайтов и программ
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_open_youtube = types.KeyboardButton('YouTube')
        btn_open_steam = types.KeyboardButton('Steam')
        btn_open_tg = types.KeyboardButton('Telegram')
        btn_open_ds = types.KeyboardButton('Discord')
        btn_back = types.KeyboardButton('Назад')
        markup.add(btn_open_youtube, btn_open_steam, btn_open_tg, btn_open_ds, btn_back)

        bot.send_message(message.chat.id, "Выберите сайт или программу:", reply_markup=markup)

    elif message.text == 'Назад':
        # Возвращаемся к главной клавиатуре
        send_welcome(message)

    elif message.text == 'Сделать скриншот':
        screenshot_image = pyautogui.screenshot()
        screenshot_image.save('screenshot.png')
        with open('screenshot.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove('screenshot.png')

    elif message.text == 'Выключить компьютер':
        bot.send_message(message.chat.id, "Выключаю компьютер...")
        shutdown_computer()

    elif message.text == 'Перезагрузить компьютер':
        bot.send_message(message.chat.id, "Перезагружаю компьютер...")
        restart_computer()

    elif message.text == 'Выключить через время':
        bot.send_message(message.chat.id, "Укажите время в секундах. Пример: 60")
        bot.register_next_step_handler(message, shutdown_in)

    elif message.text == 'Очистить корзину':
        response = empty_recycle_bin()
        bot.send_message(message.chat.id, response)

    elif message.text == 'Записать звук':
        filename = "audio.wav"
        response = record_audio(filename)
        if response == filename:
            with open(filename, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
            os.remove(filename)
        else:
            bot.send_message(message.chat.id, response)

    elif message.text == 'Сообщение на рабочий стол':
        show_message_box(title="Сообщение от бота", text="Это сообщение на рабочем столе.")
        bot.send_message(message.chat.id, "Сообщение отправлено на рабочий стол.")

    elif message.text == 'Режим сна':
        response = sleep_computer()
        bot.send_message(message.chat.id, response)

    elif message.text == 'Открыть диспетчер задач':
        response = open_task_manager()
        bot.send_message(message.chat.id, response)

    elif message.text == 'YouTube':
        bot.send_message(message.chat.id, "Открываю YouTube...")
        open_website('https://www.youtube.com')

    elif message.text == 'Steam':
        steam_path = r'C:\Program Files (x86)\Steam\steam.exe'
        response = open_application(steam_path)
        bot.send_message(message.chat.id, response)

    elif message.text == 'Telegram':
        tg_path = r'C:\Users\Student\Downloads\AyuGram\AyuGram.exe'
        response = open_application(tg_path)
        bot.send_message(message.chat.id, response)

    elif message.text == 'Discord':
        ds_path = r'C:\Users\vipma\AppData\Local\Discord\app-1.0.9163\Discord.exe'
        response = open_application(ds_path)
        bot.send_message(message.chat.id, response)


# Функция для отложенного выключения C:\Users\Student\Downloads\AyuGram\AyuGram.exe
def shutdown_in(message):
    try:
        delay = int(message.text)
        bot.send_message(message.chat.id, f"Компьютер будет выключен через {delay} секунд...")
        threading.Thread(target=shutdown_after_delay, args=(delay,)).start()
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите корректное число в секундах.")


# Запуск бота
bot.polling()
