# coding:utf8
from config import *
import MySQLdb


class DataBase:
    def __init__(self, first=False):
        self.__db = None
        self.__cursor = None
        self.load_db(first)

    def load_db(self, first):
        try:
            self.__db = MySQLdb.connect(CONFIG.DBHost, CONFIG.DBLogin, CONFIG.DBPassword, CONFIG.DBName)
            self.__cursor = self.__db.cursor()
            self.__db.set_character_set('utf8mb4')
        except MySQLdb.Error as e:
            print("[load_db]: DataBase Error " + e.args[1])
            return False
        if first:
            return self.__check_tables()
        return True

    def __check_tables(self):
        try:
            self.__cursor.execute("show tables")
            tables = self.__cursor.fetchall()
            if not self.__contains(tables, CONFIG.DBTableWorks):
                self.__cursor.execute("CREATE TABLE " + CONFIG.DBTableWorks + CONFIG.DBTableWorksRequest + ";")
            if not self.__contains(tables, CONFIG.DBTableMessages):
                self.__cursor.execute("CREATE TABLE " + CONFIG.DBTableMessages + CONFIG.DBTableMessagesRequest + ";")
        except MySQLdb.Error as e:
            print("[check_tables]: DataBase Error " + e.args[1])
            self.close()
            return False
        self.close()
        return True

    @staticmethod
    def __contains(tables, table):
        for tables1 in tables:
            for t in tables1:
                if t == table:
                    return True
        return False

    def add_work(self, work):
        request = "insert into " + \
                  CONFIG.DBTableWorks + \
                  "(chat_id, timestap, status)" + \
                  " values (" + \
                  str(work.chat_id) + ", " + \
                  str(work.timestap) + ", " + \
                  str(work.status) + \
                  ");"
        try:
            self.__db.query(request)
            self.__db.commit()
        except MySQLdb.Error as e:
            print("[add_work]: DB Error: " + e.args[1])
            self.close()
            return None
        return work

    def get_id(self, work):
        request = "SELECT * FROM " + \
                  CONFIG.DBTableWorks + \
                  " WHERE chat_id=" + \
                  str(work.chat_id) + \
                  " AND timestap=" + \
                  str(work.timestap) + \
                  ";"
        try:
            self.__cursor.execute(request)
        except MySQLdb.Error as e:
            print("[get_id]: DB Error: " + e.args[1])
            self.close()
            return None
        result = self.__cursor.fetchall()
        return result[0][0]

    def close(self):
        self.__db.close()

    def update_work(self, work):
        request = "UPDATE " + \
                  CONFIG.DBTableWorks + \
                  " SET " + \
                  "status=" + str(work.status) + \
                  ("" if work.header is None else ", header='" + work.header + "'") + \
                  ("" if work.text is None else ", text='" + work.text + "'") + \
                  ("" if work.uah == -1 else ", uah=" + str(work.uah)) + \
                  ("" if work.usd == -1 else ", usd=" + str(work.usd)) + \
                  " WHERE ID=" + \
                  "" + \
                  str(work.id) + \
                  ";"
        try:
            self.__cursor.execute(request.encode('utf8'))
            self.__db.commit()
        except MySQLdb.Error as e:
            print("[update_work]: DB Error: " + e.args[1])

    def remove_message(self, chat_id, msg_id, work_id):
        request = "DELETE FROM " + \
                  CONFIG.DBTableMessages + \
                  " WHERE " + \
                  "chat_id=" + str(chat_id) + \
                  " AND message=" + str(msg_id) + \
                  " AND work_id=" + str(work_id) + \
                  ";"
        try:
            self.__cursor.execute(request.encode('utf8'))
            self.__db.commit()
        except MySQLdb.Error as e:
            print("[remove_message]: DB Error: " + e.args[1])

    def add_message(self, chat_id, msg_id, work_id):
        request = "insert into " + \
                  CONFIG.DBTableMessages + \
                  "(chat_id, message, work_id)" + \
                  " values (" + \
                  str(chat_id) + ", " + \
                  str(msg_id) + ", " + \
                  str(work_id) + \
                  ");"
        try:
            self.__db.query(request)
            self.__db.commit()
        except MySQLdb.Error as e:
            print("[add_message]: DB Error: " + e.args[1])
            self.close()

    def get_works(self):
        request = "SELECT * FROM " + \
                  CONFIG.DBTableWorks + \
                  ";"
        try:
            self.__cursor.execute(request)
        except MySQLdb.Error as e:
            print("[get_works]: DB Error: " + e.args[1])
            self.close()
            return list()
        result = self.__cursor.fetchall()
        return result

    def get_messages(self, chat_id, work_id):
        request = "SELECT * FROM " + \
                  CONFIG.DBTableMessages + \
                  " WHERE chat_id=" + str(chat_id) + \
                  " AND work_id=" + str(work_id) + \
                  ";"
        try:
            self.__cursor.execute(request)
        except MySQLdb.Error as e:
            print("[get_messages]: DB Error: " + e.args[1])
            self.close()
            return list()
        result = self.__cursor.fetchall()
        return result

    def remove_work(self, work):
        request = "DELETE FROM " + \
                  CONFIG.DBTableWorks + \
                  " WHERE " + \
                  "ID=" + str(work.id) + \
                  ";"
        try:
            self.__cursor.execute(request)
            self.__db.commit()
        except MySQLdb.Error as e:
            print("[remove_work]: DB Error: " + e.args[1])
        return
