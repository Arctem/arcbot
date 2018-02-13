import tavern.pool.controller as pool_controller
import tavern.hq.controller as hq_controller


class Pool():
    def __init__(self, plugin):
        self.plugin = plugin

    def hire(self, arcuser, channel, args):
        tavern = hq_controller.find_tavern(arcuser)
        if not tavern:
            self.plugin.say(channel, '{}: Please name your tavern with ".tavern name <tavern name>" first.'.format(arcuser.base.nick))
            return

        hero_to_hire = pool_controller.find_hero(name=args)
        if hero_to_hire:
            self.plugin.say(channel, '{}: How did you get here?')
            # @TODO: hire a hero
        else:
            self.plugin.say(channel, '{}: No hero named {} was found.'.format(arcuser.base.nick, args))
