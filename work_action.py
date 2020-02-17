# coding:utf8
import telebot
import re
from work import *
from datetime import *
import tg as TG


class WorkAction:
    actions = dict()

    def __init__(self, work):
        self.__work = work

    @staticmethod
    def get_instance(work):
        wa = WorkAction(work)
        WorkAction.actions[work.id] = wa
        return wa

    @staticmethod
    def load_from_db(db_object):
        return

    @staticmethod
    def remove(wa):
        if wa.__work.id in WorkAction.actions:
            del WorkAction.actions[wa.__work.id]
        return

    @staticmethod
    def get_work_action_by_chat_id(chat_id):
        for key in WorkAction.actions:
            if WorkAction.actions[key].__work.chat_id == chat_id and WorkAction.actions[key].__work.status != 6:
                return WorkAction.actions[key]
        return None

    @staticmethod
    def get_work_action_by_id(id):
        id = int(id)
        for key in WorkAction.actions:
            if WorkAction.actions[key].__work.id == id:
                return WorkAction.actions[key]
        for key in WorkAction.actions:
            if WorkAction.actions[key].__work.t_id == id:
                return WorkAction.actions[key]
        return None

    @staticmethod
    def new(chat_id):
        work = Work.new_instance(None, chat_id, None, None, int(datetime.now().timestamp()), 0)
        if work is None:
            TG.TelegramBot.send_message(work.chat_id,
                                        "В данный момент происходит техническое обслуживание. Попытайтесь позже.")
            return
        action = WorkAction(work)
        WorkAction.actions[work.id] = action
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("Отменить создание")
        TG.TelegramBot.send_message(work.chat_id, "Укажите заголовок", keyboard)

    def update_by_msg(self, msg):
        if self.__work.status == 0:
            self.__work.status = 1
            self.__work.header = msg
            TG.TelegramBot.send_message(self.__work.chat_id, "Укажите описание работы.")
        elif self.__work.status == 1:
            self.__work.status = 2
            self.__work.text = msg
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(
                telebot.types.InlineKeyboardButton("UAH", callback_data="id=" + str(self.__work.id) + "&types=UAH"),
                telebot.types.InlineKeyboardButton("USD", callback_data="id=" + str(self.__work.id) + "&types=USD")
            )
            msg = TG.TelegramBot.send_message(self.__work.chat_id, "Выберите валюту.", keyboard)
            self.__work.add_message(msg.message_id)
        elif self.__work.status == 3:
            msg = re.sub(r"\D", "", msg)
            if len(msg) == 0:
                msg = "-1"
            if int(msg) < 0:
                TG.TelegramBot.send_message(self.__work.chat_id, "Сумма должна быть неотрицательная!\n")
            else:
                self.__work.status = 5
                self.__work.uah = int(msg)
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(
                    telebot.types.InlineKeyboardButton("Подтвердить добавление работы",
                                                       callback_data="id=" + str(self.__work.id) + "&action=accept"),
                    telebot.types.InlineKeyboardButton("Отменить добавление работы",
                                                       callback_data="id=" + str(self.__work.id) + "&action=cancel")
                )
                msg = TG.TelegramBot.send_message(self.__work.chat_id, "Подтвердите добавление работы.\n" +
                                                  self.__work.header + "\n" +
                                                  self.__work.text + "\n" +
                                                  ("" if self.__work.uah < 0 else "UAH: " + str(
                                                      self.__work.uah) + "\n") +
                                                  ("" if self.__work.usd < 0 else "USD: " + str(
                                                      self.__work.usd) + "\n"), keyboard)
                self.__work.add_message(msg.message_id)
        elif self.__work.status == 4:
            msg = re.sub(r"\D", "", msg)
            if len(msg) == 0:
                msg = "-1"
            if int(msg) < 0:
                TG.TelegramBot.send_message(self.__work.chat_id, "Сумма должна быть неотрицательная!\n")
            else:
                self.__work.status = 5
                self.__work.usd = int(msg)
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(
                    telebot.types.InlineKeyboardButton("Подтвердить добавление работы",
                                                       callback_data="id=" + str(self.__work.id) + "&action=accept"),
                    telebot.types.InlineKeyboardButton("Отменить добавление работы",
                                                       callback_data="id=" + str(self.__work.id) + "&action=cancel")
                )
                msg = TG.TelegramBot.send_message(self.__work.chat_id, "Подтвердите добавление работы.\n" +
                                                  self.__work.header + "\n" +
                                                  self.__work.text + "\n" +
                                                  ("" if self.__work.uah < 0 else "UAH: " + str(
                                                      self.__work.uah) + "\n") +
                                                  ("" if self.__work.usd < 0 else "USD: " + str(
                                                      self.__work.usd) + "\n"), keyboard)
                self.__work.add_message(msg.message_id)

        self.__work.update()

    def update_by_button(self, params):
        if 'types' in params:
            TG.TelegramBot.remove_messages(self.__work)
            if params['types'] == 'UAH':
                self.__work.status = 3
                TG.TelegramBot.send_message(self.__work.chat_id, "Введите сумму в UAH")
            elif params['types'] == 'USD':
                self.__work.status = 4
                TG.TelegramBot.send_message(self.__work.chat_id, "Введите сумму в USD")
            self.__work.update()
        elif 'action' in params:
            TG.TelegramBot.remove_messages(self.__work)
            if params['action'] == 'accept':
                self.__work.status = 6
                TG.TelegramBot.send_buttons(self.__work.chat_id, "Добавление завершено")
                WorkAction.remove(self)
                self.__work.update()
            elif params['action'] == 'cancel':
                TG.TelegramBot.send_buttons(self.__work.chat_id, "Добавление отменено")
                WorkAction.remove(self)
                self.__work.remove()

    def cancel(self):
        TG.TelegramBot.remove_messages(self.__work)
        WorkAction.remove(self)
        self.__work.remove()
