import random

import ircbot.storage as db
import tavern.hq.controller as hq_controller
import tavern.raws.job as job_raws
from tavern import logs
from tavern.shared import TavernException
from tavern.tavern_models import (HeroActivity, Tavern, TavernAdventure,
                                  TavernDungeon, TavernHero)
from tavern.util import constants
from tavern.util.names import SHAKESPEARE_NAMES


@db.needs_session
def print_debug(s=None):
    for hero in s.query(TavernHero).all():
        print("There is a hero {} that is {}".format(hero.info_string(), hero.activity))


@db.needs_session
def get_heroes(s=None):
    return s.query(TavernHero).all()


@db.needs_session
def find_hero(heroId=None, name=None, patron=None, s=None):
    if heroId:
        return s.query(TavernHero).filter(TavernHero.id == heroId).first()
    elif name:
        return s.query(TavernHero).filter(TavernHero.name == name).first()
    elif patron:
        s.add(patron)
        return s.query(TavernHero).filter(TavernHero.patron.id == patron.id).first()


@db.needs_session
def get_dungeon(hero=None, s=None):
    adventure = s.query(TavernAdventure).filter(TavernAdventure.hero ==
                                                hero, TavernAdventure.active == True).one_or_none()
    if adventure:
        return adventure.dungeon


@db.needs_session
def search_heroes(name, s=None):
    return s.query(TavernHero).filter(TavernHero.name.like('%{}%'.format(name))).all()


@db.needs_session
def generate_hero(name=None, stat_points=None, s=None):
    if not name:
        print(set(s.query(TavernHero).values(TavernHero.name)))
        name = random.choice(list(set(SHAKESPEARE_NAMES) -
                                  {name[0] for name in s.query(TavernHero).values(TavernHero.name)}))
    primary, secondary = random.sample(job_raws.jobs.keys(), 2)
    epithet = create_epithet(primary, secondary)
    hero = TavernHero(name=name, epithet=epithet, level=1,
                      cost=constants.HERO_START_COST, money=constants.HERO_START_MONEY,
                      activity=HeroActivity.Elsewhere,
                      primary_class=primary, secondary_class=secondary)
    s.add(hero)
    return hero


def create_epithet(primary, secondary):
    return '{} {}'.format(random.choice(tuple(job_raws.jobs[secondary].adjectives)).capitalize(),
                          random.choice(tuple(job_raws.jobs[primary].nouns)).capitalize())


@db.needs_session
def hire_hero(tavern_id, hero_id, cost, s=None):
    # check current state and change
    tavern = s.query(Tavern).filter(Tavern.id == tavern_id).first()
    hero = find_hero(heroId=hero_id, s=s)
    change_hero_activity(hero, HeroActivity.Hired, tavern, s=s)
    tavern.money -= cost
    hero.money += cost
    increase_cost(hero, constants.HERO_COST_HIRE_BUMP)


@db.needs_session
def change_hero_activity(hero, activity, tavern=None, s=None):
    if bool(tavern) != (activity in (HeroActivity.VisitingTavern, HeroActivity.Hired)):
        raise TavernException(
            "Invalid activity change: Activity {} and Tavern {} both provided.".format(activity, tavern))

    if activity == hero.activity and (activity != HeroActivity.VisitingTavern or hero.visiting == tavern):
        return

    hero.activity = activity
    hero.visiting = None
    if hero.employer is not None:
        hero.employer.hire_hero = None
        hero.employer = None
    if activity == HeroActivity.VisitingTavern:
        hero.visiting = tavern
    if activity == HeroActivity.Hired:
        tavern.hired_hero = hero


@db.needs_session
def pay_tab(hero, s=None):
    if hero.activity != HeroActivity.VisitingTavern or hero.visiting is None:
        raise TavernException("Hero {} not at Tavern.".format(hero))
    if hero.money >= constants.HERO_BAR_TAB:
        hero.money -= constants.HERO_BAR_TAB
        hero.visiting.money += constants.HERO_BAR_TAB
        s.add(logs.hero_paid_tab(hero, constants.HERO_BAR_TAB, hero.visiting.owner))
    elif hero.money > 0:
        s.add(logs.hero_short_on_tab(hero, constants.HERO_BAR_TAB, hero.money, hero.visiting.owner))
        hero.visiting.money += hero.money
        hero.money = 0
    else:
        s.add(logs.hero_broke_tab(hero, hero.visiting.owner))


@db.needs_session
def injure_hero(hero, s=None):
    if hero.injured:
        raise TavernException("Hero {} already injured.".format(hero))
    hero.injured = True


@db.needs_session
def heal_hero(hero, s=None):
    if not hero.injured:
        raise TavernException("Hero {} isn't injured.".format(hero))
    hero.injured = False
    s.add(logs.hero_healed(hero, s=s))


@db.needs_session
def kill_hero(hero, s=None):
    if not hero.alive:
        raise TavernException("Hero {} already dead.".format(hero))
    hero.alive = False
    change_hero_activity(hero, HeroActivity.Dead, s=s)
    hq_controller.distribute_dead_hero_money(hero, s=s)


@db.needs_session
def level_hero(hero, s=None):
    hero.level += 1
    s.add(logs.hero_leveled_up(hero, hero.level, s=s))


def increase_cost(hero, cost):
    cost = int(cost) + hero.cost
    hero.cost = max(cost, constants.HERO_MIN_COST)


def degrade_cost(hero):
    cost = hero.cost * (1 - constants.HERO_COST_DEGRADE_RATE)
    hero.cost = max(cost, constants.HERO_MIN_COST)


@db.needs_session
def hero_details(hero, s=None):
    info = []
    info.append('{name}{patron} is a {dead}{job}. They are {activity}.'
                .format(name=hero.name,
                        patron=" of {patron}".format(patron=hero.patron.name) if hero.patron else "",
                        dead="" if hero.alive else "dead ",
                        job=hero.level_string(),
                        activity=hero_activity_string(hero, s=s)))
    info.append('They have {money} gold and charge {cost} for their services.{injured} They have been on {adv_count} adventures.'
                .format(
                    money=hero.money,
                    cost=hero.cost,
                    injured=" They are injured." if hero.injured else "",
                    adv_count=len(hero.adventures)))
    return info


@db.needs_session
def hero_activity_string(hero, s=None):
    if hero.activity is HeroActivity.Elsewhere:
        return 'out of town'
    elif hero.activity is HeroActivity.CommonPool:
        return 'in the town square'
    elif hero.activity is HeroActivity.VisitingTavern:
        return 'visiting {tavern}'.format(tavern=hero.visiting)
    elif hero.activity is HeroActivity.Hired:
        return 'waiting for orders from {tavern}'.format(tavern=hero.employer)
    elif hero.activity is HeroActivity.Adventuring:
        for adventure in hero.adventures:
            if adventure.active:
                return 'on floor {floor} of {dungeon}'.format(floor=adventure.floor.number, dungeon=adventure.dungeon)
    elif hero.activity is HeroActivity.Dead:
        return 'dead as a doornail'
