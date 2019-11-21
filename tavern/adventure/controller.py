import ircbot.storage as db
import tavern.dungeon.controller as dungeon_controller
import tavern.pool.controller as pool_controller
from tavern import logs
from tavern.tavern_models import (HeroActivity, Tavern, TavernAdventure,
                                  TavernDungeon, TavernHero)
from tavern.util import constants

##################################
# Starting and Stopping Adventures
##################################


@db.needs_session
def start_adventure(hero_id, dungeon_id, hiring_tavern_id=None, s=None):
    hero = s.query(TavernHero).filter(TavernHero.id == hero_id).first()
    dungeon = s.query(TavernDungeon).filter(TavernDungeon.id == dungeon_id).first()
    tavern = None if hiring_tavern_id is None else s.query(Tavern).filter(Tavern.id == hiring_tavern_id).first()

    if not (hero.activity == HeroActivity.Hired and tavern is not None and hero.employer == tavern) and not (tavern is None and hero.activity == HeroActivity.Elsewhere):
        raise TavernException('Hero {} cannot start an adventure with tavern {} from state {}'.format(
            hero, tavern, hero.activity))
    if not dungeon.active:
        raise TavernException('Cannot send hero to adventure in inactive dungeon {}'.format(dungeon))

    adventure = TavernAdventure(hero=hero, dungeon=dungeon, employer=tavern,
                                floor=dungeon_controller.get_floor(dungeon.id, 0, s=s),
                                active=True, money_gained=0)
    s.add(adventure)
    pool_controller.change_hero_activity(hero, HeroActivity.Adventuring, s=s)
    s.add(logs.adventure_started(hero, dungeon, tavern))


@db.needs_session
def end_adventure(adventure, s=None):
    hero = adventure.hero
    dungeon = adventure.dungeon
    tavern = adventure.employer

    if not adventure.active:
        raise TavernException('Adventure {} is not active.'.format(adventure))
    tavern.money += adventure.money_gained
    hero.money += adventure.money_gained
    pool_controller.increase_cost(hero, adventure.money_gained * constants.MONEY_GAINED_TO_HERO_COST)
    adventure.active = False
    s.add(logs.adventure_ended(hero, dungeon, tavern, adventure.money_gained))


@db.needs_session
def fail_adventure(adventure, s=None):
    hero = adventure.hero
    dungeon = adventure.dungeon
    tavern = adventure.employer

    if not adventure.active:
        raise TavernException('Adventure {} is not active.'.format(adventure))
    adventure.active = False
    s.add(logs.adventure_failed(hero, dungeon, tavern, adventure.money_gained))


##########################
# Events During Adventures
##########################

@db.needs_session
def advance_floor(adventure, s=None):
    next_floor = dungeon_controller.get_floor(adventure.dungeon.id, adventure.floor.number + 1, s=s)
    if next_floor:
        adventure.floor = next_floor
        s.add(logs.adventure_reached_floor(adventure))
    else:
        end_adventure(adventure, s=s)
