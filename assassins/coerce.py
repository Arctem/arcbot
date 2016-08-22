import re

from ircbot.command import IRCCommand
from ircbot.events import sendmessage

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
    'status' : 'Display information about the game currently in progress.',
    'end' : 'Admin command to end a game with scoring.',
    'kick' : 'Admin command to kick a player.',
    'reset' : 'Admin command to end a game without scoring.'
  }

  def __init__(self):
    super(Coercion, self).__init__('coerce', self.game_trigger)

  def directmessage(self, user, channel, args):
      self.generalmessage(user, channel, args)

  def generalmessage(self, user, channel, args):
    coerce_controller.handle_message(channel, user.nick, args)
    if coerce_controller.check_game_over(channel):
      coerce_controller.finish_game(channel, self.send_func)

  def game_trigger(self, user, chan, args):
    cmd = args.split()[0] if len(args.split()) > 0 else 'help'
    args = args.split(None, 1)[1] if len(args.split()) > 1 else []

    private = not chan.startswith('#')

    if cmd == 'help':
      self.help(user.nick, chan, args)
    elif cmd == 'join' and not private:
      coerce_controller.handle_join(chan, user.nick, self.send_func)
    elif cmd == 'quit' and not private:
      coerce_controller.handle_quit(chan, user.nick, self.send_func)
    elif cmd == 'start' and not private:
      coerce_controller.start_game(chan, self.send_func)
    elif cmd == 'score' and not private:
      coerce_controller.print_score(chan, user.nick, args, self.send_func)
    elif cmd == 'top' and not private:
      coerce_controller.print_top(chan, user.nick, args, self.send_func)
    elif cmd == 'status':
      #self.games[chan].player_status(user.nick)
      coerce_controller.print_status(chan, user.nick, self.send_func)
    elif cmd == 'reset' and user.admin:
      coerce_controller.reset_game(chan)
    elif cmd == 'end' and user.admin:
      coerce_controller.finish_game(chan, self.send_func)
    elif cmd == 'kick' and user.admin:
      coerce_controller.handle_quit(chan, args, self.send_func)
    else:
      self.fire(sendmessage(chan,
        '{}: Please include a command. Did you mean "help"?'.format(user.nick)))

  def send_func(self, chan, msg):
    self.fire(sendmessage(chan, msg))

  def help(self, user, chan, args):
    if args:
      topic = args.split()[0]
      self.fire(sendmessage(chan, '{}: {}'.format(user, self.help_msg[topic])))
    else:
      self.fire(sendmessage(chan, user + ': ' +
        self.create_generic_help().format(user)))

  def create_generic_help(self):
    base = 'Welcome to Coercion! For more information, specify what you ' +\
      'want help about from the following topics: {}'
    topics = sorted(self.help_msg.keys())
    return base.format(', '.join(topics[:-1]) + ', and ' + topics[-1])
