import enum

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from ircbot.storage import Base


class HeroActivity(enum.Enum):
    Elsewhere = 1
    CommonPool = 2
    VisitingTavern = 3
    Hired = 4
    Adventuring = 5
    Dead = 6


class TavernValue(Base):
    __tablename__ = 'tavern_values'

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=True, unique=True)
    value = Column(String)


class Tavern(Base):
    __tablename__ = 'taverns'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('arcusers.id'), nullable=False, unique=True)
    owner = relationship('ArcUser', back_populates='tavern')
    creation_time = Column(DateTime, nullable=False)

    name = Column(String, nullable=False)
    money = Column(Integer, nullable=False)

    resident_hero_id = Column(Integer, ForeignKey('tavern_heroes.id'))
    resident_hero = relationship('TavernHero', back_populates='patron', foreign_keys=[resident_hero_id])

    visiting_heroes = relationship('TavernHero', back_populates='visiting',
                                   foreign_keys='[TavernHero.visiting_id]')

    hired_hero_id = Column(Integer, ForeignKey('tavern_heroes.id'))
    hired_hero = relationship('TavernHero', back_populates='employer', foreign_keys=[hired_hero_id])
    adventures = relationship('TavernAdventure', back_populates='employer')

    def __str__(self):
        return self.name


class TavernKeyStore(Base):
    __tablename__ = 'tavern_keystore'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=False)


class TavernHero(Base):
    __tablename__ = 'tavern_heroes'

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)
    epithet = Column(String, nullable=False)
    primary_class = Column(String, nullable=False)
    secondary_class = Column(String, nullable=False)

    alive = Column(Boolean, default=True, nullable=False)
    injured = Column(Boolean, default=False, nullable=False)
    level = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)

    adventures = relationship('TavernAdventure', back_populates='hero')
    patron = relationship('Tavern', back_populates='resident_hero',
                          uselist=False, foreign_keys=[Tavern.resident_hero_id])

    activity = Column(Enum(HeroActivity), nullable=False)
    visiting_id = Column(Integer, ForeignKey('taverns.id'))
    visiting = relationship('Tavern', back_populates='visiting_heroes', foreign_keys=[visiting_id], post_update=True)
    employer = relationship('Tavern', uselist=False, back_populates='hired_hero', foreign_keys=[Tavern.hired_hero_id])

    def __str__(self):
        return '{} the {}'.format(self.name, self.epithet)

    def info_string(self):
        return '{name} | {stats}'.format(name=self.name, stats=self.level_string())

    def level_string(self):
        if self.secondary_class is not None:
            return 'level {lvl} {primary} {secondary}'.format(lvl=self.level, primary=self.primary_class.capitalize(), secondary=self.secondary_class.capitalize())
        return 'level {lvl} {primary}'.format(lvl=self.level, primary=self.primary_class.capitalize())


class TavernLog(Base):
    __tablename__ = 'tavern_logs'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('arcusers.id'))
    user = relationship('ArcUser', back_populates='tavern_logs')
    text = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    sent = Column(Boolean, default=False, nullable=False)

    def __str__(self):
        return self.text


class TavernAdventure(Base):
    __tablename__ = 'tavern_adventures'

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('tavern_heroes.id'), nullable=False)
    hero = relationship('TavernHero', back_populates='adventures', lazy='joined')

    employer_id = Column(Integer, ForeignKey('taverns.id'), nullable=False)
    employer = relationship('Tavern', back_populates='adventures', lazy='joined')

    dungeon_id = Column(Integer, ForeignKey('tavern_dungeons.id'), nullable=False)
    dungeon = relationship('TavernDungeon', back_populates='adventures', lazy='joined')
    floor_id = Column(Integer, ForeignKey('tavern_floors.id'), nullable=False)
    floor = relationship('TavernFloor', back_populates='adventures', lazy='joined')

    money_gained = Column(Integer, nullable=False)
    active = Column(Boolean, default=True, nullable=False)


class TavernDungeon(Base):
    __tablename__ = 'tavern_dungeons'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    secret = Column(Boolean, default=True, nullable=False)

    floors = relationship('TavernFloor', back_populates='dungeon',
                          order_by='TavernFloor.number')
    traits = relationship('TavernDungeonTrait', back_populates='dungeon', lazy='joined')

    adventures = relationship('TavernAdventure', back_populates='dungeon')

    def __str__(self):
        return self.name


class TavernDungeonTrait(Base):
    __tablename__ = 'tavern_dungeon_traits'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dungeon_id = Column(Integer, ForeignKey('tavern_dungeons.id'), nullable=False)
    dungeon = relationship('TavernDungeon', back_populates='traits', lazy='joined')

    def __str__(self):
        return self.name


class TavernFloor(Base):
    __tablename__ = 'tavern_floors'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    dungeon_id = Column(Integer, ForeignKey('tavern_dungeons.id'), nullable=False)
    dungeon = relationship('TavernDungeon', back_populates='floors')
    monsters = relationship('TavernMonster', back_populates='floor')
    adventures = relationship('TavernAdventure', back_populates='floor')

    def __str__(self):
        return "{} F{}".format(self.dungeon.name, self.number)


class TavernMonster(Base):
    __tablename__ = 'tavern_monsters'

    id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False)
    stock = Column(String, nullable=False)
    modifier = Column(String, nullable=True)

    floor_id = Column(Integer, ForeignKey('tavern_floors.id'), nullable=False)
    floor = relationship('TavernFloor', back_populates='monsters')

    def __str__(self):
        species = self.stock
        if self.modifier:
            species = self.modifier + " " + species
        return "L{} {}".format(self.level, species)
