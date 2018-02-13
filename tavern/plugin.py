from datetime import datetime

from circuits.core import timers

from ircbot.events import debugalert, sendmessage, sendaction, sendnotice
from ircbot.command import IRCCommand

import arcuser.arcuser_controller as arcuser_controller
#from factoid.events import registersmartvariable
from tavern.events import taverntick
from tavern.hq.commands import HQ
from tavern.pool.commands import Pool


class TavernPlugin(IRCCommand):

    def __init__(self):
        super(TavernPlugin, self).__init__('tavern', self.tavern,
                                           args='<things?>',
                                           description='Sorry Elliot, I got no idea yet.')

        self.hq = HQ(self)
        self.pool = Pool(self)

        self.functions = {
            'hire': self.pool.hire,
            'name': self.hq.generate,
            'generate': self.hq.generate,
            'status': self.hq.status,
        }

    def ready(self, component):
        self.ticker = timers.Timer(300, taverntick(), persist=True)
        self.ticker.register(self)
        self.fire(debugalert("Tavern tick rate started."))

    def taverntick(self):
        self.fire(debugalert("Tavern tick"))

    def tavern(self, user, channel, args):
        arcuser = arcuser_controller.get_or_create_arcuser(user)
        args = args.split()
        if len(args) is 0:
            # self.fire(sendmessage(channel, '{}: What do you want to do?'.format(user.nick)))
            self.fire(sendmessage(channel, '{}: {}'.format(user.nick, self.playerTavern)))
            return

        cmd = args[0]
        args = ' '.join(args[1:])
        if cmd not in self.functions:
            self.fire(sendmessage(channel, '{}: Invalid command {}.'.format(user.nick, cmd)))
        else:
            self.functions[cmd](arcuser, channel, args)

    def say(self, channel, message):
        self.fire(sendmessage(channel, message))

    def _tutorial_lock(function):
        def locked_function(self, arcuser, channel, args):
            self.fire(sendmessage(channel, 'here'))
            tavern = hq_controller.find_tavern(arcuser)
            if not tavern:
                self.fire(sendmessage(channel, '{}: Please name your tavern with ".tavern name <tavern name>" first.'.format(arcuser.base.nick)))
                return
            if not tavern.resident_hero:
                self.fire(sendmessage(channel, '{}: Please hire your first hero with ".tavern hire <hero name>" first.'.format(arcuser.base.nick)))
                return
            return function(self, arcuser, channel, args)
        return locked_function
