from datetime import datetime
import random
import string

import inflection

import ircbot.storage as db

from arcuser.arcuser_models import ArcUser

from tavern.shared import TavernException
from tavern.tavern_models import TavernDungeon, TavernDungeonTrait, TavernFloor, TavernMonster
from tavern.util import constants
from tavern import logs
import tavern.raws.dungeon as dungeon_raws
import tavern.raws.monster as monster_raws
import tavern.dungeon.controller as dungeon_controller


@db.needs_session
def dungeon_tick(tick, s=None):
    if ensure_dungeon_count(s=s) > 0:
        dungeon_controller.print_debug(s=s)


@db.needs_session
def ensure_dungeon_count(s=None):
    created = 0
    known = s.query(TavernDungeon).filter(TavernDungeon.secret == False).count()
    for i in range(constants.DUNGEONS_MIN_KNOWN - known):
        dungeon = dungeon_controller.create_new_dungeon(random.randint(
            constants.DUNGEONS_MIN_FLOORS, constants.DUNGEONS_MAX_FLOORS), s=s)
        created += 1
        dungeon_controller.discover_dungeon(dungeon, s=s)
        dungeon_controller.populate_dungeon(dungeon, s=s)
    return created
