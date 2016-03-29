import random
import re
import urllib.request as request

from ircbot.command import IRCCommand

class Link(IRCCommand):
    link_regex = re.compile(  r"^"
        # protocol identifier
        r"(?:(?:https?|ftp)://)"
        # user:pass authentication
        r"(?:\S+(?::\S*)?@)?"
        r"(?:"
        # IP address exclusion
        # private & local networks
        r"(?!(?:10|127)(?:\.\d{1,3}){3})"
        r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
        r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broacast addresses
        # (first & last IP address of each class)
        r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
        r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
        r"|"
        # host name
        r"(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        r"(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
        # TLD may end with dot
        r"\.?"
        r")"
        # port number
        r"(?::\d{2,5})?"
        # resource path
        r"(?:[/?#]\S*)?"
        r"$", re.IGNORECASE)

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

