from datetime import datetime
import random

from sqlalchemy.sql.expression import func

import ircbot.storage as db

from tavern.tavern_models import Tavern, TavernHero
from arcuser.arcuser_models import ArcUser

STARTING_MONEY = 100
NAMES = ['Bruce', 'Wendy', 'Samson']


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
def create_resident_hero(tavern, name, s=None):
    s.add(tavern)
    tavern.resident_hero = generate_hero(name=name, s=s)
    return tavern.resident_hero


@db.atomic
def generate_hero(name=None, stat_points=None, s=None):
    if not name:
        name = random.choice(NAMES)
    if not stat_points:
        stat_points = random.randint(4, 9)
    stats = [0, 0, 0]
    for i in range(stat_points):
        stats[random.randint(0, 2)] += random.choice([-1, 1])
    return TavernHero(name=name, anger=stats[0], reason=stats[1], charm=stats[2])
