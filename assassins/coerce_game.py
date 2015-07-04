import os
import random
import re

from assassins.coerce import Coercion

base_dir = os.path.dirname(__file__)

class CoercionGame(object):
  def __init__(self, parent, chan):
    self.parent = parent
    self.chan = chan
    self.players = {}
    self.state = 'pregame'
    self.load_words()
    self.partial_points = {}

  def tell_player(self, player, msg):
    self.parent.owner.send_privmsg(player.name, msg)

  def announce(self, msg):
    self.parent.owner.send_privmsg(self.chan, msg)

  def handle_message(self, speaker, msg):
    if speaker in self.players and self.state == 'running':
      speaker = self.players[speaker]
      for player in self.players.values():
        if player == speaker:
          continue
        if re.search(player.word, msg, re.IGNORE_CASE):
          if player.target == speaker:
            self.end_game(winner=player)
          else:
            self.partial_points[player] += 1
        #check if it matched a word and increment score

  def end_game(self, winner=None):
    if winner:
      scores = self.calculate_scores()

      self.parent.award_points(winner, scores[None])
      self.announce("{} has won by getting {} to say {} and received {} points!"
        .format(winner.name, winner.target.name, winner.word, scores[None]))

      for player, points in scores.items:
        if not player:
          continue
        self.parent.award_points(player, points)
        self.announce("{} received {} for coercing non-targets into saying {}."
          .format(player.name, points, player.word))
    else:
      self.announce("The game ended for some reason. Whoops. No points have " +
        "been awarded.")

    for p in self.players.values():
      p.word = None
      p.target = None
    self.partial_points = {}

    self.state = 'pregame'

  def calculate_scores(self):
    total_partial = sum(self.partial_points.values())
    prize_pool = math.ceil(math.sqrt(total_partial))
    winner_score = max(prize_pool, 1)
    scores = { None: winner_score }
    for player, points in self.partial_points.items:
      scores[player] = min(prize_pool * (points / total_partial), .5 * prize_pool)
    return scores

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
        self.partial_points = { p : 0 for p in self.players.values() }
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
