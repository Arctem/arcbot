import sys, os

try:
    import psutil
    print(' Succeeded in loading psutil for CPU and RAM tracking.')
except:
    print(' Could not import psutil for CPU and RAM tracking.')
    psutil = None

from ircbot.ircbot import IRCBot
from ircbot.help import Help
from ircbot.user_tracker import UserTracker

from karst import Karst
from link_command import Link
from markov import Markov
import phrase_commands
from thefucking import TheFucking
from word_swap import WordSwap
from assassins.coerce import Coercion

#from markov import Markov
#from markov import load as load_markov


class ArcBot(IRCBot):
    markov_dat_file = 'markov.botdat'
    links_file = 'links.botdat'

    def __init__(self):
        IRCBot.__init__(self, 'arcbot',
            "Ultimate Botting Machine:" +
            " http://i.imgur.com/mrrKP.png" +
            " https://www.youtube.com/watch?v=L9biyJcBhRs")

        self.register(Help(outro='If the help message is out of date, please ' +
            'yell at my creator until he fixes it. I don\'t like being out of' +
            ' date. :('))
        self.register(UserTracker())

        self.register(Karst())
        self.register(Link(ArcBot.links_file))
        self.register(Markov(ArcBot.markov_dat_file))
        self.register(TheFucking())
        self.register(WordSwap())
        self.register(Coercion())
        for cmd in phrase_commands.get_phrase_commands():
            self.register(cmd)



    def start(self):
        pass


def main(args = None):
    arcbot = ArcBot()
    arcbot.connect('irc.sudo-rmrf.net', 6667, ['#csb'])
    arcbot.process()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
