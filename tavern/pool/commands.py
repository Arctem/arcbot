# from ircbot.storage import session_scope
import ircbot.storage as db

import tavern.dungeon.controller as dungeon_controller
import tavern.hq.controller as hq_controller
import tavern.pool.controller as pool_controller
import tavern.util.tutorial as tutorial

from tavern.tavern_models import HeroActivity


class Pool():

    def __init__(self, plugin):
        self.plugin = plugin

    @tutorial.tutorial_lock
    @db.atomic
    def hire(self, arcuser, channel, args, s=None):
        tavern = hq_controller.find_tavern(arcuser, s=s)
        if tavern.hired_hero is not None:
            self.plugin.say(channel, "{}: You've already hired {}. Use .tavern quest to send them somewhere!".format(
                arcuser.base.nick, tavern.hired_hero))
            s.rollback()
            return

        hero_to_hire = pool_controller.search_heroes(name=args, s=s)
        if len(hero_to_hire) is 1:
            hero = hero_to_hire[0]
            if hero.activity == HeroActivity.Elsewhere and tavern.resident_hero.id == hero.id:
                # hiring a resident hero is free
                pool_controller.hire_hero(tavern.id, hero.id, 0, s=s)
                s.commit()
                self.plugin.say(channel, '{}: You hired your resident hero, {}, for free. Use .tavern quest to send them somewhere!'.format(
                    arcuser.base.nick, hero))
                return
            if (hero.activity == HeroActivity.VisitingTavern and hero.visiting.id == tavern.id) or hero.activity == HeroActivity.CommonPool:
                if tavern.money < hero.cost:
                    self.plugin.say(channel, '{}: You only have {} gold but {} wants {}!'.format(
                        arcuser.base.nick, tavern.money, hero, hero.cost))
                    return
                pool_controller.hire_hero(tavern.id, hero.id, hero.cost, s=s)
                s.commit()
                self.plugin.say(channel, '{}: You hired {} for {}. Use .tavern quest to send them somewhere!'.format(
                    arcuser.base.nick, hero, hero.cost))
                return
            self.plugin.say(channel, '{}: {} is currently {} and cannot be hired.'.format(
                arcuser.base.nick, hero, hero.activity_string()))
            s.rollback()
            return
        elif len(hero_to_hire) > 1:
            self.plugin.say(channel, '{}: Found {} heroes. Please specify: {}'.format(
                arcuser.base.nick, len(hero_to_hire), ', '.join(map(str, hero_to_hire))))
            s.rollback()
            return
        else:
            self.plugin.say(channel, '{}: No hero named {}.'.format(arcuser.base.nick, args))
            s.rollback()
            return

    @tutorial.tutorial_lock
    @db.atomic
    def quest(self, arcuser, channel, args, s=None):
        tavern = hq_controller.find_tavern(arcuser, s=s)
        if tavern.hired_hero is None:
            self.plugin.say(
                channel, "{}: You haven't hired a hero yet. Use .tavern hire to hire an available hero!".format(arcuser.base.nick))
            s.rollback()
            return

        dungeons = dungeon_controller.search_dungeons(args, s=s)
        if len(dungeons) > 1:
            self.plugin.say(channel, '{}: Found {} dungeons. Please specify: {}'.format(
                arcuser.base.nick, len(dungeons), ', '.join(map(str, dungeons))))
            return
        elif len(dungeons) is 0:
            self.plugin.say(channel, '{}: No dungeons named {}.'.format(arcuser.base.nick, args))
            return

        dungeon = dungeons[0]
        hero = tavern.hired_hero
        pool_controller.start_adventure(hero.id, dungeon.id, tavern.id, s=s)
        self.plugin.say(channel, '{}: You sent {} on an adventure to {}! Hopefully they survive.'.format(
            arcuser.base.nick, hero, dungeon))
