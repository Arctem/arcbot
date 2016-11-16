import sys, os

from circuits import Debugger

# try:
#     import psutil
#     print(' Succeeded in loading psutil for CPU and RAM tracking.')
# except:
#     print(' Could not import psutil for CPU and RAM tracking.')
#     psutil = None

from ircbot.ircbot import IRCBot

from ircbot.admin import Admin
from ircbot.command import IRCCommand
from ircbot.events import sendmessage
from ircbot.usertracker import UserTracker, LastMessage
from ircbot.help import Help
from ircbot import storage

from link_command import Link
from markov import Markov
import phrase_commands
from thefucking import TheFucking
from word_swap import WordSwap
from assassins.coerce import Coercion
from questions import Questions
from arcuser.arcuser import ArcUserVariables
from factoid.factoid import FactoidPlugin, LearnerPlugin
from factoid.smart_variables import SmartVariables
from band.band import BandPlugin

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
        Help(intro='The following modules are loaded. To find out more, do ' +
             '".help <module>."',
             outro='If you have any questions about me or a module, ' +
             'please direct them to arctem.').register(self)

        Link(ArcBot.links_file).register(self)
        Markov(ArcBot.markov_dat_file).register(self)
        TheFucking().register(self)
        WordSwap().register(self)
        Coercion().register(self)
        Questions().register(self)
        UserTracker().register(self)
        Admin().register(self)
        LastMessage().register(self)
        FactoidPlugin().register(self)
        LearnerPlugin().register(self)
        BandPlugin().register(self)
        SmartVariables().register(self)
        ArcUserVariables().register(self)
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
