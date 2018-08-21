import tavern.hq.controller as hq_controller

plugin = None


def tutorial_lock(function):
    def locked_function(self, arcuser, channel, args):
        global plugin
        tavern = hq_controller.find_tavern(arcuser)
        if not tavern:
            plugin.say(
                channel, '{}: Please name your tavern with ".tavern name <tavern name>" first.'.format(arcuser.base.nick))
            return
        if not tavern.resident_hero:
            plugin.say(
                channel, '{}: Please hire your first hero with ".tavern hire <hero name>" first.'.format(arcuser.base.nick))
            return
        return function(self, arcuser, channel, args)
    return locked_function
