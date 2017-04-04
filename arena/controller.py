import random

import ircbot.storage as db

import phrase_maker.phrase_maker as phrase_maker

from arena.models import ArenaObject, ArenaAttribute
from arena.raws import raws


@db.atomic
def create_hero(arcuser, s=None):
    s.add(arcuser)
    race = random.choice(raws.races)
    hero = ArenaObject(name=phrase_maker.make('name'), employer=arcuser)
    s.add(hero)
    hero.race = race
    return hero


@db.needs_session
def get_hero(s=None):
    return s.query(ArenaObject).first()
