import random
import re

import inflection

from ircbot.command import IRCPlugin
from ircbot.events import sendmessage

regex_bandname = re.compile(r'^[a-zA-Z\'\-]{6,}\s[a-zA-Z\'\-]{6,}\s[a-zA-Z\'\-]{6,}$')

class BandPlugin(IRCPlugin):
    def __init__(self):
        super(BandPlugin, self).__init__()

    def generalmessage(self, user, channel, args):
        if user.bot:
            return False
        if regex_bandname.fullmatch(args) and random.randint(1, 2) is 1:
            name = inflection.titleize(args)
            self.fire(sendmessage(channel, '{} would make a good band name.'.format(name)))
