from ircbot.command import IRCCommand
from ircbot.events import sendmessage
from ircbot.plugin import IRCPlugin

import arcuser.arcuser_controller as arcuser_controller
from factoid.events import registersmartvariable

class Me(IRCCommand):
    def __init__(self):
        super(Me, self).__init__('me', self.me_cmd)

    def me_cmd(self, user, channel, args):
        pass


class ArcUserVariables(IRCPlugin):
    def ready(self, component):
        self.fire(registersmartvariable(self.user_variables))

    def user_variables(self, vars, trigger=None, target=None, **metadata):
        #supports $who, $someone, $to
        #maybe eventually supports $op
        replacements = {}
        if trigger:
            replacements['who'] = trigger.base.nick
        if target:
            replacements['to'] = target.base.nick
        return replacements
