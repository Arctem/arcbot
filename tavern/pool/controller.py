import random

import ircbot.storage as db

from tavern import logs
from tavern.shared import TavernException
from tavern.tavern_models import Tavern, TavernAdventure, TavernDungeon, TavernHero, HeroActivity
from tavern.util.names import SHAKESPEARE_NAMES
import tavern.raws.job as job_raws

START_COST = 10
START_MONEY = 10


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
                      cost=START_COST, money=START_MONEY,
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


@db.needs_session
def change_hero_activity(hero, activity, tavern=None, s=None):
    if bool(tavern) != (activity in (HeroActivity.VisitingTavern, HeroActivity.Hired)):
        raise TavernException(
            "Invalid activity change: Activity {} and Tavern {} both provided.".format(activity, tavern))

    if activity == hero.activity and (activity != HeroActivity.VisitingTavern or hero.visiting == tavern):
        return

    stop_log = logs.make_stop_activity_log(hero, s=s)
    if stop_log:
        s.add(stop_log)

    hero.activity = activity
    hero.visiting = None
    if hero.employer is not None:
        hero.employer.hire_hero = None
        hero.employer = None
    if activity == HeroActivity.VisitingTavern:
        hero.visiting = tavern
    if activity == HeroActivity.Hired:
        tavern.hired_hero = hero

    start_log = logs.make_start_activity_log(hero, s=s)
    if start_log:
        s.add(start_log)


@db.needs_session
def injure_hero(hero, s=None):
    if hero.injured:
        raise TavernException("Hero {} already injured.".format(hero))
    hero.injured = True


@db.needs_session
def kill_hero(hero, s=None):
    if not hero.alive:
        raise TavernException("Hero {} already dead.".format(hero))
    hero.alive = False


@db.needs_session
def hero_details(hero, s=None):
    info = []
    info.append(hero.name)
    if not hero.alive:
        info.append('Dead.')
    info.append(hero_activity_string(hero, s=s))
    info.append(hero.level_string())
    info.append('Has {money} and demands {cost} gold.'.format(money=hero.money, cost=hero.cost))
    if hero.patron:
        info.append('Patron of {patron}.'.format(patron=hero.patron.name))
    info.append('Has been on {adv_count} adventures.'.format(adv_count=len(hero.adventures)))
    return info


@db.needs_session
def hero_activity_string(hero, s=None):
    if hero.activity is HeroActivity.Elsewhere:
        return 'Is elsewhere.'
    elif hero.activity is HeroActivity.CommonPool:
        return 'Is hanging out at the town square'
    elif hero.activity is HeroActivity.VisitingTavern:
        return 'Is visiting {tavern}.'.format(tavern=hero.visiting)
    elif hero.activity is HeroActivity.Hired:
        return 'Has been hired by {tavern}.'.format(tavern=hero.employer)
    elif hero.activity is HeroActivity.Adventuring:
        for adventure in hero.adventures:
            if adventure.active:
                return 'Is on floor {floor} of {dungeon}.'.format(floor=adventure.floor.number, dungeon=adventure.dungeon)
    elif hero.activity is HeroActivity.Dead:
        return 'At the graveyard.'
