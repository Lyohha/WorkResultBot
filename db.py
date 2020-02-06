from config import *
import MySQLdb


class DataBase:
    def __init__(self, first=False):
        self.__load_db(first)

    def __load_db(self, first):
        self.__db = MySQLdb.connect(CONFIG.DBHost, CONFIG.DBLogin, CONFIG.DBPassword, CONFIG.DBName)
        self.__cursor = self.__db.cursor()
        if first:
            self.__check_tables()

    def __check_tables(self):
        try:
            self.__cursor.execute("show tables")
            tables = self.__cursor.fetchall()
            if not self.__contains(tables, CONFIG.DBTableWorks):
                self.__cursor.execute("""CREATE TABLE """ + CONFIG.DBTableWorks + CONFIG.DBTableWorksRequest + """;""")
        except MySQLdb.Error as e:
            print("DataBase Error " + e.args[1])
        self.__db.close()

    def __contains(self, tables, table):
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
            print("DB Error: " + e.args[1])
            self.__db.close()
            return None
        self.__db.close()
        return work

    def update_work(self, work):
        return
