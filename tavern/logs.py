from datetime import datetime

import ircbot.storage as db
import tavern.pool.controller as pool_controller
from tavern.shared import TavernException
from tavern.tavern_models import HeroActivity, TavernLog
from tavern.util import constants

#########
# Taverns
#########


def tavern_got_money(tavern, money):
    return TavernLog(text="You got {money} gold. You now have {total} gold.".format(money=money, total=tavern.money),
                     user=tavern.owner,
                     time=datetime.now())


def dead_hero_money_distributed(hero, money):
    return TavernLog(text="{hero}'s money was shared with the town. Each tavern has received {money} gold.".format(hero=hero, money=money),
                     time=datetime.now())

##########
# Dungeons
##########


def make_discovery_log(dungeon):
    return TavernLog(text="The entrance to {} has been found!".format(dungeon),
                     time=datetime.now())


def make_hidden_log(dungeon):
    return TavernLog(text="The way to {} has been lost!".format(dungeon),
                     time=datetime.now())


########
# Heroes
########


@db.needs_session
def make_arrival_log(hero, s=None):
    return TavernLog(text="The brave hero {} has arrived in town!".format(hero),
                     time=datetime.now())


def pool_refreshed(visitors, pool):
    return TavernLog(text="Heroes in town have moved around. {pool} are available in the town square while {vistors} are visiting taverns."
                     .format(pool=pool, visitors=visitors),
                     time=datetime.now())


def hero_visiting(hero, tavern):
    return TavernLog(text="{hero} is visiting your tavern. They can be hired or will pay {tab} for their drinks when they leave."
                     .format(hero=hero, tab=constants.HERO_BAR_TAB),
                     user=tavern.owner,
                     time=datetime.now())


def hero_paid_tab(hero, amount, player):
    return TavernLog(text="{hero} paid {amount} gold for drinks.".format(hero=hero, amount=amount),
                     user=player,
                     time=datetime.now())


def hero_short_on_tab(hero, total, paid, player):
    return TavernLog(text="{hero} couldn't cover their full tab of {total} gold so only paid {paid}.".format(hero=hero, total=total, paid=paid),
                     user=player,
                     time=datetime.now())


def hero_broke_tab(hero, player):
    return TavernLog(text="{hero} is broke and skipped out without paying their tab!".format(hero=hero),
                     user=player,
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

def hero_fled_monster(hero, monster, player):
    return TavernLog(text="{hero} has narrowly evaded {monster}.".format(hero=hero, monster=monster),
                     user=player,
                     time=datetime.now())


def hero_defeated_monster(hero, monster, player):
    return TavernLog(text="{hero} has defeated {monster}!".format(hero=hero, monster=monster),
                     user=player,
                     time=datetime.now())


def hero_looted_monster(hero, monster, loot, player):
    return TavernLog(text="{hero} has defeated {monster} and looted {loot} gold!".format(hero=hero, monster=monster, loot=loot),
                     user=player,
                     time=datetime.now())


def hero_leveled_monster(hero, monster, player):
    return TavernLog(text="{hero} has leveled up from their experience defeating {monster}!".format(hero=hero, monster=monster),
                     user=player,
                     time=datetime.now())


def hero_injured_by_monster(adventure, monster):
    return TavernLog(text="{hero} was injured by {monster} on {floor}!"
                     .format(hero=adventure.hero, monster=monster, floor=adventure.floor),
                     time=datetime.now())


def hero_killed_by_monster(adventure, monster):
    return TavernLog(text="{hero} was killed by {monster} on {floor}!"
                     .format(hero=adventure.hero, monster=monster, floor=adventure.floor),
                     time=datetime.now())


def adventure_reached_floor(adventure):
    return TavernLog(text="{hero} has reached floor {floor_num} in {dungeon}."
                     .format(hero=adventure.hero, floor_num=adventure.floor.number, dungeon=adventure.dungeon),
                     user=adventure.employer.owner,
                     time=datetime.now())


def adventure_started(hero, dungeon, tavern):
    return TavernLog(text="{hero} has been sent to explore {dungeon} at the request of {tavern}."
                     .format(hero=hero, dungeon=dungeon, tavern=tavern),
                     time=datetime.now())


def adventure_ended(hero, dungeon, tavern, money):
    return TavernLog(text="{hero} has returned from {dungeon}, bringing back {money} gold for themselves and {tavern}."
                     .format(hero=hero, tavern=tavern, dungeon=dungeon, money=money),
                     time=datetime.now())


def adventure_failed(hero, dungeon, tavern,  money):
    return TavernLog(text="{hero} has failed {tavern}'s quest to {dungeon}, leaving {money} gold behind."
                     .format(hero=hero, tavern=tavern, dungeon=dungeon, money=money),
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
