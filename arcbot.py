import sys, os

try:
    import psutil
    print(' Succeeded in loading psutil for CPU and RAM tracking.')
except:
    print(' Could not import psutil for CPU and RAM tracking.')
    psutil = None

try:
    import nltk
    print(' Succeeded in loading nltk for natural language analysis.')
except:
    print(' Could not load nltk for language analysis.')
    nltk = None

from ircbot.ircbot import IRCBot
from ircbot.help import Help
from ircbot.user_tracker import UserTracker

import phrase_commands
from markov import Markov

#from markov import Markov
#from markov import load as load_markov


class ArcBot(IRCBot):
    markov_dat_file = 'markov.botdat'
    links_file = 'links.botdat'
    links_backup = 'links_backup.botdat'

    def __init__(self):
        IRCBot.__init__(self, 'newarcbot',
            "Ultimate Botting Machine:" +
            " http://i.imgur.com/mrrKP.png" +
            " https://www.youtube.com/watch?v=L9biyJcBhRs")

        self.register(Help(outro='If the help message is out of date, please ' +
            'yell at my creator until he fixes it. I don\'t like being out of' +
            ' date. :('))
        self.register(UserTracker())
        self.register(Markov(ArcBot.markov_dat_file))
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
