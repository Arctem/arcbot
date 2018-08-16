import tavern.hq.controller as hq_controller
import tavern.pool.controller as pool_controller
import tavern.util.tutorial as tutorial


class Pool():

    def __init__(self, plugin):
        self.plugin = plugin

    @tutorial.tutorial_lock
    def hire(self, arcuser, channel, args):
        tavern = hq_controller.find_tavern(arcuser)

        hero_to_hire = pool_controller.find_hero(name=args)
        if hero_to_hire:
            self.plugin.say(channel, '{}: Unimplemented (but hey, that person exists).'.format(arcuser.base.nick))
        else:
            self.plugin.say(channel, '{}: No hero named {}.'.format(arcuser.base.nick, args))
