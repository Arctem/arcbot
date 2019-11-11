import random

import ircbot.storage as db

from tavern import logs
import tavern.adventure.controller as adventure_controller
import tavern.pool.controller as pool_controller
from tavern.tavern_models import Tavern, TavernAdventure, TavernDungeon, TavernHero, HeroActivity


@db.needs_session
def adventure_tick(tick, s=None):
    process_active_adventures(s=s)


@db.needs_session
def process_active_adventures(s=None):
    for adventure in s.query(TavernAdventure).filter(TavernAdventure.active == True).all():
        floor = adventure.floor
        if len(floor.monsters) is 0:
            pass  # advance to next floor
            return
        enemy = random.choice(floor.monsters)
        s.add(logs.make_fight_log(adventure.hero, enemy))
