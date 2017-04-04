from sqlalchemy import Boolean, Column, Integer, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from ircbot.storage import Base


class CoercePlayer(Base):
    __tablename__ = 'coerce_players'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    score = Column(Float, default=0)


class CoerceGame(Base):
    __tablename__ = 'coerce_games'

    id = Column(Integer, primary_key=True)
    chan = Column(String, unique=True)
    state = Column(String, default='pregame')
    start_time = Column(Float, default=None)
    coerce_player_games = relationship('CoercePlayerGame', back_populates='game')


class CoercePlayerGame(Base):
    __tablename__ = 'coerce_player_games'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('coerce_players.id'))
    player = relationship('CoercePlayer', foreign_keys=[player_id])
    game_id = Column(Integer, ForeignKey('coerce_games.id'))
    game = relationship('CoerceGame', back_populates='coerce_player_games')

    target_id = Column(Integer, ForeignKey('coerce_players.id'))
    target = relationship('CoercePlayer', foreign_keys=[target_id])

    word = Column(String, default=None)
    wins = Column(Boolean, default=False)
    partials = relationship('CoercePartialPoint', back_populates='coerce_player_game')

    #UniqueConstraint('player_id', 'game_id')


class CoercePartialPoint(Base):
    __tablename__ = 'coerce_partial_points'

    id = Column(Integer, primary_key=True)
    coerce_player_game_id = Column(Integer, ForeignKey('coerce_player_games.id'))
    coerce_player_game = relationship('CoercePlayerGame', foreign_keys=[coerce_player_game_id], back_populates='partials')
    player_id = Column(Integer, ForeignKey('coerce_players.id'))
    player = relationship('CoercePlayer', foreign_keys=[player_id])
