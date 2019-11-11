from datetime import datetime

import ircbot.storage as db

import tavern.pool.controller as pool_controller
from tavern.shared import TavernException
from tavern.tavern_models import HeroActivity, TavernLog


@db.needs_session
def make_discovery_log(dungeon, s=None):
    return TavernLog(text="The entrance to {} has been found!".format(dungeon), time=datetime.now())


@db.needs_session
def make_arrival_log(hero, s=None):
    return TavernLog(text="The brave hero {} has arrived in town!".format(hero), time=datetime.now())

STOP_LOGS = {
    HeroActivity.Elsewhere: None,
    HeroActivity.CommonPool: "{hero} has left the town square.",
    HeroActivity.VisitingTavern: "{hero} has left {tavern}.",
    HeroActivity.Hired: "{hero} is no longer waiting orders from {employer}.",
    HeroActivity.Adventuring: "{hero} has left {dungeon}.",
    HeroActivity.Dead: "{hero} has stopped...being dead? Really?",  # TODO
}


@db.needs_session
def make_stop_activity_log(hero, s=None):
    text = STOP_LOGS[hero.activity]
    if text:
        return TavernLog(text=text.format(hero=hero, tavern=hero.visiting,
                                          patron=hero.patron, employer=hero.employer,
                                          dungeon=pool_controller.get_dungeon(hero, s=s)),
                         time=datetime.now())

START_LOGS = {
    HeroActivity.Elsewhere: None,
    HeroActivity.CommonPool: "{hero} is hanging out in the town square.",
    HeroActivity.VisitingTavern: "{hero} is visiting {tavern}.",
    HeroActivity.Hired: "{hero} was hired by {employer}.",
    HeroActivity.Adventuring: "{hero} has started adventuring at {dungeon}.",
    HeroActivity.Dead: "{hero} has died? Really? I didn't think we did that yet.",  # TODO
}


@db.needs_session
def make_start_activity_log(hero, s=None):
    text = START_LOGS[hero.activity]
    if text:
        return TavernLog(text=text.format(hero=hero, tavern=hero.visiting,
                                          patron=hero.patron, employer=hero.employer,
                                          dungeon=pool_controller.get_dungeon(hero, s=s)),
                         time=datetime.now())


@db.needs_session
def make_fight_log(hero, monster, s=None):
    return TavernLog(text="{hero} gets ready to fight a {monster}, but unfortunately that isn't possible yet.".format(hero=hero, monster=monster),
                     time=datetime.now())


@db.needs_session
def get_unsent(s=None):
    return s.query(TavernLog).filter(TavernLog.sent == False).order_by(TavernLog.time).all()


@db.needs_session
def mark_all_sent(s=None):
    return s.query(TavernLog).update({TavernLog.sent: True})
