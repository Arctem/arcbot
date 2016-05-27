import sys, os

from circuits import Debugger

# try:
#     import psutil
#     print(' Succeeded in loading psutil for CPU and RAM tracking.')
# except:
#     print(' Could not import psutil for CPU and RAM tracking.')
#     psutil = None

from ircbot.ircbot import IRCBot
from ircbot.help import Help
from ircbot import storage

from link_command import Link
from markov import Markov
import phrase_commands
from thefucking import TheFucking
from word_swap import WordSwap
from assassins.coerce import Coercion

storage.initialize('sqlite:///coerce.db')

class ArcBot(IRCBot):
    markov_dat_file = 'markov.botdat'
    links_file = 'links.botdat'

    def __init__(self):
        super(ArcBot, self).__init__(host='irc.sudo-rmrf.net', port=6667,
            channel='#csb', nick='arcbot',
            realname="Ultimate Botting Machine:" +
                " http://i.imgur.com/mrrKP.png" +
                " https://www.youtube.com/watch?v=L9biyJcBhRs")

    def init(self):
        Help(outro='If the help message is out of date, please ' +
            'yell at my creator until he fixes it. I don\'t like being out of' +
            ' date. :(').register(self)

        Link(ArcBot.links_file).register(self)
        Markov(ArcBot.markov_dat_file).register(self)
        TheFucking().register(self)
        WordSwap().register(self)
        Coercion().register(self)
        for cmd in phrase_commands.get_phrase_commands():
            cmd.register(self)

    def ready(self, component):
        pass

def main(args = None):
    arcbot = ArcBot()
    d = Debugger().register(arcbot)
    arcbot.run()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
