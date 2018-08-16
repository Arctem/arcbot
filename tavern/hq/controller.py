from datetime import datetime
import random

from sqlalchemy.sql.expression import func

import ircbot.storage as db

import tavern.pool.controller as pool_controller

from tavern.tavern_models import Tavern
from arcuser.arcuser_models import ArcUser


STARTING_MONEY = 100


@db.needs_session
def find_tavern(owner, s=None):
    return s.query(Tavern).filter(Tavern.owner == owner).first()


@db.atomic
def name_tavern(owner, name, s=None):
    s.add(owner)
    tavern = find_tavern(owner, s=s)
    if not tavern:
        tavern = Tavern(owner=owner, creation_time=datetime.now(), name=name, money=STARTING_MONEY)
        s.add(tavern)
    else:
        tavern.name = name
    return tavern


@db.atomic
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
