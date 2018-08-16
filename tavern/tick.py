import ircbot.storage as db

import tavern.dungeon_tasks as dungeon
# import tavern.town_tasks as town


@db.atomic
def tick(s=None):
    dungeon.dungeon_tick(s=s)
    return True
