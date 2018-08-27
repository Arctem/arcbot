from datetime import datetime
import random
import string

import inflection

import ircbot.storage as db

from arcuser.arcuser_models import ArcUser

from tavern.shared import TavernException
from tavern.tavern_models import HeroActivity, TavernHero
from tavern import logs
import tavern.pool.controller as pool_controller

HEROES_MAX_ACTIVE = 20  # Soft max of heroes alive, beaten by HEROES_MIN and HEROES_MIN_IDLE
HEROES_MIN_ALIVE = 10  # Minimum amount of heroes alive.
HEROES_MIN_IDLE = 4  # Minimum amount of heroes either Elsewhere or CommonPool.


@db.atomic
def pool_tick(s=None):
    if ensure_hero_count(s=s) > 0:
        pool_controller.print_debug(s=s)


@db.atomic
def ensure_hero_count(s=None):
    created = 0
    alive = s.query(TavernHero).filter(TavernHero.activity != HeroActivity.Dead).count()
    for i in range(HEROES_MIN_ALIVE - alive):
        hero = pool_controller.generate_hero(s=s)
        created += 1
        s.add(logs.make_arrival_log(hero))
    return created
