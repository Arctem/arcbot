from ircbot.command import IRCCommand
from ircbot.events import sendmessage

import arcuser.arcuser_controller as arcuser_controller

class Me(IRCCommand):
    def __init__(self):
        super(Me, self).__init__('me', self.some_func)

    def me_cmd(self, user, channel, args):
        pass
