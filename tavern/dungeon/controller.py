import random
import string
from datetime import datetime

import inflection

import ircbot.storage as db
import tavern.raws.dungeon as dungeon_raws
import tavern.raws.monster as monster_raws
from arcuser.arcuser_models import ArcUser
from tavern import logs
from tavern.shared import TavernException
from tavern.tavern_models import (TavernAdventure, TavernDungeon,
                                  TavernDungeonTrait, TavernFloor,
                                  TavernMonster)
from tavern.util import constants


@db.needs_session
def print_debug(s=None):
    for dungeon in s.query(TavernDungeon).all():
        print("There is a dungeon called {} that is {}".format(
            dungeon.name, ", ".join(map(lambda t: t.name, dungeon.traits))))
        for floor in dungeon.floors:
            print("{}: {}".format(floor, ", ".join(map(str, floor.monsters))))

##################
# User Interaction
##################


@db.needs_session
def get_dungeons(s=None):
    return s.query(TavernDungeon).all()


@db.needs_session
def get_known_dungeons(s=None):
    return s.query(TavernDungeon).filter(TavernDungeon.active == True, TavernDungeon.secret == False).all()


@db.needs_session
def search_dungeons(name, s=None):
    exact = s.query(TavernDungeon).filter(TavernDungeon.name == name).one_or_none()
    if exact:
        return [exact]  # return as list to match the normal interface
    return s.query(TavernDungeon).filter(TavernDungeon.name.like('%{}%'.format(name))).all()


@db.needs_session
def get_heroes_in_dungeon(dungeon, s=None):
    return s.query(TavernAdventure).filter(TavernAdventure.dungeon == dungeon, TavernAdventure.active == True).count()


@db.needs_session
def get_floor(dungeon_id, floor_num, s=None):
    return s.query(TavernFloor).filter(TavernFloor.dungeon_id == dungeon_id, TavernFloor.number == floor_num).one_or_none()


@db.needs_session
def dungeon_details(dungeon, s=None):
    info = []
    info.append('{} has {} floors.'.format(dungeon.name, len(dungeon.floors)))
    info.append('It is currently active.' if dungeon.active else 'It is not currently active.')
    heroes = []
    for adventure in filter(lambda adv: adv.active, dungeon.adventures):
        heroes.append(adventure.hero)
    if len(heroes) > 0:
        info.append('{} are currently here.'.format(', '.join(map(str, heroes))))
    info.append('It has been visited {} times.'.format(len(dungeon.adventures)))
    return info


##################
# Dungeon Creation
##################


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

def complete_dungeon(dungeon, s=None):
    if not dungeon.active:
        return DungeonNotActiveException(dungeon)

    dungeon.active = False
    s.add(logs.dungeon_cleared(dungeon))
    depopulate_dungeon(dungeon, s=s)


def discover_dungeon(dungeon, s=None):
    if not dungeon.secret:
        raise DungeonNotSecretException(dungeon)

    dungeon.secret = False
    s.add(logs.dungeon_discovered(dungeon))
    return dungeon


def hide_dungeon(dungeon, s=None):
    if dungeon.secret:
        raise DungeonSecretException(dungeon)
    dungeon.secret = True
    s.add(logs.dungeon_hidden(dungeon))
    return dungeon


def populate_dungeon(dungeon):
    traits = map(lambda t: dungeon_raws.types[t.name], dungeon.traits)
    required = set()
    optional = set()
    for trait in traits:
        required |= trait.monster_reqs
        optional |= trait.monster_opts
    optional |= required

    options = monster_raws.get_monster_options(required, optional)

    num_monsters = len(dungeon.floors) * constants.MONSTERS_PER_FLOOR
    monsters = generate_monsters(num_monsters, options)
    monsters.sort(key=monster_rank_func(constants.MONSTER_SORT_VARIATION))

    print(dungeon.floors)
    for floor in range(len(dungeon.floors)):
        dungeon.floors[floor].monsters = monsters[
            floor * constants.MONSTERS_PER_FLOOR:(floor + 1) * constants.MONSTERS_PER_FLOOR]


def depopulate_dungeon(dungeon, s=None):
    for floor in dungeon.floors:
        for monster in floor.monsters:
            s.delete(monster)

####################
# Monster Management
####################


def kill_monster(monster, s=None):
    s.delete(monster)


def monster_gold(monster, s=None):
    return max(1, monster_effective_level(monster))


def generate_monsters(num_monsters, options):
    monsters = []
    for i in range(num_monsters):
        stock, modifier = None, None
        if random.random() < constants.MONSTER_NO_MOD_CHANCE:
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
        level = monster_effective_level(monster)
        level *= random.uniform(1 - variation, 1 + variation)
        return level
    return ranking_func


def monster_level(monster):
    level = monster.level
    if monster.modifier:
        level += monster_raws.modifiers[monster.modifier].level
    return level


def monster_effective_level(monster):
    level = monster.level
    level += len(monster_raws.stocks[monster.stock].strengths)
    level -= len(monster_raws.stocks[monster.stock].weaknesses)
    if monster.modifier:
        level += monster_raws.modifiers[monster.modifier].level
        level += len(monster_raws.modifiers[monster.modifier].strengths)
        level -= len(monster_raws.modifiers[monster.modifier].weaknesses)
    return level


class DungeonActiveException(TavernException):

    def __init__(self, dungeon, *args, **kwargs):
        TavernException.__init__(self, "Dungeon {} is active.".format(dungeon))


class DungeonNotActiveException(TavernException):

    def __init__(self, dungeon, *args, **kwargs):
        TavernException.__init__(self, "Dungeon {} is not active.".format(dungeon))


class DungeonSecretException(TavernException):

    def __init__(self, dungeon, *args, **kwargs):
        TavernException.__init__(self, "Dungeon {} is secret.".format(dungeon))


class DungeonNotSecretException(TavernException):

    def __init__(self, dungeon, *args, **kwargs):
        TavernException.__init__(self, "Dungeon {} is not secret.".format(dungeon))
