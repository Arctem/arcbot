import re

from ircbot.plugin import IRCPlugin

class TheFucking(IRCPlugin):
    reg = re.compile(r'[tT][hH][eE] [fF][uU][cC][kK][iI][nN][gG]')

    def __init__(self):
        IRCPlugin.__init__(self)
        self.triggers['PRIVMSG'] = (0, self.privmsg)

    def privmsg(self, prefix, args):
        channel = args.pop(0)
        user = prefix.split('!')[0]

        orig = args[0]
        matches = self.reg.findall(orig)
        if not matches:
            return False
        else:
            for m in set(matches):
                the, fucking = m.split(' ')
                out = ['fucking', 'the']
                if the == the.upper():
                    out[0] = 'FUCKING'
                elif the[0] == the[0].upper():
                    out[0] = 'Fucking'
                if fucking == fucking.upper():
                    out[0] = 'THE'
                elif fucking[0] == fucking[0].upper():
                    out[0] = 'The'
                orig = orig.replace(m, ' '.join(out))
            self.owner.send_privmsg(channel, orig)
            return True

