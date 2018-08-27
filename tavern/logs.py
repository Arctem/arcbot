from datetime import datetime

import ircbot.storage as db

from tavern.shared import TavernException
from tavern.tavern_models import TavernLog


def make_discovery_log(dungeon):
    return TavernLog(text="The entrance to {} has been found!".format(dungeon), time=datetime.now())


def make_arrival_log(hero):
    return TavernLog(text="The brave hero {} has arrived in town!".format(hero), time=datetime.now())


@db.needs_session
def get_unsent(s=None):
    return s.query(TavernLog).filter(TavernLog.sent == False).order_by(TavernLog.time).all()


@db.atomic
def mark_all_sent(s=None):
    return s.query(TavernLog).update({TavernLog.sent: True})
