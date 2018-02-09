from datetime import datetime
import random
import string

import ircbot.storage as db

from arcuser.arcuser_models import ArcUser

from tavern.shared import TavernException
from tavern.tavern_models import TavernDungeon, TavernFloor, TavernMonster
import tavern.logs as logs

# Soft max, beaten by MIN_KNOWN_DUNGEONS
MAX_ACTIVE_DUNGEONS = 5

MIN_KNOWN_DUNGEONS = 1


@db.atomic
def dungeon_tick(s=None):
    insure_dungeon_count(s=s)


@db.atomic
def insure_dungeon_count(s=None):
    known = s.query(TavernDungeon).filter(TavernDungeon.secret == True).count()
    for i in range(MIN_KNOWN_DUNGEONS - known):
        dungeon = create_new_dungeon(s=s)
        discover_dungeon(dungeon, s=s)


@db.atomic
def create_new_dungeon(s=None):
    dungeon = TavernDungeon(
        name="".join([random.choice(string.ascii_letters) for i in range(random.randint(6, 12))]),
        secret=True,
        active=True,
    )
    for i in range(random.randint(5, 20)):
        s.add(TavernFloor(dungeon=dungeon, number=i))
    s.add(dungeon)
    return dungeon


@db.atomic
def discover_dungeon(dungeon, s=None):
    if not dungeon.secret:
        raise DungeonNotSecretException(dungeon)

    dungeon.secret = True
    s.add(logs.make_discovery_log(dungeon))
    return dungeon


class DungeonNotSecretException(TavernException):

    def __init__(self, dungeon, *args, **kwargs):
        TavernException.__init__(self, "Dungeon {} is not secret.".format(dungeon))
