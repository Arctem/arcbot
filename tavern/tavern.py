from datetime import datetime

from circuits.core import timers

from ircbot.events import debugalert, sendmessage, sendaction, sendnotice
from ircbot.command import IRCCommand

import arcuser.arcuser_controller as arcuser_controller
#from factoid.events import registersmartvariable
import tavern.controller as controller
from tavern.events import taverntick


class TavernPlugin(IRCCommand):

    def __init__(self):
        super(TavernPlugin, self).__init__('tavern', self.tavern,
                                           args='<things?>',
                                           description='Sorry Elliot, I got no idea yet.')
        self.functions = {
            'hire': self.cmd_hire,
            'name': self.cmd_name,
            'status': self.cmd_status,
        }

    def ready(self, component):
        self.ticker = timers.Timer(300, taverntick(), persist=True)
        self.ticker.register(self)
        self.fire(debugalert("Tavern tick rate started."))

    def taverntick(self):
        self.fire(debugalert("Tavern tick"))
        self.fire(sendnotice("#bot", "Tick"))

    def tavern(self, user, channel, args):
        arcuser = arcuser_controller.get_or_create_arcuser(user)
        args = args.split()
        if len(args) is 0:
            self.fire(sendmessage(channel, '{}: What do you want to do?'.format(user.nick)))
            return

        cmd = args[0]
        args = ' '.join(args[1:])
        if cmd not in self.functions:
            self.fire(sendmessage(channel, '{}: Invalid command {}.'.format(user.nick, cmd)))
        else:
            self.functions[cmd](arcuser, channel, args)

    def _tutorial_lock(function):
        def locked_function(self, arcuser, channel, args):
            tavern = controller.find_tavern(arcuser)
            if not tavern:
                self.fire(sendmessage(channel, '{}: Please name your tavern with ".tavern name <tavern name>" first.'.format(arcuser.base.nick)))
                return
            if not tavern.resident_hero:
                self.fire(sendmessage(channel, '{}: Please hire your first hero with ".tavern hire <hero name>" first.'.format(arcuser.base.nick)))
                return
            return function(self, arcuser, channel, args)
        return locked_function

    def cmd_name(self, arcuser, channel, args):
        tavern = controller.name_tavern(arcuser, args)
        if tavern:
            self.fire(sendmessage(channel, '{}: Your tavern is now named {}.'.format(arcuser.base.nick, tavern.name)))
        else:
            self.fire(sendmessage(channel, '{}: Unable to name tavern.'.format(arcuser.base.nick)))

    def cmd_hire(self, arcuser, channel, args):
        tavern = controller.find_tavern(arcuser)
        if not tavern:
            self.fire(sendmessage(channel, '{}: Please name your tavern with ".tavern name <tavern name>" first.'))
            return

        args = args.split()
        if len(args) is 0:
            self.fire(sendmessage(channel, '{}: Who do you want to hire?'.format(arcuser.base.nick)))
            return
        if not tavern.resident_hero:
            hero = controller.create_resident_hero(tavern, ' '.join(args))
            self.fire(sendmessage(channel, '{}: You have hired {}.'.format(arcuser.base.nick, hero)))
            return

        self.fire(sendmessage(channel, '{}: Unimplemented.'.format(arcuser.base.nick)))

    @_tutorial_lock
    def cmd_status(self, arcuser, channel, args):
        pass
