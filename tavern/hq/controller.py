from datetime import datetime
import random

import ircbot.storage as db

from tavern.tavern_models import Tavern, TavernHero
from arcuser.arcuser_models import ArcUser
from tavern.util.names import SHAKESPEARE_NAMES

STARTING_MONEY = 100

@db.atomic
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
    name = random.choice(SHAKESPEARE_NAMES)
    stats = [0, 0, 0]
    for i in range(random.randint(4,9)):
        stats[random.randint(0, 2)] += random.choice([-1, 1])
    tavern.resident_hero = TavernHero(name=name, anger=stats[0], reason=stats[1], charm=stats[2])
    return tavern.resident_hero

@db.atomic
def find_heroes(tavern, s=None):
    s.add(tavern)
    resident_hero = tavern.resident_hero
    return [resident_hero]
    # @TODO: return hired heroes too
