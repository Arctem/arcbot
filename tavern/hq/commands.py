import tavern.hq.controller as hq_controller
import tavern.util.tutorial as tutorial


class HQ():

    def __init__(self, plugin):
        self.plugin = plugin

    def create(self, arcuser, channel, args):
        if len(args) is 0:
            self.plugin.say(
                channel, '{}: Please name your tavern with ".tavern name <tavern name>"'.format(arcuser.base.nick))
        else:
            tavern = hq_controller.name_tavern(arcuser, args)
            if tavern:
                self.plugin.say(channel, '{}: Your tavern is now named {}.'.format(arcuser.base.nick, tavern.name))

                tavern = hq_controller.find_tavern(arcuser)
                resident_hero = tavern.resident_hero
                if not tavern.resident_hero:
                    resident_hero = hq_controller.create_resident_hero(tavern)

                self.plugin.say(channel, '{}: Your tavern has a resident hero. Their name is {}.'.format(
                    arcuser.base.nick, resident_hero.name))
            else:
                self.plugin.say(channel, '{}: Unable to name tavern.'.format(arcuser.base.nick))

    @tutorial.tutorial_lock
    def status(self, arcuser, channel, args):
        tavern = hq_controller.find_tavern(arcuser)
        if not tavern:
            self.plugin.say(
                channel, '{}: Please name your tavern with ".tavern name <tavern name>" first.'.format(arcuser.base.nick))
            return
        heroes = hq_controller.find_heroes(tavern)
        if heroes:
            for hero in heroes:
                self.plugin.say(channel, '{}: {}'.format(arcuser.base.nick, hero))
        else:
            self.plugin.say(
                channel, '{}: Please hire your first hero with ".tavern hire <hero name>"'.format(arcuser.base.nick))
