import random
import re

from ircbot.plugin import IRCPlugin
from ircbot.events import sendmessage

choose_regex = re.compile(r'^((?:(?:.+?), )*)(.+?),? or (.+?)\??$')

class Questions(IRCPlugin):
    def directmessage(self, user, channel, message):
        if not self.choose_one(user, channel, message):
            self.eightball(user, channel, message)

    def choose_one(self, user, channel, message):
        options = choose_regex.match(message).groups()
        if not options:
            return False

        options = list(options)

        if options[0]:
            #exclude the last element of options[0] because it's always blank
            options = options[0].split(', ')[:-1] + options[1:]
        else:
            options = options[1:]

        if random.randint(1, 500) == 500:
            if len(options) == 2:
                choice = 'Both.'
            else:
                choice = ' and '.join(random.sample(map(str,options), 2)) + '.'
        else:
            choice = random.choice(options)

        self.fire(sendmessage(channel, '{}: {}'.format(user.nick, choice)))
        return True

    def eightball(self, user, channel, message):
        if message[-1] == '?':
            self.fire(sendmessage(channel, '{}: {}'.format(user.nick, random.choice(eightball_responses))))
