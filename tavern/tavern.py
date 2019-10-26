from datetime import datetime

from circuits.core import timers

from ircbot.events import debugalert, sendmessage, sendaction, sendnotice
from ircbot.command import IRCCommand
from ircbot.storage import session_scope

from tavern import tick, logs
from tavern.events import taverntick
from tavern.hq.commands import HQ
from tavern.pool.commands import Pool
from tavern.util import constants
import arcuser.arcuser_controller as arcuser_controller
import tavern.dungeon.controller as dungeon_controller
import tavern.hq.controller as hq_controller
import tavern.pool.controller as pool_controller
import tavern.util.tutorial

DEFAULT_CHANNEL = "#bot"


class TavernPlugin(IRCCommand):

    def __init__(self):
        super(TavernPlugin, self).__init__('tavern', self.tavern,
                                           args='<things?>',
                                           description='Sorry Elliot, I got no idea yet.')
        self.hq = HQ(self)
        self.pool = Pool(self)
        tavern.util.tutorial.plugin = self

        self.functions = {
            'hire': self.pool.hire,
            'quest': self.pool.quest,
            'name': self.hq.name,
            'create': self.hq.name,
            'status': self.hq.status,
            'tick': lambda *args, **kwargs: self.fire(taverntick()),
        }

    def ready(self, component):
        self.ticker = timers.Timer(constants.TICK_LENGTH, taverntick(), persist=True)
        self.ticker.register(self)
        self.fire(debugalert("Tavern tick rate started."))

    def taverntick(self):
        with session_scope() as s:
            self.fire(debugalert("Tavern tick"))
            # self.fire(sendnotice(DEFAULT_CHANNEL, "Tick"))
            if not tick.tick(s=s):
                self.fire(sendnotice(DEFAULT_CHANNEL, "Tick failed"))
                return

            for log in logs.get_unsent(s=s):
                print(log)
                if log.user:
                    self.fire(sendmessage(log.user.base.nick, str(log)))
                else:
                    self.fire(sendnotice(DEFAULT_CHANNEL, str(log)))
            logs.mark_all_sent(s=s)

    def tavern(self, user, channel, args):
        arcuser = arcuser_controller.get_or_create_arcuser(user)
        args = args.split()
        if len(args) is 0:
            self.say(channel, '{}: What do you want to do?'.format(user.nick))
            return

        cmd = args[0]
        args = ' '.join(args[1:])
        if cmd not in self.functions:
            self.fire(sendmessage(channel, '{}: Invalid command {}.'.format(user.nick, cmd)))
        else:
            self.functions[cmd](arcuser, channel, args)

    def say(self, channel, message):
        self.fire(sendmessage(channel, message))
