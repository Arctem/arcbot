import re

from ircbot.command import IRCCommand

import assassins.coerce_controller as coerce_controller

class Coercion(IRCCommand):
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
    self.triggers['PRIVMSG'] = (9, self.privmsg)

  def privmsg(self, prefix, args):
    channel = args[0]
    args = args[1]
    user = prefix.split('!')[0]

    reg = re.compile(r'^{}[:,] {}'.format(self.owner.nick, self.command))
    trig = bool(reg.match(args))

    if trig:
      self.game_trigger(user, channel, args)
    else:
      coerce_controller.handle_message(channel, user, args)
      if coerce_controller.check_game_over(channel):
        coerce_controller.finish_game(channel, self.owner.send_privmsg)
    return trig

  def game_trigger(self, user, chan, args):
    cmd = args.split()[2] if len(args.split()) > 2 else 'help'
    args = args.split(None, 3)[3] if len(args.split()) > 3 else []
    print(cmd)
    print(args)

    private = not chan.startswith('#')

    if cmd == 'help':
      self.help(user, chan, args)
    elif cmd == 'join' and not private:
      coerce_controller.handle_join(chan, user, self.owner.send_privmsg)
    elif cmd == 'quit' and not private:
      coerce_controller.handle_quit(chan, user, self.owner.send_privmsg)
    elif cmd == 'start' and not private:
      coerce_controller.start_game(chan, self.owner.send_privmsg)
    elif cmd == 'score' and not private:
      coerce_controller.print_score(chan, user, args, self.owner.send_privmsg)
    elif cmd == 'status':
      #self.games[chan].player_status(user)
      coerce_controller.print_status(chan, user, self.owner.send_privmsg)
    elif cmd == 'reset' and user == 'arctem':
      coerce_controller.reset_game(chan)
    elif cmd == 'end' and user == 'arctem':
      coerce_controller.finish_game(chan, self.owner.send_privmsg)
    else:
      self.owner.send_privmsg(chan,
        '{}: Please include a command. Did you mean "help"?'.format(user))

  def help(self, user, chan, args):
    if args:
      topic = args.split()[0]
      self.owner.send_privmsg(chan, '{}: {}'.format(user, self.help_msg[topic]))
    else:
      self.owner.send_privmsg(chan, user + ': ' +
        self.create_generic_help().format(user))

  def create_generic_help(self):
    base = 'Welcome to Coercion! For more information, specify what you ' +\
      'want help about from the following topics: {}'
    topics = sorted(self.help_msg.keys())
    return base.format(', '.join(topics[:-1]) + ', and ' + topics[-1])

  def show_score(self, user, chan):
    if user in self.score:
      self.owner.send_privmsg(chan, '{}: You have {} points.'.format(user,
        self.score[user]))
    else:
      self.owner.send_privmsg(chan, '{}: You have no points.'.format(user))

  def award_points(self, player, points):
    if player.name not in self.score:
      self.score[player.name] = 0
    self.score[player.name] += points
