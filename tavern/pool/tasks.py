from datetime import datetime
import random
import string

import inflection

import ircbot.storage as db

from arcuser.arcuser_models import ArcUser

from tavern.shared import TavernException
from tavern.tavern_models import HeroActivity, TavernHero
from tavern.util import constants
from tavern import logs
import tavern.hq.controller as hq_controller
import tavern.pool.controller as pool_controller

HEROES_MAX_ACTIVE = 20  # Soft max of heroes alive, beaten by HEROES_MIN and HEROES_MIN_IDLE
HEROES_MIN_ALIVE = 5  # Minimum amount of heroes alive.
HEROES_MIN_IDLE = 4  # Minimum amount of heroes either Elsewhere or CommonPool.

# POOL_RESET_FREQUENCY = int(24 * 3600 / constants.TICK_LENGTH)  # once a day, reset the pool
POOL_RESET_FREQUENCY = int(2 * 3600 / constants.TICK_LENGTH)  # once every 2 hours, reset the pool
POOL_SIZE = 3


@db.atomic
def pool_tick(tick, s=None):
    if ensure_hero_count(s=s) > 0:
        pool_controller.print_debug(s=s)
    if time_to_reset_pool(tick, s=s):
        reset_pool(s=s)


@db.atomic
def ensure_hero_count(s=None):
    alive = s.query(TavernHero).filter(TavernHero.activity != HeroActivity.Dead).count()
    idle = s.query(TavernHero).filter(TavernHero.activity.in_(
        [HeroActivity.CommonPool, HeroActivity.Elsewhere])).count()
    to_create = max(HEROES_MIN_ALIVE - alive, HEROES_MIN_IDLE - idle, hq_controller.count_taverns(s=s) - idle)

    created = 0
    for i in range(to_create):
        hero = pool_controller.generate_hero(s=s)
        created += 1
        s.add(logs.make_arrival_log(hero))
    return created


@db.needs_session
def time_to_reset_pool(tick, s=None):
    return tick % POOL_RESET_FREQUENCY == 0


@db.atomic
def reset_pool(s=None):
    available = set(s.query(TavernHero).filter(TavernHero.activity.in_([
        HeroActivity.VisitingTavern, HeroActivity.CommonPool, HeroActivity.Elsewhere
    ])).all())
    taverns = hq_controller.get_taverns(s=s)

    # Divide heroes into three groups: those visiting taverns, those in the pool, and those elsewhere.
    visitors = random.sample(available, len(taverns))
    available = available - set(visitors)
    pool_heroes = random.sample(available, min(POOL_SIZE, len(available)))
    available = available - set(pool_heroes)

    random.shuffle(taverns)
    for hero, tavern in zip(visitors, taverns):
        pool_controller.change_hero_activity(hero, HeroActivity.VisitingTavern, tavern=tavern, s=s)

    for hero in pool_heroes:
        pool_controller.change_hero_activity(hero, HeroActivity.CommonPool, s=s)

    for hero in available:
        pool_controller.change_hero_activity(hero, HeroActivity.Elsewhere, s=s)
