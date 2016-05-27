import re

from ircbot.plugin import IRCPlugin
from ircbot.events import sendmessage

class TheFucking(IRCPlugin):
    reg = re.compile(r'[tT][hH][eE] [fF][uU][cC][kK][iI][nN][gG]')

    def __init__(self):
        super(TheFucking, self).__init__()

    def generalmessage(self, user, channel, orig):
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
                else:
                    out[0] = ('f' if the[0] is 't' else 'F') + fucking[1:]
                if fucking == fucking.upper():
                    out[1] = 'THE'
                elif fucking[0] == fucking[0].upper():
                    out[1] = 'The'
                else:
                    out[1] = ('t' if fucking[0] is 'f' else 'T') + the[1:]
                orig = orig.replace(m, ' '.join(out))
            self.fire(sendmessage(channel, orig))
