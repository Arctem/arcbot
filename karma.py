from ircbot.plugin import IRCPlugin
from datetime import datetime, timedelta
import re
import pickle


class Karma(IRCPlugin):
    def __init__(self, filename=None):
        IRCPlugin.__init__(self)

        help_msg = {
            'enroll': 'Registers you for sending karma.',
            'top[n] [category]': 'Shows the top n (defaults to 3) karma scores, optionally for category'
        }

        self.cooldown_time = 5   # Time user must wait between awarding karma, in minutes
        self.warmup_time = 10    # Time user must wait after enrolling to award karma

        self.triggers['PRIVMSG'] = (1, self.privmsg)
        self.filename = filename
        self.history = []
        self.individual = {}
        self.categories = {}
        self.cooldown = {}

    def save(self):
        data = [self.history, self.individual, self.categories, self.cooldown]
        with open(self.filename, 'wb') as load_file:
            pickle.dump(data, load_file)

    def load(self):
        try:
            with open(self.filename, 'rb') as load_file:
                data = pickle.load(load_file)
            self.history, self.individual, self.categories, self.cooldown = data
        except FileNotFoundError:
            print(' Could not load karma file {}.'.format(self.filename))

    def isOnCooldown(self, user):
        if user.lower() in self.cooldown:
            return self.cooldown[user.lower()] < datetime.now()

    def privmsg(self, prefix, args):
        channel = args[0]
        msg = args[1].split(" ")
        if 'karma' in msg:
            if re.match('^{}[:,] karma enroll'.format(self.owner.nick), args[1]):
                user = prefix.split('!')[0]
                if user.lower() in self.cooldown:
                    self.owner.send_privmsg(channel,
                                            "{}: You're already enrolled!"
                                            .format(user))
                    return 2

                self.cooldown[user.lower()] = datetime.now() + timedelta(minutes=self.warmup_time)
                self.owner.send_privmsg(channel,
                                        "{}: You are enrolled for karma.".format(user))
                return 2

            matches = re.search('^{}[:,] karma top(\d)?(?: (\w+))?'.format(self.owner.nick), args[1])
            if matches is not None:
                n = 3
                category = None

                if len(matches.groups()) > 0:
                    n = int(matches.groups()[0])
                if len(matches.groups()) > 1:
                    category = matches.groups()[1]

                if category in self.categories:
                    book = self.categories[category]
                else:
                    book = self.individual
                book = self.individual if category is None else self.categories.setdefault(category, {})
                if book is None:
                    # No such category
                    self.owner.send_privmsg(channel, "Nobody has any karma for {}.".format(category))
                    return 2

                count = 0
                preface = "Karma:" if book is self.individual else "{} karma:".format(category)
                sep = ", "
                karma = []
                for key in sorted(iter(book), key=book.get):
                    if count > n:
                        break
                    karma.append("{}: {}".format(key, book[key]))
                    count += 1

                self.owner.send_privmsg(channel, "{} {}".format(preface, sep.join(karma)))
                return 2

        if len(msg) > 4:
            # We never want more than 4 words, so don't do anything else
            return False
        else:
            mod = 0
            change = msg[-1]
            if change in ['++', '--']:
                mod = 1 if change == '++' else -1
            else:
                # This message wasn't a karma award
                return False

            user = prefix.split('!')[0]
            normie = user.lower()
            target = msg[0].lower()
            if normie not in self.cooldown:
                # Gotta "register" for karma first!
                # Discourages abuse.
                self.owner.send_privmsg(channel,
                                        "{}: Use '{}: karma enroll' to start using karma"
                                        .format(user, self.owner.nick))
                return 2

            elif not self.isOnCooldown(user):
                self.history.append((normie, msg))
                self.cooldown[normie] = datetime.now() + timedelta(minutes=self.cooldown_time)

                if len(msg) == 2:
                    if target in self.individual:
                        self.individual[target] += mod
                    else:
                        self.individual[target] = mod
                    self.owner.send_privmsg(channel,
                                            "{}: Karma for {} recorded."
                                            .format(user, target.title()))

                elif len(msg) == 3:
                    category = self.categories.setdefault(msg[1], {})
                    if target in category:
                        category[target] += mod
                    else:
                        category[target] = mod
                    self.owner.send_privmsg(channel,
                                            "{}: Karma for {} recorded."
                                            .format(user, target.title()))

                self.save()
                return 2

            elif self.isOnCooldown(user):
                # User made a karma action too recently
                remain = (self.cooldown[normie] - datetime.now()).total_seconds()/60
                self.owner.send_privmsg(channel,
                                        "{}: You must wait {} minutes to award karma."
                                        .format(user, int(remain)))
                return 2
