import random
import string
from datetime import datetime

import inflection

import ircbot.storage as db
import tavern.dungeon.controller as dungeon_controller
import tavern.raws.dungeon as dungeon_raws
import tavern.raws.monster as monster_raws
from arcuser.arcuser_models import ArcUser
from tavern import logs
from tavern.shared import TavernException
from tavern.tavern_models import (TavernDungeon, TavernDungeonTrait,
                                  TavernFloor, TavernMonster)
from tavern.util import constants


def dungeon_tick(tick, s=None):
    hide_emptied_dungeons(s=s)
    if ensure_dungeon_count(s=s) > 0:
        dungeon_controller.print_debug(s=s)


def hide_emptied_dungeons(s=None):
    for dungeon in dungeon_controller.get_known_dungeons(s=s):
        empty_floors = len(list(filter(lambda f: len(f.monsters) == 0, dungeon.floors)))
        if empty_floors / len(dungeon.floors) > constants.DUNGEON_EMPTY_THRESHHOLD:
            dungeon_controller.hide_dungeon(dungeon, s=s)


def ensure_dungeon_count(s=None):
    created = 0
    known = s.query(TavernDungeon).filter(TavernDungeon.secret == False,
                                          TavernDungeon.active == True).count()
    for i in range(constants.DUNGEONS_MIN_KNOWN - known):
        dungeon = dungeon_controller.create_new_dungeon(random.randint(
            constants.DUNGEONS_MIN_FLOORS, constants.DUNGEONS_MAX_FLOORS), s=s)
        created += 1
        dungeon_controller.discover_dungeon(dungeon, s=s)
        dungeon_controller.populate_dungeon(dungeon)
    return created
