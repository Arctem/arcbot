import ircbot.storage as db

from tavern.tavern_models import TavernValue
import tavern.adventure.tasks as adventure
import tavern.dungeon.tasks as dungeon
import tavern.pool.tasks as pool

TICK = 'tick'


@db.needs_session
def increment_tick(s=None):
    tick = s.query(TavernValue).filter(TavernValue.key == TICK).one_or_none()
    if not tick:
        tick = TavernValue(key=TICK, value=0)
        s.add(tick)
    else:
        tick.value = int(tick.value) + 1
    return int(tick.value)


@db.needs_session
def tick(s=None):
    tick = increment_tick(s=s)
    print("Starting tick {}".format(tick))
    adventure.adventure_tick(tick, s=s)
    dungeon.dungeon_tick(tick, s=s)
    pool.pool_tick(tick, s=s)
    return True
