from db import DataBase


class Work:
    def __init__(self):
        self.__chat_id = None
        self.__id = None
        self.__header = None
        self.__text = None
        self.__timestap = None
        self.__status = None

    @property
    def chat_id(self):
        return self.__chat_id

    @property
    def id(self):
        return self.__id

    @property
    def header(self):
        return self.__header

    @property
    def text(self):
        return self.__text

    @property
    def timestap(self):
        return self.__timestap

    @property
    def status(self):
        return self.__status

    @staticmethod
    def new_instance(id, chat_id, header, text, timestap, status):
        work = Work()
        work.__id = id
        work.__chat_id = chat_id
        work.__header = header
        work.__text = text
        work.__timestap = timestap
        work.__status = status

        db = DataBase()
        db.add_work(work)

        return work

