from datetime import datetime
import random
import string

import inflection

import ircbot.storage as db

from arcuser.arcuser_models import ArcUser

from tavern.shared import TavernException
from tavern.tavern_models import TavernDungeon, TavernDungeonTrait, TavernFloor, TavernMonster
from tavern import logs
import tavern.raws.dungeon as dungeon_raws
import tavern.raws.monster as monster_raws
import tavern.dungeon.controller as dungeon_controller


DUNGEONS_MAX_ACTIVE = 10  # Soft max, beaten by DUNGEONS_MIN_KNOWN
DUNGEONS_MIN_KNOWN = 5
DUNGEONS_MIN_FLOORS = 5
DUNGEONS_MAX_FLOORS = 10


@db.atomic
def dungeon_tick(s=None):
    if ensure_dungeon_count(s=s) > 0:
        dungeon_controller.print_debug(s=s)


@db.atomic
def ensure_dungeon_count(s=None):
    known = s.query(TavernDungeon).filter(TavernDungeon.secret == True).count()
    for i in range(DUNGEONS_MIN_KNOWN - known):
        dungeon = dungeon_controller.create_new_dungeon(random.randint(DUNGEONS_MIN_FLOORS, DUNGEONS_MAX_FLOORS), s=s)
        dungeon_controller.discover_dungeon(dungeon, s=s)
        dungeon_controller.populate_dungeon(dungeon, s=s)
    return DUNGEONS_MIN_KNOWN - known
