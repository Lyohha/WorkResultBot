# coding:utf8
def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)


class Config(object):
    @constant
    def TelegramToken():
        return "821891169:AAFlNWbrBP_y662sncqHR1JghNeC5ywMjUM"

    @constant
    def DBName():
        return "tgbase"

    @constant
    def DBLogin():
        return "root"

    @constant
    def DBPassword():
        return ""

    @constant
    def DBTableWorks():
        return "tg_works"

    @constant
    def DBTableMessages():
        return "tg_messages"

    @constant
    def DBTableMessagesRequest():
        return """(ID INT NOT NULL AUTO_INCREMENT Primary key, chat_id INT NOT NULL, work_id INT NOT NULL, message INT NOT NULL)"""

    @constant
    def DBTableWorksRequest():
        return """(ID INT NOT NULL AUTO_INCREMENT Primary key, chat_id INT NOT NULL, header TEXT COLLATE 'utf8_general_ci', text TEXT COLLATE 'utf8_general_ci', timestap INT NOT NULL, status INT NOT NULL, uah INT, usd INT)"""

    @constant
    def DBHost():
        return "localhost"


CONFIG = Config()
