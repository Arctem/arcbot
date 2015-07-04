from ircbot.command import IRCCommand

from coerce_game import CoercionGame

class Coercion(IRCCommand):
  MIN_PLAYERS = 4

  help_msg = {
    'rules' : 'When a round of Coercion starts, you will be assigned a ' +
      'target and a word. The first player who gets their target to say the ' +
      'assigned word wins the round and gets a point.',
    'join' : 'Sign up to participate in the next round of the game.',
    'quit' : 'Leave the game. Someone else will receive your mission instead.',
    'start' : 'Trigger the start of the next round if enough players have ' +
      'joined.',
    'score' : 'View the scoreboard.',
    'status' : 'Display information about the game currently in progress.'
  }

  def __init__(self):
    IRCCommand.__init__(self, 'coerce', self.game_trigger)

    #hash of channel to CoercionGame object.
    self.games = {}
    self.triggers['PRIVMSG'] = (9, self.privmsg)
    self.score = {}

  def privmsg(self, prefix, args):
    channel = args[0]
    args = args[1]
    user = prefix.split('!')[0]

    if channel in self.games:
      self.games[channel].message(user, args)

  def game_trigger(self, user, chan, args):
    cmd = args.split()[0] if args else 'help'
    args = args.split()[1:] if args else []

    private = not chan.startswith('#')
    if not private and chan not in self.games:
      self.games[chan] = CoercionGame(self, chan)

    if cmd == 'help':
      self.help(user, chan, args)
    elif cmd == 'join' and not private:
      self.games[chan].player_join(user)
    elif cmd == 'quit' and not private:
      self.games[chan].player_quit(user)
    elif cmd == 'start' and not private:
      self.games[chan].player_start(user)
    elif cmd == 'score' and not private:
      self.score(user, chan)
    elif cmd == 'status':
      pass
    else:
      self.owner.send_privmsg(chan,
        '{}: Please include a command. Did you mean "help"?'.format(user))

  def help(self, user, chan, args):
    topic = args[0]
    if args:
      self.owner.send_privmsg(chan, '{}: {}'.format(user, self.help_msg[topic]))
    else:
      self.owner.send_privmsg(chan, user + ': ' +
        self.create_generic_help().format(user))

  def create_generic_help(self):
    base = 'Welcome to Coercion! For more information, specify what you want ' +
      'help about from the following topics: {}'
    topics = sorted(self.help.keys())
    return base.format(', '.join(topics[:-1]) + ', and ' + topics[-1])

  def score(self, user, chan):
    if user in self.score:
      self.owner.send_privmsg(chan, '{}: You have {} points.'.format(user,
        self.score[user]))
    else:
      self.owner.send_privmsg(chan, '{}: You have no points.'.format(user))

  def award_points(self, player, points):
    if player.name not in self.score:
      self.score[player.name] = 0
    self.score[player.name] += points
