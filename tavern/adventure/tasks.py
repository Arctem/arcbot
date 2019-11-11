from enum import Enum, auto
import random

import ircbot.storage as db

from tavern import logs
import tavern.adventure.controller as adventure_controller
import tavern.pool.controller as pool_controller
from tavern.tavern_models import Tavern, TavernAdventure, TavernDungeon, TavernHero, HeroActivity
import tavern.raws.monster as monster_raws


class BattleOutcome(Enum):
    INJURED = auto()
    FLEE = auto()
    WIN = auto()
    WIN_LOOT = auto()
    WIN_LEVEL = auto()
    WIN_ADVANCE = auto()


class BattleTier:

    def __init__(self, results, penalty, bonus):
        self.results = results
        self.penalty = penalty
        self.bonus = bonus

INJ = BattleOutcome.INJURED
FLE = BattleOutcome.FLEE
WIN = BattleOutcome.WIN
LOT = BattleOutcome.WIN_LOOT
LVL = BattleOutcome.WIN_LEVEL
ADV = BattleOutcome.WIN_ADVANCE

BATTLE_RESULTS = {
    -6: BattleTier((INJ, INJ, INJ, FLE, FLE, WIN), INJ, LVL),
    -5: BattleTier((INJ, INJ, FLE, FLE, WIN, LOT), INJ, LVL),
    -4: BattleTier((INJ, FLE, FLE, FLE, WIN, LOT), INJ, LVL),
    -3: BattleTier((INJ, FLE, FLE, FLE, WIN, LVL), INJ, LVL),
    -2: BattleTier((INJ, FLE, FLE, FLE, WIN, LVL), INJ, LVL),
    -1: BattleTier((INJ, FLE, FLE, WIN, WIN, LVL), FLE, LOT),
    0: BattleTier((INJ, FLE, FLE, WIN, LOT, LVL), FLE, LOT),
    1: BattleTier((INJ, FLE, FLE, LOT, LOT, LVL), FLE, LOT),
    2: BattleTier((INJ, FLE, FLE, LOT, LOT, ADV), FLE, LOT),
    3: BattleTier((INJ, FLE, WIN, LOT, LOT, ADV), FLE, ADV),
    4: BattleTier((INJ, FLE, WIN, LOT, ADV, ADV), FLE, ADV),
    5: BattleTier((FLE, FLE, WIN, LOT, ADV, ADV), INJ, ADV),
    6: BattleTier((FLE, WIN, WIN, LOT, ADV, ADV), INJ, ADV),
}


@db.needs_session
def adventure_tick(tick, s=None):
    process_active_adventures(s=s)


@db.needs_session
def process_active_adventures(s=None):
    for adventure in s.query(TavernAdventure).filter(TavernAdventure.active == True).all():
        floor = adventure.floor
        if len(floor.monsters) is 0:
            pass  # advance to next floor
            return
        enemy = random.choice(floor.monsters)
        result = battle_result(adventure.hero, enemy)
        if result == BattleTier.INJURED:
            if not adventure.hero.injured:
                pool_controller.injure_hero(adventure.hero, s=s)
                s.add(logs.hero_injured_by_monster(adventure.hero, enemy, adventure.employer.owner, s=s))
                adventure_controller.end_adventure(adventure, s=s)
                pool_controller.change_hero_activity(hero, HeroActivity.Elsewhere, s=s)
            else:
                pool_controller.kill_hero(adventure.hero, s=s)
                s.add(logs.hero_killed_by_monster(adventure.hero, enemy, adventure.employer.owner, s=s))
                adventure_controller.fail_adventure(adventure, s=s)
                pool_controller.change_hero_activity(hero, HeroActivity.Dead, s=s)
        elif result == BattleTier.FLEE:
            pass
        elif result == BattleTier.WIN:
            pass
        elif result == BattleTier.WIN_LOOT:
            pass
        elif result == BattleTier.WIN_LEVEL:
            pass
        elif result == BattleTier.WIN_ADVANCE:
            pass

        s.add(logs.make_fight_log(adventure.hero, enemy, result, adventure.employer.owner, s=s))


def battle_result(hero, monster):
    tier = battle_tier(hero, monster)
    results = list(tier.results)  # convert so we can modify it freely
    stock = monster_raws.stocks[monster.stock]
    strengths = stock.strengths
    weaknesses = stock.weaknesses
    if monster.modifier:
        modifier = monster_raws.modifiers[monster.modifier]
        strengths = list(strengths) + list(modifier.strengths)
        weaknesses = list(weaknesses) + list(modifier.weaknesses)
    for strength in strengths:
        if strength == hero.primary_class:
            results.append(tier.penalty)
            results.append(tier.penalty)
        if strength == hero.secondary_class:
            results.append(tier.penalty)
    for weakness in weaknesses:
        if weakness == hero.primary_class:
            results.append(tier.bonus)
            results.append(tier.bonus)
        if weakness == hero.secondary_class:
            results.append(tier.bonus)
    print("Results for {hero} vs {monster}: {results}".format(hero=hero, monster=monster, results=results))
    return random.choice(results)


def battle_tier(hero, monster):
    diff = hero.level - monster.level
    while diff not in BATTLE_RESULTS:
        diff = diff + (-1 if diff > 0 else 1)
    return BATTLE_RESULTS[diff]