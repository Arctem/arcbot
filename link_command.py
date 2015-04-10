import random
import re
import urllib.request as request

from ircbot.command import IRCCommand

class Link(IRCCommand):
    link_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self, link_file):
        IRCCommand.__init__(self, 'link', self.link_trigger)

        self.link_file = link_file
        self.load()

    def link_trigger(self, user, chan, args):
        print(args)
        if args:
            args = args.split()
            if args[0] in self.links:
                self.owner.send_privmsg(chan, '{}: Link already in database.'
                    .format(user))
            elif Link.valid_link(args[0]):
                self.links.append(args[0])
                self.save()
                self.owner.send_privmsg(chan, '{}: Link added.'.format(user))
            else:
                self.owner.send_privmsg(chan, '{}: Invalid link.'.format(user))
        else:
            if self.links:
                self.owner.send_privmsg(chan, '{}: {}'.format(user,
                    random.choice(self.links)))
            else:
                self.owner.send_privmsg(chan, '{}: No links available.'
                    .format(user))

    def load(self):
        try:
            with open(self.link_file, 'r') as link_file:
                self.links = link_file.read().split('\n')
        except FileNotFoundError:
            self.links = []

    def save(self):
        with open(self.link_file, 'w') as link_file:
            link_file.write('\n'.join(self.links))

    def valid_link(link):
        if not Link.link_regex.match(link):
            return False
        try:
            req = request.urlopen(link)
            if req.getcode() // 100 == 2:
                return True
        except:
            return False
        return False

