import datetime
import math
import os
import random
import re
import time

from sqlalchemy.sql import exists

import ircbot.storage as db

from assassins.coerce_models import CoercePlayer, CoercePlayerGame, CoercePartialPoint, CoerceGame

MIN_PLAYERS = 4
BASE_DIR = os.path.dirname(__file__)

##################
# Special Exceptions
##################

class CoerceException(Exception):
  def __init__(self, *args, **kwargs):
    Exception.__init__(self, *args, **kwargs)

class MissingChannelException(CoerceException):
  def __init__(self, *args, **kwargs):
    CoerceException.__init__(self, "Could not find a channel to use to load or create a game.")

class PlayerInGameException(CoerceException):
  def __init__(self, *args, **kwargs):
    CoerceException.__init__(self, "Player is already in the game.")

class PlayerNotInGameException(CoerceException):
  def __init__(self, *args, **kwargs):
    CoerceException.__init__(self, "Player is not in the game.")

class GameInProgressException(CoerceException):
  def __init__(self, *args, **kwargs):
    CoerceException.__init__(self, "Game is in progress.")

class NoSuchPlayerException(CoerceException):
  def __init__(self, name, *args, **kwargs):
    CoerceException.__init__(self, "No player named {}.".format(name))

class NotEnoughPlayersException(CoerceException):
  def __init__(self, *args, **kwargs):
    CoerceException.__init__(self, "Game requires at least {} players.".format(MIN_PLAYERS))

##################
# Decorators
##################

#loads a session if needed
def needs_session(func):
  def needs_session_wrapper(*args, s=None, **kwargs):
    if not s:
      s = db.session()
    return func(*args, s=s, **kwargs)
  return needs_session_wrapper

#make sure we commit at the end of this function
def atomic(func):
  @needs_session
  def atomic_wrapper(*args, s=None, **kwargs):
    if hasattr(func, 'atomic') and func.atomic:
      return func(*args, s=s, **kwargs)

    try:
      func.atomic = True
      retval = func(*args, s=s, **kwargs)
      s.commit()
      return retval
    except CoerceException as e:
      print(e)
      s.rollback()
    except Exception as e:
      print(e)
      s.rollback()
      raise e
    finally:
      func.atomic = False
      s.close()
  return atomic_wrapper

def load_game(func, argnum=0):
  @needs_session
  def load_game_wrapper(*args, s=None, **kwargs):
    if not isinstance(args[argnum], CoerceGame):
      args = list(args)
      args[argnum] = get_game(args[argnum], s=s)
      args = tuple(args)
    return func(*args, s=s, **kwargs)
  return load_game_wrapper

##################
# Start of main functions
##################

@needs_session
def get_game(channel, s=None):
  game = s.query(CoerceGame).filter_by(chan = channel).one_or_none()
  if not game:
    game = CoerceGame(chan = channel)
    s.add(game)
  return game

@needs_session
def get_player(name, s=None):
  player = s.query(CoercePlayer).filter(CoercePlayer.name == name).one_or_none()
  return player

@atomic
@load_game
def handle_join(game, name, print_func=print, s=None):
  player = get_player(name, s=s)
  if not player:
    player = CoercePlayer(name=name)
    s.add(player)

  if s.query(CoercePlayerGame).filter_by(game = game, player = player).first():
    print_func(game.chan, "{}: You are already in the game.".format(name))
    raise PlayerInGameException()

  s.add(CoercePlayerGame(player=player, game=game))
  print_func(game.chan, "{} has joined the game.".format(name))

@atomic
@load_game
def handle_quit(game, name, print_func=print, s=None):
  player = get_player(name, s=s)
  error = None

  if not player:
    error = NoSuchPlayerException(name)
  elif game.state == 'pregame':
    if s.query(CoercePlayerGame).filter_by(game = game, player = player).delete() > 0:
      print_func(game.chan, "{} has left the game.".format(name))
    else:
      error = PlayerNotInGameException()
  else:
    error = GameInProgressException()

  if error:
    print_func(game.chan, "{}: Cannot quit: {}".format(name, error))
    raise PlayerNotInGameException()

@atomic
@load_game
def handle_message(game, speaker, msg, s=None):
  speaker = get_player(speaker, s=s)
  msg = msg.lower()
  if game.state == 'running' and speaker:
    if s.query(CoercePlayerGame).filter_by(game = game, player = speaker).one_or_none():
      for cpg in s.query(CoercePlayerGame).filter(CoercePlayerGame.game == game, CoercePlayerGame.player != speaker, CoercePlayerGame.word != None):
        if re.search(cpg.word, msg):
          if cpg.target == speaker:
            cpg.wins = True
          else:
            s.add(CoercePartialPoint(coerce_player_game=cpg, player=speaker))

@atomic
@load_game
def reset_game(game, s=None):
  game.state = 'pregame'
  game.start_time = None
  for cpg in game.coerce_player_games:
    s.query(CoercePartialPoint).filter_by(coerce_player_game=cpg).delete()
    cpg.target = None
    cpg.word = None
    cpg.wins = False

@atomic
@load_game
def start_game(game, print_func=print, s=None):
  if game.state == 'running':
    print_func(game.chan, "Game is already running.")
    raise GameInProgressException()
  if len(game.coerce_player_games) < MIN_PLAYERS:
    print_func(game.chan, "Not enough players. Please wait until at least {} players have joined.".format(MIN_PLAYERS))
    raise NotEnoughPlayersException()

  print_func(game.chan, "Starting game!")
  cpg_list = list(game.coerce_player_games)
  random.shuffle(cpg_list)
  with open(os.path.join(BASE_DIR, 'word_data/base.txt'), 'r') as base:
    word_list = base.read().strip().split('\n')
  random.shuffle(word_list)

  while cpg_list[0].target == None:
    cpg_list[0].target = cpg_list[1].player
    cpg_list[0].word = word_list.pop()
    cpg_list = cpg_list[1:] + cpg_list[:1]

  game.state = 'running'
  game.start_time = time.time()

  for cpg in game.coerce_player_games:
    print_func(cpg.player.name, "Your target is {}. Get them to say {}.".format(cpg.target.name, cpg.word))
  print_func(game.chan, "The game has started!")

@load_game
def print_status(game, user=None, print_func=print, s=None):
  if game.state == 'pregame':
    print_func(game.chan, "The game is not in progress.")
    players = s.query(CoercePlayerGame).filter_by(game = game)
    player_count = players.count()
    players = players.join(CoercePlayerGame.player).order_by(CoercePlayer.name).values(CoercePlayer.name)
    players = map(lambda p: p[0], players)
    print_func(game.chan, "{} players are signed up for the next game: {}".format(player_count, ", ".join(players)))
  elif game.state == 'running':
    print_func(game.chan, "The game has been in progress for {}.".format(game_duration(game, s=s)))

    players = s.query(CoercePlayerGame).filter_by(game = game).filter(CoercePlayerGame.target != None)
    player_count = players.count()
    players = players.join(CoercePlayerGame.player).order_by(CoercePlayer.name).values(CoercePlayer.name)
    players = map(lambda p: p[0], players)
    print_func(game.chan, "{} players are playing: {}".format(player_count, ", ".join(players)))

    players = s.query(CoercePlayerGame).filter_by(game = game, target = None)
    player_count = players.count()
    if player_count > 0:
      players = players.join(CoercePlayerGame.player).order_by(CoercePlayer.name).values(CoercePlayer.name)
      players = map(lambda p: p[0], players)
      print_func(game.chan, "{} players are signed up for the next game: {}".format(player_count, ", ".join(players)))

    if user:
      player = get_player(user, s=s)
      cpg = s.query(CoercePlayerGame).filter_by(player = player, game = game).one_or_none()
      if cpg and cpg.target:
        target = s.query(CoercePlayer).filter_by(id = cpg.target_id).one()
        print_func(player.name, "Your target is {}. Get them to say {}.".format(target.name, cpg.word))
  else:
    print_func(game.chan, "I have no clue what is going on. Why is the game state {}?".format(game.state))

@needs_session
def print_score(channel, user, target, print_func=print, s=None):
  player = get_player(target or user, s=s)
  if player:
    print_func(channel, "{}: {} has {} points.".format(user, player.name, player.score))
  else:
    print_func(channel, "{}: {} has never registered for Coerce.".format(user, target or user))

@needs_session
def print_top(channel, user, number, print_func=print, s=None):
  try:
    number = int(number or 5)
  except ValueError as e:
    print_func(channel, "{}: Please give a valid integer.".format(user))
    return

  query = s.query(CoercePlayer)
  if number < 0:
    query = query.order_by(CoercePlayer.score.asc()).limit(-number)
  else:
    query = query.order_by(CoercePlayer.score.desc()).limit(number)

  for player in query.all():
    print_func(channel, "{} has {} points.".format(player.name, player.score))

@load_game
def check_game_over(game, s=None):
  return bool(s.query(CoercePlayerGame).filter_by(wins = True, game = game).first())

@atomic
@load_game
def finish_game(game, print_func=print, s=None):
  scores = calculate_scores(game, s=s)
  for cpg in s.query(CoercePlayerGame).filter_by(wins = True, game = game):
    print_func(game.chan, "{} has won by getting {} to say {} and received {} points!".format(cpg.player.name, cpg.target.name, cpg.word, scores[None]))
    cpg.player.score += scores[None]

  if s.query(CoercePlayerGame).filter_by(game = game, wins = True).count() == 0:
    print_func(game.chan, "The game ended for some reason. No one won.")

  for cpg in game.coerce_player_games:
    cpg.player.score += scores[cpg.player]
    print_func(game.chan, "{} received {} for coercing non-targets into saying {}.".format(cpg.player.name, scores[cpg.player], cpg.word))
    #TODO: Tell people exactly who said their word.

  reset_game(game, s=s)

@load_game
def calculate_scores(game, s=None):
  total_partials = s.query(CoercePartialPoint).join(CoercePartialPoint.coerce_player_game).filter(CoercePlayerGame.game == game).count()
  total_partials = max(total_partials, 1)
  prize_pool = math.ceil(math.sqrt(total_partials))
  winner_score = max(prize_pool, 1)
  scores = { None: winner_score }
  for cpg in game.coerce_player_games:
    count = s.query(CoercePartialPoint).filter_by(coerce_player_game = cpg).count()
    scores[cpg.player] = min(prize_pool * (count / total_partials), 0.5 * prize_pool)
  return scores

@load_game
def game_duration(game, s=None):
  return str(datetime.timedelta(seconds=int(time.time() - (game.start_time or 0))))
