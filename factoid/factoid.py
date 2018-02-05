import re

from ircbot.events import sendmessage, sendaction
from ircbot.command import IRCCommand

import arcuser.arcuser_controller as arcuser_controller
import factoid.factoid_controller as factoid_controller
from factoid.events import sendsmartmessage, sendsmartaction

regex_to = re.compile('^(?P<to>\S+)[:,]\s+(?P<message>.+)$')


class FactoidPlugin(IRCCommand):

    def __init__(self):
        super(FactoidPlugin, self).__init__('fact', self.last_factoid,
                                            args='[[<command> ]<factoid_number>]',
                                            description='Get information on the last factoid triggered.')
        self.last = None

    def generalmessage(self, source, channel, message):
        source = arcuser_controller.get_or_create_arcuser(source)
        factoid = factoid_controller.find_factoid(message, channel)
        for msg in [message, message.lower()]:
            if not factoid:
                match = regex_to.search(msg)
                if match:
                    to = match.group('to')
                    msg = match.group('message')
                    factoid = factoid_controller.find_factoid(msg, channel)
            if not factoid:
                factoid = factoid_controller.find_factoid(msg.rstrip('?'), channel)
            if factoid:
                break
        if factoid:
            self.last = factoid.id
            if factoid.verb == "'s":
                self.fire(sendsmartmessage(channel, "{}'s {}".format(factoid.trigger, factoid.reply),
                                           channel=channel, original=message, trigger=source))
            elif factoid.verb == 'reply':
                self.fire(sendsmartmessage(channel, factoid.reply, channel=channel, original=message, trigger=source))
            elif factoid.verb == 'action':
                self.fire(sendsmartaction(channel, factoid.reply, channel=channel, original=message, trigger=source))
            else:
                self.fire(sendsmartmessage(channel, '{} {} {}'.format(factoid.trigger,
                                                                      factoid.verb, factoid.reply), channel=channel, original=message, trigger=source))

    # oh god this method is awful I need to refactor it
    def last_factoid(self, user, channel, args):
        args = args.split()
        if len(args) == 0:
            if self.last:
                factoid = factoid_controller.get_factoid(self.last)
                self.print_factoid_info(user, channel, factoid)
            else:
                self.fire(sendmessage(channel, '{}: No recent factoid found.'.format(user.nick)))
        elif len(args) == 1:
            factoid = factoid_controller.get_factoid(int(args[0]))
            if factoid:
                self.print_factoid_info(user, channel, factoid)
            else:
                self.fire(sendmessage(channel, '{}: Could not find factoid #{}.'.format(user.nick, args[0])))
        elif len(args) > 1:
            cmd = args[0]
            id = int(args[1])
            if cmd == 'delete':
                factoid = factoid_controller.get_factoid(id)
                if not factoid:
                    self.fire(sendmessage(channel, '{}: Factoid {} does not exist.'.format(user.nick, id)))
                elif user.admin or factoid.creator.base.id == user.id:
                    if factoid_controller.delete_factoid(id):
                        self.fire(sendmessage(channel, '{}: Deleted factoid #{}.'.format(user.nick, id)))
                    else:
                        self.fire(sendmessage(channel, '{}: Could not delete factoid #{}.'.format(user.nick, id)))
                else:
                    self.fire(sendmessage(channel, "{}: Only admins can delete other users' factoids."
                                          .format(user.nick)))
            else:
                self.fire(sendmessage(channel, '{}: Command {} not available.'.format(user.nick, cmd)))

    def print_factoid_info(self, user, channel, factoid):
        self.fire(sendmessage(channel, '{}: Factoid #{} was set by {} with trigger {}.'.format(
            user.nick, factoid.id, factoid.creator.base.nick, factoid.trigger)))

    def stats(self):
        stats = {
            (lambda: "There are {} factoids.".format(factoid_controller.count_factoids()),
                ('factoids', 'counts', 'all')),
            (self._top_factoider, ('factoids', 'counts', 'top'))
        }
        for arcuser in factoid_controller.get_all_arcusers_with_factoids():
            stats.add((
                self._make_stat_for_arcuser(arcuser),
                ('factoids', 'counts', arcuser.base.nick)
            ))
        return stats

    def _make_stat_for_arcuser(self, arcuser):
        return lambda: "{} has created {} factoids.".format(arcuser.base.nick, factoid_controller.count_factoids(arcuser))

    def _top_factoider(self):
        arcusers = factoid_controller.get_all_arcusers_with_factoids()
        top_arcusers, top_count = arcusers[:1], factoid_controller.count_factoids(arcusers[0])
        for arcuser in arcusers[1:]:
            count = factoid_controller.count_factoids(arcuser)
            if count > top_count:
                top_arcusers = [arcuser]
                top_count = count
            elif count == top_count:
                top_arcusers.append(arcuser)

        if not top_arcusers:
            return 'No one has submitted any factoids!'
        elif len(top_arcusers) == 1:
            return '{} has submitted the most factoids, with {}.'.format(top_arcusers[0].base.nick, top_count)
        else:
            start = ', '.join(map(lambda u: u.base.nick, top_arcusers[:-1]))
            users_string = start + ' and ' + top_arcusers[-1].base.nick
            return '{} have submitted the most factoids, with {} each.'.format(users_string, top_count)

# for directed messages
regex_learn = list(map(re.compile, [
    r"^(?P<trigger>\S+?(?:\s+\S+?)?)\s*\<(?P<verb>.+?)\>\s+(?P<reply>.+)$",
    r"^(?P<trigger>\S+?(?:\s+\S+?)?)\s+(?P<verb>is|are)\s+(?P<reply>\S+(?:\s+\S+)?)$",
    r"^(?P<trigger>\S+?(?:\s+\S+?)?)(?P<verb>'s)\s+(?P<reply>.+)$",
]))

# for the command (more general)
regex_teach = list(map(re.compile, [
    r"^(?P<trigger>.+?)\s*\<(?P<verb>.+?)\>\s+(?P<reply>.+)$",
    r"^(?P<trigger>.+?)\s+(?P<verb>is|are)\s+(?P<reply>.+)$",
    r"^(?P<trigger>.+?)(?P<verb>'s)\s+(?P<reply>.+)$",
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
                return

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
                return
        self.fire(sendmessage(channel, "{}: Sorry, I couldn't understand that factoid. Remember to include a verb!"
                              .format(source.nick)))
