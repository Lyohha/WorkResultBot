# coding:utf8
from db import DataBase
import tg as TG
import encoding as Encode


# Status
# 0 - new work / wait header
# 1 - wait text
# 2 - wait type money
# 3 - wait UAH
# 4 - wait USD
# 5 - wait accept work
# 6 - work created


class Work:
    list = list()
    temp_id = -1

    def __init__(self):
        self.__chat_id = None
        self.__id = None
        self.__header = None
        self.__text = None
        self.__timestap = 0
        self.__status = -1
        self.__uah = -1
        self.__usd = -1
        self.__messages = list()
        self.__temp_id = Work.temp_id
        Work.temp_id -= 1

    @property
    def chat_id(self):
        return self.__chat_id

    @chat_id.setter
    def chat_id(self, value):
        self.__chat_id = value

    @property
    def id(self):
        if self.__id is None:
            return self.__temp_id
        return self.__id

    @property
    def t_id(self):
        return self.__temp_id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, value):
        self.__header = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def timestap(self):
        return self.__timestap

    @timestap.setter
    def timestap(self, value):
        self.__timestap = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def uah(self):
        return self.__uah

    @uah.setter
    def uah(self, value):
        self.__uah = value

    @property
    def usd(self):
        return self.__usd

    @usd.setter
    def usd(self, value):
        self.__usd = value

    def add_message(self, msg_id):
        self.__messages.append(msg_id)
        db = DataBase()
        db.add_message(self.chat_id, msg_id, self.id)
        db.close()

    def get_messages(self):
        return self.__messages

    def remove_messages(self):
        self.__messages = list()

    @staticmethod
    def new_instance_from_db(db_object):
        work = Work()
        work.id = db_object[0]
        work.chat_id = db_object[1]
        if db_object[2] is not None:
            work.header = db_object[2].encode('utf8').decode()
            Encode.decode(db_object[2])
            print(db_object[2].encode('utf8'))
            print(db_object[2].encode('utf8').decode('utf8'))
            print(work.header)
        if db_object[3] is not None:
            work.text = db_object[3].encode().decode()
        work.timestap = db_object[4]
        work.status = db_object[5]
        if db_object[6] is not None:
            work.uah = db_object[6]
        if db_object[7] is not None:
            work.usd = db_object[7]

        Work.list.append(work)

        return work

    @staticmethod
    def new_instance(id, chat_id, header, text, timestap, status):
        work = Work()
        work.id = id
        work.chat_id = chat_id
        work.header = header
        work.text = text
        work.timestap = timestap
        work.status = status

        db = DataBase()
        work = db.add_work(work)
        if work is None:
            return None
        work.id = int(db.get_id(work))
        if work.id is None:
            return None

        db.close()

        Work.list.append(work)

        return work

    def update(self):
        db = DataBase()
        db.update_work(self)

    def remove(self):
        db = DataBase()
        db.remove_work(self)
        Work.list.remove(self)

    @staticmethod
    def show_user_works(chat_id):
        for work in Work.list:
            if work.chat_id == chat_id:
                if work.status == 6:
                    TG.TelegramBot.send_message(chat_id, work.header + "\n" + work.text + "\n" +
                                                ("" if work.uah < 0 else "UAH: " + str(work.uah) + "\n") +
                                                ("" if work.usd < 0 else "USD: " + str(work.usd) + "\n"))
