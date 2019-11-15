import random
from datetime import datetime

from sqlalchemy.sql.expression import func

import ircbot.storage as db
import tavern.pool as pool
from arcuser.arcuser_models import ArcUser
from tavern import logs
from tavern.tavern_models import Tavern

STARTING_MONEY = 100


@db.needs_session
def find_tavern(owner, s=None):
    return s.query(Tavern).filter(Tavern.owner == owner).first()


@db.needs_session
def get_taverns(s=None):
    return s.query(Tavern).all()


@db.needs_session
def count_taverns(s=None):
    return s.query(Tavern).count()


@db.needs_session
def search_taverns(name, s=None):
    return s.query(Tavern).filter(Tavern.name.like('%{}%'.format(name))).all()


@db.needs_session
def name_tavern(owner, name, s=None):
    s.add(owner)
    tavern = find_tavern(owner, s=s)
    if not tavern:
        tavern = Tavern(owner=owner, creation_time=datetime.now(), name=name, money=STARTING_MONEY)
        s.add(tavern)
    else:
        tavern.name = name
    return tavern


@db.needs_session
def create_resident_hero(tavern, s=None):
    s.add(tavern)
    tavern.resident_hero = pool.controller.generate_hero(s=s)
    return tavern.resident_hero


@db.needs_session
def find_heroes(tavern, s=None):
    s.add(tavern)
    resident_hero = tavern.resident_hero
    return [resident_hero]
    # TODO: return hired heroes too


@db.needs_session
def tavern_details(tavern, s=None):
    info = []
    info.append('{name} is owned by {owner} and was founded on {creation_time:%d %B, %Y}.'.format(
        name=tavern.name, owner=tavern.owner, creation_time=tavern.creation_time))
    info.append('{gold} gold'.format(gold=tavern.money))
    if tavern.resident_hero is not None:
        info.append('Resident hero is {hero}.'.format(hero=tavern.resident_hero.name))
    if len(tavern.visiting_heroes) == 1:
        info.append('{} is visiting.'.format(tavern.visiting_heroes[0].name))
    elif len(tavern.visiting_heroes) > 1:
        info.append('{} are visiting.'.format(', '.format(tavern.visiting_heroes)))
    return info


@db.needs_session
def give_money(tavern, money, s=None):
    tavern.money += money
    s.add(logs.tavern_got_money(tavern, money))


@db.needs_session
def distribute_dead_hero_money(hero, s=None):
    money_per_tavern = int(hero.money / count_taverns(s=s))
    hero.money -= money_per_tavern * count_taverns(s=s)
    for tavern in get_taverns(s=s):
        give_money(tavern, money_per_tavern, s=s)
    s.add(logs.dead_hero_money_distributed(hero, money_per_tavern))
