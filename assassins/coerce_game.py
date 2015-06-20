from ircbot.command import IRCCommand

class CoercionGame(object):
  def __init__(self, parent, chan):
    self.parent = parent
    self.chan = chan
    self.players = {}
    self.state = 'pregame'

  def tell_player(self, player, msg):
    self.parent.owner.send_privmsg(player, msg)

  def announce(self, msg):
    self.parent.owner.send_privmsg(self.chan, msg)

  def player_join(self, user):
    if user not in self.players:
      self.players[user] = CoercionPlayer(self, user)
      self.announce('{} has registered for the next game!')
    else:
      self.announce('{}: You are already registered.'.format(user))



