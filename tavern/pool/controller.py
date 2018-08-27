import random

import ircbot.storage as db

from tavern.tavern_models import Tavern, TavernHero, HeroActivity
from tavern.util.names import SHAKESPEARE_NAMES


@db.needs_session
def print_debug(s=None):
    for hero in s.query(TavernHero).all():
        print("There is a hero {} that is {}".format(hero.info_string(), hero.activity))


@db.atomic
def generate_hero(name=None, stat_points=None, s=None):
    if not name:
        print(set(s.query(TavernHero).values(TavernHero.name)))
        name = random.choice(list(set(SHAKESPEARE_NAMES) -
                                  {name[0] for name in s.query(TavernHero).values(TavernHero.name)}))
    if not stat_points:
        stat_points = random.randint(4, 9)
    stats = [0, 0, 0]
    for i in range(stat_points):
        stats[random.randint(0, 2)] += random.choice([-1, 1])
    hero = TavernHero(name=name, anger=stats[0], reason=stats[1], charm=stats[2], activity=HeroActivity.Elsewhere)
    s.add(hero)
    return hero


@db.atomic
def find_hero(heroId=None, name=None, patron=None, s=None):
    if heroId:
        return s.query(TavernHero).filter(TavernHero.id == heroId).first()
    elif name:
        return s.query(TavernHero).filter(TavernHero.name == name).first()
    elif patron:
        s.add(patron)
        return s.query(TavernHero).filter(TavernHero.patron.id == patron.id).first()
