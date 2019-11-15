from datetime import datetime

import ircbot.storage as db

import tavern.pool.controller as pool_controller
from tavern.shared import TavernException
from tavern.tavern_models import HeroActivity, TavernLog


#########
# Taverns
#########


def tavern_got_money(tavern, money):
    return TavernLog(text="You got {money} gold. You now have {total} gold.".format(money=money, total=tavern.money),
                     user=tavern.owner.owner,
                     time=datetime.now())


def dead_hero_money_distributed(hero, money):
    return TavernLog(text="{hero}'s money was shared with the town. Each tavern has received {money}.".format(hero=hero, money=money),
                     time=datetime.now())

##########
# Dungeons
##########


@db.needs_session
def make_discovery_log(dungeon, s=None):
    return TavernLog(text="The entrance to {} has been found!".format(dungeon),
                     time=datetime.now())

########
# Heroes
########


@db.needs_session
def make_arrival_log(hero, s=None):
    return TavernLog(text="The brave hero {} has arrived in town!".format(hero),
                     time=datetime.now())

STOP_LOGS = {
    HeroActivity.Elsewhere: None,
    HeroActivity.CommonPool: "{hero} has left the town square.",
    HeroActivity.VisitingTavern: "{hero} has left {tavern}.",
    HeroActivity.Hired: None,
    HeroActivity.Adventuring: "{hero} has left {dungeon}.",
    HeroActivity.Dead: "{hero} has stopped...being dead? Really?",  # TODO
}


@db.needs_session
def make_stop_activity_log(hero, s=None):
    text = STOP_LOGS[hero.activity]
    if text:
        return TavernLog(text=text.format(hero=hero, tavern=hero.visiting,
                                          patron=hero.patron, employer=hero.employer,
                                          dungeon=pool_controller.get_dungeon(hero, s=s)),
                         time=datetime.now())

START_LOGS = {
    HeroActivity.Elsewhere: None,
    HeroActivity.CommonPool: "{hero} is hanging out in the town square.",
    HeroActivity.VisitingTavern: "{hero} is visiting {tavern}.",
    HeroActivity.Hired: "{hero} was hired by {employer}.",
    HeroActivity.Adventuring: "{hero} has started adventuring at {dungeon}.",
    HeroActivity.Dead: None,
}


@db.needs_session
def make_start_activity_log(hero, s=None):
    text = START_LOGS[hero.activity]
    if text:
        return TavernLog(text=text.format(hero=hero, tavern=hero.visiting,
                                          patron=hero.patron, employer=hero.employer,
                                          dungeon=pool_controller.get_dungeon(hero, s=s)),
                         time=datetime.now())


@db.needs_session
def hero_paid_tab(hero, amount, player, s=None):
    return TavernLog(text="{hero} paid {amount} gold for drinks.".format(hero=hero, amount=amount),
                     user=player,
                     time=datetime.now())


@db.needs_session
def hero_injured(hero, s=None):
    return TavernLog(text="{hero} has been injured!".format(hero=hero),
                     time=datetime.now())


@db.needs_session
def hero_died(hero, s=None):
    return TavernLog(text="{hero} died!".format(hero=hero),
                     time=datetime.now())


@db.needs_session
def hero_healed(hero, s=None):
    return TavernLog(text="{hero} has recovered from their wounds!".format(hero=hero),
                     time=datetime.now())


@db.needs_session
def hero_leveled_up(hero, level, s=None):
    return TavernLog(text="{hero} has reached level {level}!".format(hero=hero, level=level),
                     time=datetime.now())


############
# Adventures
############


@db.needs_session
def hero_injured_by_monster(hero, monster, player, s=None):
    return TavernLog(text="{hero} was injured by {monster}!".format(hero=hero, monster=monster),
                     user=player,
                     time=datetime.now())


@db.needs_session
def hero_killed_by_monster(hero, monster, player, s=None):
    return TavernLog(text="{hero} was killed by {monster}!".format(hero=hero, monster=monster),
                     user=player,
                     time=datetime.now())


@db.needs_session
def hero_defeated_monster(hero, monster, player, s=None):
    return TavernLog(text="{hero} has defeated {monster}!".format(hero=hero, monster=monster),
                     user=player,
                     time=datetime.now())


@db.needs_session
def hero_looted_monster(hero, monster, loot, player, s=None):
    return TavernLog(text="{hero} has defeated {monster} and looted {loot} gold!".format(hero=hero, monster=monster, loot=loot),
                     user=player,
                     time=datetime.now())


@db.needs_session
def hero_leveled_monster(hero, monster, player, s=None):
    return TavernLog(text="{hero} has leveled up from their experience defeating {monster}!".format(hero=hero, monster=monster),
                     user=player,
                     time=datetime.now())


@db.needs_session
def adventure_reached_floor(adventure, s=None):
    return TavernLog(text="{hero} has reached floor {floor_num} in {dungeon}."
                     .format(hero=adventure.hero, floor_num=adventure.floor.number, dungeon=adventure.dungeon),
                     user=adventure.employer.owner,
                     time=datetime.now())


@db.needs_session
def adventure_ended(hero, tavern, dungeon, money, s=None):
    return TavernLog(text="{hero} has returned from {dungeon}, bringing back {money} gold for themselves and {tavern}."
                     .format(hero=hero, tavern=tavern, dungeon=dungeon, money=money),
                     time=datetime.now())


@db.needs_session
def adventure_failed(hero, tavern, dungeon, money, s=None):
    return TavernLog(text="{hero} has failed {tavern}'s quest to {dungeon}, leaving {money} gold behind."
                     .format(hero=hero, tavern=tavern, dungeon=dungeon, money=money),
                     time=datetime.now())


@db.needs_session
def make_fight_log(hero, monster, result, player, s=None):
    return TavernLog(text="{hero} fought {monster}, and got {result}.".format(hero=hero, monster=monster, result=result),
                     user=player,
                     time=datetime.now())

################
# Log Management
################


@db.needs_session
def get_unsent(s=None):
    return s.query(TavernLog).filter(TavernLog.sent == False).order_by(TavernLog.time).all()


@db.needs_session
def mark_all_sent(s=None):
    return s.query(TavernLog).update({TavernLog.sent: True})
