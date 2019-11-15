from datetime import datetime

from circuits.core import timers

import arcuser.arcuser_controller as arcuser_controller
import tavern.dungeon.controller as dungeon_controller
import tavern.hq.controller as hq_controller
import tavern.pool.controller as pool_controller
import tavern.tick as tick
import tavern.util.tutorial
from ircbot.command import IRCCommand
from ircbot.events import debugalert, sendaction, sendmessage, sendnotice
from ircbot.storage import session_scope
from tavern import logs
from tavern.events import taverntick
from tavern.hq.commands import HQ
from tavern.pool.commands import Pool
from tavern.util import constants

DEFAULT_CHANNEL = "#bot"


class TavernPlugin(IRCCommand):

    def __init__(self):
        super(TavernPlugin, self).__init__('tavern', self.tavern,
                                           args='<function> [<args>]',
                                           description='A game about running a tavern and hiring adventurers!')
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

    def help_topics(self):
        return {
            'status': {
                None: 'See the status of your tavern with .status. Give an argument to learn about other things.',
                'dungeons': 'See the status of all the active dungeons.',
                'heroes': 'See the status of all the active heroes.',
                'search': 'Type any other string to search heroes, dungeons, and taverns and learn about them!',
            },
            'name': 'Create or rename your tavern with .name!',
            'hire': 'Use .hire to hire a hero, then use .quest to send them on a quest! Make sure you can afford to hire them with .status.',
            'quest': "Once you've hired a hero, use .quest <dungeon name> to send them on a quest!",
            'heroes': {
                None: 'Every hero has a name, a primary and secondary class, and a level.',
                'resident': 'Your tavern has a resident hero that only you can hire and is free! Treat them well.',
                'injury': 'Heroes can become injured. If you send them on another quest before they heal, they might die!',
                'visiting': "A visiting hero will buy drinks from your tavern, giving a bit of income. They also can't be hired by anyone else until they leave, so snatch them up while you can!",
                'square': "Heroes in the town square can be hired by anyone.",
                'classes': {
                    None: "A hero's class tells you what they're good at. If you want to succeed, never send a Rogue to do a Wizard's job!",
                    'barbarian': 'Barbarians are good at smashing fragile things, but have trouble catching evasive things.',
                    'bard': "Bards are charismatic musicians that can talk their way out of any situation. If that doesn't work, they're out of luck!",
                    'commoner': "Commoners aren't experts at any particular thing, but they aren't bad at anything either!",
                    'druid': "Druids are completely in-tune with nature, but haven't quite figured out how civilized life works.",
                    'monk': "Monks have trained for years to have lightning-fast reflexes, but anything that hurts to touch won't give them a good time.",
                    'rogue': "Rogues can sneak up on anyone bigger and slower than them, but you better hope nothing notices them!",
                    'scholar': "Scholars are experts on everything ancient, but haven't quite figured out this newfangled 'technology' the kids love talking about.",
                    'wizard': "Wizards have spent decades studying the arcane. It's left them a bit out of touch with day to day life.",
                },
            },
            'dungeons': {
                None: "Every dungeon has a number of floors, all crawling with monsters! Try to figure out which classes might be strong against the dungeon's theme if you want heroes to succeed."
            },
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
