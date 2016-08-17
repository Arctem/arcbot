import re

from ircbot.events import sendmessage, sendaction
from ircbot.command import IRCCommand

import arcuser.arcuser_controller as arcuser_controller
import factoid.factoid_controller as factoid_controller

class FactoidPlugin(IRCCommand):
    def __init__(self):
        super(FactoidPlugin, self).__init__('fact', self.last_factoid,
            description='Get information on the last factoid triggered.')
        self.last = None

    def generalmessage(self, source, channel, msg):
        source = arcuser_controller.get_or_create_arcuser(source)
        factoid = factoid_controller.find_factoid(msg, channel)
        if factoid:
            self.last = factoid.id
            if factoid.verb == "'s'":
                self.fire(sendmessage(channel, "{}'s {}".format(factoid.trigger, factoid.reply)))
            elif factoid.verb == 'reply':
                self.fire(sendmessage(channel, factoid.reply))
            elif factoid.verb == 'action':
                self.fire(sendaction(channel, factoid.reply))
            else:
                self.fire(sendmessage(channel, '{} {} {}'.format(factoid.trigger, factoid.verb, factoid.reply)))

    def last_factoid(self, user, channel, args):
        if self.last:
            factoid = factoid_controller.get_factoid(self.last)
            self.fire(sendmessage(channel, '{}: Factoid #{} was set by {} with trigger {}.'.format(user.nick, factoid.id, factoid.creator.base.nick, factoid.trigger)))
        else:
            self.fire(sendmessage(channel, '{}: No recent factoid found.'.format(user.nick)))

#for directed messages
regex_learn = list(map(re.compile, [
    r"^(?P<trigger>\S+?(?:\s+\S+?)?)(?P<verb>'s)\s+(?P<reply>.+)$",
    r"^(?P<trigger>\S+?(?:\s+\S+?)?)\s+\<(?P<verb>.+?)\>\s+(?P<reply>.+)$",
    r"^(?P<trigger>\S+?(?:\s+\S+?)?)\s+(?P<verb>is|are)\s+(?P<reply>\S+(?:\s+\S+)?)$",
]))

#for the command (more general)
regex_teach = list(map(re.compile, [
    r"^(?P<trigger>.+?)\s+\<(?P<verb>.+?)\>\s+(?P<reply>.+)$",
    r"^(?P<trigger>.+?)(?P<verb>'s)\s+(?P<reply>.+)$",
    r"^(?P<trigger>.+?)\s+(?P<verb>is|are)\s+(?P<reply>.+)$",
]))

class LearnerPlugin(IRCCommand):
    def __init__(self):
        super(LearnerPlugin, self).__init__('learn', self.learn_factoid,
            description='arcbot is quite impressionable! Be careful what you teach him.')

    def directmessage(self, source, channel, msg):
        arcuser = arcuser_controller.get_or_create_arcuser(source)
        for regex in regex_learn:
            match = regex.search(msg)
            if match:
                trigger = match.group('trigger')
                reply = match.group('reply')
                verb = match.group('verb')
                factoid = factoid_controller.save_factoid(arcuser, channel, trigger, reply, verb)
                self.fire(sendmessage(channel, '{}: Okay! Learned factoid #{} for {}'.format(source.nick, factoid.id, trigger)))
                break

    def learn_factoid(self, source, channel, msg):
        arcuser = arcuser_controller.get_or_create_arcuser(source)
        for regex in regex_teach:
            match = regex.search(msg)
            if match:
                trigger = match.group('trigger')
                reply = match.group('reply')
                verb = match.group('verb')
                factoid = factoid_controller.save_factoid(arcuser, channel, trigger, reply, verb)
                self.fire(sendmessage(channel, '{}: Okay! Learned factoid #{} for {}'.format(source.nick, factoid.id, trigger)))
                break
