import tavern.hq.controller as hq_controller
import tavern.pool.controller as pool_controller
import tavern.util.tutorial as tutorial

from tavern.tavern_models import HeroActivity


class Pool():

    def __init__(self, plugin):
        self.plugin = plugin

    @tutorial.tutorial_lock
    def hire(self, arcuser, channel, args):
        tavern = hq_controller.find_tavern(arcuser)
        if tavern.hired_hero is not None:
            self.plugin.say(channel, "{}: You've already hired {}. Use .quest to send them somewhere!".format(
                arcuser.base.nick, tavern.hired_hero))
            return

        hero_to_hire = pool_controller.search_heroes(name=args)
        if len(hero_to_hire) is 1:
            hero = hero_to_hire[0]
            if hero.activity == HeroActivity.Elsewhere and tavern.resident_hero == hero:
                # hiring a resident hero is free
                pool_controller.hire_hero(tavern.id, hero.id, 0)
                self.plugin.say(channel, '{}: You hired your resident hero, {}, for free. Use .quest to send them somewhere!'.format(
                    arcuser.base.nick, hero))
                return
            if hero.visiting == tavern or hero.activity == HeroActivity.CommonPool:
                if tavern.money < hero.cost:
                    self.plugin.say(channel, '{}: You only have {} gold but {} wants {}!'.format(
                        arcuser.base.nick, tavern.money, hero, hero.cost))
                    return
                pool_controller.hire_hero(tavern.id, hero.id, hero.cost)
                self.plugin.say(channel, '{}: You hired {} for {}. Use .quest to send them somewhere!'.format(
                    arcuser.base.nick, hero, hero.cost))
                return
            print("hero.visiting: ", hero.visiting)
            print("tavern: ", tavern)
            self.plugin.say(channel, '{}: {} is currently {} and cannot be hired.'.format(
                arcuser.base.nick, hero, hero.activity_string()))
            return
        elif len(hero_to_hire) > 1:
            self.plugin.say(channel, '{}: Found {} heroes. Please specify: {}'.format(
                arcuser.base.nick, len(hero_to_hire), ', '.join(map(str, hero_to_hire))))
        else:
            self.plugin.say(channel, '{}: No hero named {}.'.format(arcuser.base.nick, args))
