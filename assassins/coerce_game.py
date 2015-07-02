import os
import random

from coerce import Coercion

base_dir = os.path.dirname(__file__)

class CoercionGame(object):
  def __init__(self, parent, chan):
    self.parent = parent
    self.chan = chan
    self.players = {}
    self.state = 'pregame'
    self.load_words()

  def tell_player(self, player, msg):
    self.parent.owner.send_privmsg(player.name, msg)

  def announce(self, msg):
    self.parent.owner.send_privmsg(self.chan, msg)

  def handle_message(self, user, msg):
    if user in self.players:
      #check if it matched a word and increment score

  def player_join(self, user):
    if user not in self.players:
      self.players[user] = CoercionPlayer(self, user)
      self.announce('{} has registered for the next game!')
    else:
      self.announce('{}: You are already registered.'.format(user))

  def player_quit(self, user):
    if user not in self.players:
      self.announce('{}: You are not registered!'.format(user))
    elif self.state == 'pregame':
      del self.players[user]
      self.announce('{} has been removed from the list of waiting players.')
    else: #if game is started
      #TODO: change the target of whoever is hunting this player
      pass

  def player_start(self, user):
    if self.state == 'pregame':
      if len(players) < Coercion.MIN_PLAYERS:
        self.announce('{}: We need at least {} players!'.format(user,
          Coercion.MIN_PLAYERS))
      else:
        self.announce('Starting a game with {} players!'.format(len(players)))
        self.assign_targets()
        self.assign_words()
        self.inform_players()
        self.state = 'running'
        self.announce('The game has now started!')
    else:
      self.announce('{}: The game is already in progress!'.format(user))

  def assign_targets(self):
    unused = set(self.players)
    used = {}
    next = random.choice(unused)

    while unused:
      #prevents first player being assigned themselves
      target = random.choice(unused - {next})
      self.players[next].target = self.players[target]
      unused.remove(target)
      used.add(target)
      next = target

  def assign_words(self):
    used_words = {}
    for player in self.players.keys():
      self.players[player].word = random.choice(self.word_list - used_words)
      used_words.update(self.players[player].word)

  def inform_players(self):
    for player in self.players:
      self.tell_player(player, "Your target in {} is {}. Get them to say {}."
        .format(player.target, player.word))

  def load_words(self):
    self.word_list = set()
    with open(os.path.join(base_dir, 'word_data/base.txt'), 'r') as base:
      self.word_list.update(base.read().split('\n'))
    #TODO load extra lists based on channel