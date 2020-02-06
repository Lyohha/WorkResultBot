from work import *
from datetime import *
import tg as TG


class WorkAction:
    actions = dict()

    def __init__(self, work):
        self.__work = work

    @staticmethod
    def load_from_db(db_object):
        return

    @staticmethod
    def new(chat_id):
        work = Work.new_instance(None, chat_id, None, None, int(datetime.now().timestamp()), 0)
        if work == None:
            TG.TelegramBot.send_message(work.chat_id,
                                        "В данный момент происходит техническое обслужевание. Попытайтесь позже.")
            return
        action = WorkAction(work)
        WorkAction.actions[work.chat_id] = work
        TG.TelegramBot.send_message(work.chat_id, "Попытка создать новую фигню")
