import threading

from sqlalchemy import Column, String

from SiestaRobot.modules.sql import BASE, SESSION # import your file name

class VanitasUser(BASE):
    __tablename__ = "vanitasuser"
    chat_id = Column(String(14), primary_key=True)
    user_id = Column(Integer, primary_key=True)

    def __init__(self, chat_id, user_id):
        self.chat_id = str(chat_id)  # ensure string
        self.user_id = user_id

    def __repr__(self):
        return "<Vanitas %s>" % self.user_id


VanitasUser.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


class VanitasChats(BASE):
    __tablename__ = "vanitas_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

VanitasChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_vanitas(chat_id):
    try:
        vanitaschat = SESSION.query(VanitasChats).get(str(chat_id))
        return bool(vanitaschat)
    finally:
        SESSION.close()


def rem_vanitas(chat_id):
    with INSERTION_LOCK:
        vanitaschat = SESSION.query(VanitasChats).get(str(chat_id))
        if not vanitaschat:
            vanitaschat = VanitasChats(str(chat_id))
        SESSION.add(vanitaschat)
        SESSION.commit()


def set_vanitas(chat_id):
    with INSERTION_LOCK:
        vaitaschat = SESSION.query(VanitasChats).get(str(chat_id))
        if vaitaschat:
            SESSION.delete(vaitaschat)
        SESSION.commit()
