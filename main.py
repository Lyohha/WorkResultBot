# coding:utf8
from tg import *
from db import *


def load_from_db():
    db = DataBase()
    works = db.get_works()
    for w in works:
        work = Work.new_instance_from_db(w)
        if work.status != 6:
            wa = WA.WorkAction.get_instance(work)
            messages = db.get_messages(work.chat_id, work.id)
            for msg_id in messages:
                work.add_message(msg_id)
    db.close()


def main():
    print("WorkResultBot Start")
    db = DataBase(True)
    load_from_db()
    tg = TelegramBot()
    while True:
        continue


main()
