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

MONSTERS_PER_FLOOR = 10
MONSTER_NO_MOD_CHANCE = 0.3
MONSTER_SORT_VARIATION = 0.5


@db.needs_session
def print_debug(s=None):
    for dungeon in s.query(TavernDungeon).all():
        print("There is a dungeon called {} that is {}".format(
            dungeon.name, ", ".join(map(lambda t: t.name, dungeon.traits))))
        for floor in dungeon.floors:
            print("{}: {}".format(floor, ", ".join(map(str, floor.monsters))))

##################
# Dungeon Creation
##################


@db.atomic
def create_new_dungeon(floors, s=None):
    dungeon = TavernDungeon(
        secret=True,
        active=True,
    )
    types = random.sample(dungeon_raws.types.keys(), random.randint(2, 3))
    for t in types:
        s.add(TavernDungeonTrait(name=t, dungeon=dungeon))
    dungeon.name = create_name(types)

    for i in range(floors):
        s.add(TavernFloor(dungeon=dungeon, number=i))
    s.add(dungeon)
    return dungeon


def create_name(dungeon_traits):
    dungeon_traits = set(map(lambda trait: dungeon_raws.types[trait], dungeon_traits))
    base = random.choice(tuple(filter(lambda t: len(t.nouns) > 0, dungeon_traits)))
    dungeon_traits.remove(base)
    epithet = None
    epithet_options = set(filter(lambda t: len(t.epithets) > 0, dungeon_traits))
    if len(epithet_options) > 0 and (len(dungeon_traits) > 1 or random.randint(1, 2) is 1):
        epithet = random.choice(tuple(epithet_options))
        dungeon_traits.remove(epithet)

    name = random.choice(tuple(base.nouns))
    if epithet:
        name = name + " of " + random.choice(tuple(epithet.epithets))
    if len(dungeon_traits) > 0:
        random.shuffle(dungeon_traits)
        adjectives = map(lambda t: random.choice(tuple(t.adjectives)), dungeon_traits)
        adjectives = ", ".join(adjectives)
        name = adjectives + " " + name
    name = "The " + name
    return inflection.titleize(name)


####################
# Dungeon Management
####################


@db.atomic
def discover_dungeon(dungeon, s=None):
    if not dungeon.secret:
        raise DungeonNotSecretException(dungeon)

    dungeon.secret = True
    s.add(logs.make_discovery_log(dungeon))
    return dungeon


@db.atomic
def populate_dungeon(dungeon, s=None):
    traits = map(lambda t: dungeon_raws.types[t.name], dungeon.traits)
    required = set()
    optional = set()
    for trait in traits:
        required |= trait.monster_reqs
        optional |= trait.monster_opts
    optional |= required

    options = monster_raws.get_monster_options(required, optional)

    num_monsters = len(dungeon.floors) * MONSTERS_PER_FLOOR
    monsters = generate_monsters(num_monsters, options)
    monsters.sort(key=monster_rank_func(MONSTER_SORT_VARIATION))

    print(dungeon.floors)
    for floor in range(len(dungeon.floors)):
        dungeon.floors[floor].monsters = monsters[floor * MONSTERS_PER_FLOOR:(floor + 1) * MONSTERS_PER_FLOOR]


####################
# Monster Management
####################

def generate_monsters(num_monsters, options, s=None):
    monsters = []
    for i in range(num_monsters):
        stock, modifier = None, None
        if random.random() < MONSTER_NO_MOD_CHANCE:
            # Only a stock
            stock = random.choice(tuple(options['required_stocks']))
        else:
            req = random.choice(tuple(options['required']))
            if req in options['modifiers']:
                modifier = req
                stock = random.choice(tuple(options['stocks']))
            else:
                stock = req
                modifier = random.choice(tuple(options['modifiers']))
            modifier = modifier.name
        level = random.randint(stock.min_level, stock.max_level)
        stock = stock.name

        monsters.append(TavernMonster(level=level, stock=stock, modifier=modifier))
    return monsters


def monster_rank_func(variation=0):
    def ranking_func(monster):
        level = monster_level(monster)
        level *= random.uniform(1 - variation, 1 + variation)
        return level
    return ranking_func


def monster_level(monster):
    level = monster.level
    level += len(monster_raws.stocks[monster.stock].strengths)
    level -= len(monster_raws.stocks[monster.stock].weaknesses)
    if monster.modifier:
        level += monster_raws.modifiers[monster.modifier].level
        level += len(monster_raws.modifiers[monster.modifier].strengths)
        level -= len(monster_raws.modifiers[monster.modifier].weaknesses)
    return level


class DungeonNotSecretException(TavernException):

    def __init__(self, dungeon, *args, **kwargs):
        TavernException.__init__(self, "Dungeon {} is not secret.".format(dungeon))