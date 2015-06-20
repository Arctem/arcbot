from ircbot.command import IRCCommand

class CoercionPlayer(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
