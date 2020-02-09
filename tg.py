# coding:utf8
import telebot
from config import *
import work_action as WA
from work import *


class TelegramBot:
    bot = None
    handler = None

    @staticmethod
    def build_handler_dict(handler, **args):
        return {
            'function': handler,
            'filters': args
        }

    def __init__(self):
        TelegramBot.bot = telebot.TeleBot(CONFIG.TelegramToken)
        TelegramBot.bot.set_update_listener(TelegramBot.message_listener)
        TelegramBot.bot.add_callback_query_handler(
            TelegramBot.build_handler_dict(TelegramBot.buttons_listener, func=TelegramBot.buttons_listener, call=True))
        TelegramBot.bot.polling(none_stop=True)

    @staticmethod
    def message_listener(messages):
        for message in messages:
            if message.text == "/start" and WA.WorkAction.get_work_action_by_chat_id(message.chat.id) is None:
                TelegramBot.send_buttons(message.chat.id, "Настройка кнопок управления")
            elif message.text == "Добавить работу":
                WA.WorkAction.new(message.chat.id)
            elif message.text == "Помощь":
                TelegramBot.send_message(message.chat.id,
                                         "Помощь\n" +
                                         "Добавить работу - добавляет новую работу в список выполненых\n" +
                                         "Работы за месяц - выводит список выполненных работ за текущий месяц\n" +
                                         "Работы за все время - выводит список работ, которые были выполнены за все время")
            elif message.text == "Работы за месяц":
                continue
            elif message.text == "Работы за все время":
                Work.show_user_works(message.chat.id)
            elif message.text == "Отменить создание":
                TelegramBot.send_buttons(message.chat.id, "Добавление отменено")
                wa = WA.WorkAction.get_work_action_by_chat_id(message.chat.id)
                if wa is not None:
                    wa.cancel()
            else:
                wa = WA.WorkAction.get_work_action_by_chat_id(message.chat.id)
                if wa is not None:
                    wa.update_by_msg(message.text)
                else:
                    TelegramBot.send_buttons(message.chat.id, "Похоже произошла ошибка в системе. Попытайтесь еще раз")

    @staticmethod
    def buttons_listener(call):
        params = TelegramBot.get_params(call.data)
        if 'id' in params:
            wa = WA.WorkAction.get_work_action_by_id(params['id'])
            if wa is not None:
                wa.update_by_button(params)
            else:
                TelegramBot.send_buttons(call.message.chat.id, "Похоже произошла ошибка в системе. Попытайтесь еще раз")

    @staticmethod
    def get_params(data):
        params = data.split('&')
        d = dict()
        for param in params:
            temp = param.split('=')
            if len(temp) < 2:
                continue
            d[temp[0]] = temp[1]
        return d

    @staticmethod
    def send_message(chat_id, msg, keyboard=None):
        if keyboard is None:
            return TelegramBot.bot.send_message(chat_id, msg)
        else:
            return TelegramBot.bot.send_message(chat_id, msg, reply_markup=keyboard)

    @staticmethod
    def remove_messages(work):
        db = DataBase()
        for msg_id in work.get_messages():
            TelegramBot.remove_message(work.chat_id, msg_id)
            db.remove_message(work.chat_id, msg_id, work.id)
        work.remove_messages()
        db.close()

    @staticmethod
    def remove_message(chat_id, msg_id):
        TelegramBot.bot.delete_message(chat_id, msg_id)

    @staticmethod
    def send_buttons(chat_id, msg):
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("Добавить работу", "Помощь")
        keyboard.row("Работы за месяц", "Работы за все время")
        TelegramBot.bot.send_message(chat_id, msg, reply_markup=keyboard)
