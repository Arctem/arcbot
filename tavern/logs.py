from datetime import datetime

import ircbot.storage as db

from tavern.shared import TavernException
from tavern.tavern_models import HeroActivity, TavernLog


def make_discovery_log(dungeon):
    return TavernLog(text="The entrance to {} has been found!".format(dungeon), time=datetime.now())


def make_arrival_log(hero):
    return TavernLog(text="The brave hero {} has arrived in town!".format(hero), time=datetime.now())

STOP_LOGS = {
    HeroActivity.Elsewhere: None,
    HeroActivity.CommonPool: "{hero} has left the town square.",
    HeroActivity.VisitingTavern: "{hero} has left {tavern}.",
    HeroActivity.Hired: "{hero} has stopped being hired?",  # TODO
    HeroActivity.Adventuring: "{hero} has stopped adventuring?",  # TODO
    HeroActivity.Dead: "{hero} has stopped...being dead? Really?",  # TODO
}


def make_stop_activity_log(hero):
    text = STOP_LOGS[hero.activity]
    if text:
        return TavernLog(text=text.format(hero=hero, tavern=hero.visiting), time=datetime.now())

START_LOGS = {
    HeroActivity.Elsewhere: None,
    HeroActivity.CommonPool: "{hero} is hanging out in the town square.",
    HeroActivity.VisitingTavern: "{hero} is visiting {tavern}.",
    HeroActivity.Hired: "{hero} was hired by {patron}.",
    HeroActivity.Adventuring: "{hero} has started adventuring?",  # TODO
    HeroActivity.Dead: "{hero} has died? Really? I didn't think we did that yet.",  # TODO
}


def make_start_activity_log(hero):
    text = START_LOGS[hero.activity]
    if text:
        return TavernLog(text=text.format(hero=hero, tavern=hero.visiting, patron=hero.patron), time=datetime.now())


@db.needs_session
def get_unsent(s=None):
    return s.query(TavernLog).filter(TavernLog.sent == False).order_by(TavernLog.time).all()


@db.atomic
def mark_all_sent(s=None):
    return s.query(TavernLog).update({TavernLog.sent: True})
