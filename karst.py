from ircbot.plugin import IRCPlugin

class Karst(IRCPlugin):
    def __init__(self):
        IRCPlugin.__init__(self)
        self.triggers['PRIVMSG'] = self.privmsg

    def privmsg(self, prefix, args):
        channel = args.pop(0)
        user = prefix.split('!')[0]

        trig = 'karst' in user.lower() and '2spookybot' in args[0]
        
        if trig:
            self.owner.send_privmsg(channel, "{}: Why can't you love me for who I am!?"
                .format(user))
        return trig
