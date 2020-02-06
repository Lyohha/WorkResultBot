import telebot
from config import *
import work_action as WA


class TelegramBot:
    bot = None

    def __init__(self):
        TelegramBot.bot = telebot.TeleBot(CONFIG.TelegramToken)
        TelegramBot.bot.set_update_listener(TelegramBot.message_listener)
        TelegramBot.bot.polling(none_stop=True)

    @staticmethod
    def message_listener(messages):
        for message in messages:
            if message.text == "/start":
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.row("Добавить работу", "Помощь")
                keyboard.row("Работы за месяц", "Работы за все время")
                TelegramBot.bot.send_message(message.chat.id, "Настройка кнопок управления", reply_markup=keyboard)
            elif message.text == "Добавить работу":
                WA.WorkAction.new(message.chat.id)
            elif message.text == "Помощь":
                continue
            elif message.text == "Работы за месяц":
                continue
            elif message.text == "Работы за все время":
                continue

    @staticmethod
    def send_message(chat_id, msg):
        TelegramBot.bot.send_message(chat_id, msg)