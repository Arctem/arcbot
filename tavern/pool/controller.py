import random

import ircbot.storage as db

from tavern.tavern_models import Tavern, TavernHero
from tavern.util.names import SHAKESPEARE_NAMES


@db.atomic
def generate_hero(name=None, stat_points=None, s=None):
    if not name:
        name = random.choice(SHAKESPEARE_NAMES)
    if not stat_points:
        stat_points = random.randint(4, 9)
    stats = [0, 0, 0]
    for i in range(stat_points):
        stats[random.randint(0, 2)] += random.choice([-1, 1])
    return TavernHero(name=name, anger=stats[0], reason=stats[1], charm=stats[2])


@db.atomic
def find_hero(heroId=None, name=None, patron=None, s=None):
    if heroId:
        return s.query(TavernHero).filter(TavernHero.id == heroId).first()
    elif name:
        return s.query(TavernHero).filter(TavernHero.name == name).first()
    elif patron:
        s.add(patron)
        return s.query(TavernHero).filter(TavernHero.patron.id == patron.id).first()
