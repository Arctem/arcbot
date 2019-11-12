# TICK_LENGTH = 60 * 5  # 5 minutes
TICK_LENGTH = 60 * 30  # 30 minutes


HEROES_MAX_ACTIVE = 20  # Soft max of heroes alive, beaten by HEROES_MIN and HEROES_MIN_IDLE
HEROES_MIN_ALIVE = 5  # Minimum amount of heroes alive.
HEROES_MIN_IDLE = 4  # Minimum amount of heroes either Elsewhere or CommonPool.

# POOL_RESET_FREQUENCY = int(24 * 3600 / TICK_LENGTH)  # once a day, reset the pool
POOL_RESET_FREQUENCY = int(12 * 3600 / TICK_LENGTH)  # once every 12 hours, reset the pool
POOL_SIZE = 3

HERO_HEAL_CHANCE = 0.05  # 5% chance to heal per tick


DUNGEONS_MAX_ACTIVE = 10  # Soft max, beaten by DUNGEONS_MIN_KNOWN
DUNGEONS_MIN_KNOWN = 5
DUNGEONS_MIN_FLOORS = 5
DUNGEONS_MAX_FLOORS = 10
