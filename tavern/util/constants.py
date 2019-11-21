TICK_LENGTH = 60 * 30  # 30 minutes


HEROES_MAX_ACTIVE = 20  # Soft max of heroes alive, beaten by HEROES_MIN and HEROES_MIN_IDLE
HEROES_MIN_ALIVE = 10  # Minimum amount of heroes alive.
HEROES_MIN_IDLE = 7  # Minimum amount of heroes either Elsewhere or CommonPool.
HERO_START_MONEY = 5

MONEY_GAINED_TO_HERO_COST = 0.2  # 20% of money made on an adventure goes to a hero's cost
HERO_START_COST = 10
HERO_MIN_COST = 5
HERO_COST_HIRE_BUMP = 5
HERO_COST_DEGRADE_RATE = 0.2

POOL_RESET_FREQUENCY = int(6 * 3600 / TICK_LENGTH)  # once every 6 hours, reset the pool
POOL_SIZE = 5

HERO_HEAL_CHANCE = 0.02  # 2% chance to heal per tick
RESIDENT_HERO_HEAL_CHANCE = 0.05  # resident heroes can heal faster so players can have regular use of them
HERO_BAR_TAB = 5

DUNGEONS_MAX_ACTIVE = 10  # Soft max, beaten by DUNGEONS_MIN_KNOWN
DUNGEONS_MIN_KNOWN = 5
DUNGEONS_MIN_FLOORS = 5
DUNGEONS_MAX_FLOORS = 10
DUNGEON_EMPTY_THRESHHOLD = 0.5  # Hide a dungeon if half floors are empty.

MONSTERS_PER_FLOOR = 10
MONSTER_NO_MOD_CHANCE = 0.3
MONSTER_SORT_VARIATION = 0.5
