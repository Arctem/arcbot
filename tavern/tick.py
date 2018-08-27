import ircbot.storage as db

import tavern.dungeon.tasks as dungeon
import tavern.pool.tasks as pool


@db.atomic
def tick(s=None):
    dungeon.dungeon_tick(s=s)
    pool.pool_tick(s=s)
    return True
