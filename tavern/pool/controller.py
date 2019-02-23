import random

import ircbot.storage as db

from tavern import logs
from tavern.shared import TavernException
from tavern.tavern_models import Tavern, TavernHero, HeroActivity
from tavern.util.names import SHAKESPEARE_NAMES
import tavern.raws.job as job_raws


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
def search_heroes(name, s=None):
    return s.query(TavernHero).filter(TavernHero.name.like('%{}%'.format(name))).all()


@db.atomic
def generate_hero(name=None, stat_points=None, s=None):
    if not name:
        print(set(s.query(TavernHero).values(TavernHero.name)))
        name = random.choice(list(set(SHAKESPEARE_NAMES) -
                                  {name[0] for name in s.query(TavernHero).values(TavernHero.name)}))
    primary, secondary = random.sample(job_raws.jobs.keys(), 2)
    epithet = create_epithet(primary, secondary)
    hero = TavernHero(name=name, epithet=epithet, level=1, primary_class=primary,
                      secondary_class=secondary, activity=HeroActivity.Elsewhere)
    s.add(hero)
    return hero


def create_epithet(primary, secondary):
    return '{} {}'.format(random.choice(tuple(job_raws.jobs[secondary].adjectives)).capitalize(),
                          random.choice(tuple(job_raws.jobs[primary].nouns)).capitalize())


@db.atomic
def change_hero_activity(hero, activity, tavern=None, s=None):
    if (activity == HeroActivity.VisitingTavern) != bool(tavern):
        raise TavernException(
            "Invalid activity change: Activity {} and Tavern {} both provided.".format(activity, tavern))

    if activity == hero.activity and (activity != HeroActivity.VisitingTavern or hero.visiting == tavern):
        return

    stop_log = logs.make_stop_activity_log(hero)
    if stop_log:
        s.add(stop_log)

    hero.activity = activity
    hero.visiting = tavern

    start_log = logs.make_start_activity_log(hero)
    if start_log:
        s.add(start_log)
