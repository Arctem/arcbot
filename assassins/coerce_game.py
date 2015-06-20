from ircbot.command import IRCCommand

class CoercionGame(object):
    def __init__(self, chan):
        self.chan = chan
        self.players = []
        self.state = 'pregame'

    def game_trigger(self, user, chan, args):
        pass
