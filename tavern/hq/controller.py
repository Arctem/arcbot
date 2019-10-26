from datetime import datetime
import random

from sqlalchemy.sql.expression import func

import ircbot.storage as db

import tavern.pool.controller as pool_controller

from tavern.tavern_models import Tavern
from arcuser.arcuser_models import ArcUser
import tavern.pool.controller as pool_controller


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
    tavern.resident_hero = pool_controller.generate_hero(s=s)
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
