import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ircbot.storage import Base


class Jobs(enum.Enum):
    Barbarian = 'Barbarian'  # Good against fragile things, bad against evasion
    Rogue = 'Rogue'  # Good against big things
    Monk = 'Monk'  # Good against fast things, bad against things it can't touch
    Wizard = 'Wizard'  # Good against magic things
    Bard = 'Bard'  # Good against old things
    Druid = 'Druid'  # Good against natural things, bad against technology


class HeroActivity(enum.Enum):
    Elsewhere = 1
    CommonPool = 2
    VisitingTavern = 3
    Hired = 4
    Adventuring = 5
    Dead = 6


class Tavern(Base):
    __tablename__ = 'taverns'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('arcusers.id'), nullable=False, unique=True)
    owner = relationship('ArcUser', back_populates='tavern', lazy='joined')
    creation_time = Column(DateTime, nullable=False)

    name = Column(String, nullable=False)
    money = Column(Integer, nullable=False)

    resident_hero_id = Column(Integer, ForeignKey('tavern_heroes.id'))
    resident_hero = relationship('TavernHero', back_populates='patron', lazy='joined', foreign_keys=[resident_hero_id])

    visiting_heroes = relationship('TavernHero', back_populates='visiting',
                                   lazy='joined', foreign_keys='[TavernHero.visiting_id]')

    def __str__(self):
        return self.name


class TavernHero(Base):
    __tablename__ = 'tavern_heroes'

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)
    alive = Column(Boolean, default=True, nullable=False)

    anger = Column(Integer, nullable=False)
    reason = Column(Integer, nullable=False)
    charm = Column(Integer, nullable=False)

    adventures = relationship('TavernAdventure', back_populates='hero')
    patron = relationship('Tavern', back_populates='resident_hero', lazy='joined',
                          uselist=False, foreign_keys=[Tavern.resident_hero_id])

    activity = Column(Enum(HeroActivity), nullable=False)
    visiting_id = Column(Integer, ForeignKey('taverns.id'))
    visiting = relationship('Tavern', back_populates='visiting_heroes', lazy='joined', foreign_keys=[visiting_id])

    def __str__(self):
        return self.name

    def info_string(self):
        return '{name} | {stats} | {jobs}'.format(name=self.name, stats=self.stats_string(), jobs=self.jobs_string())

    def stats_string(self):
        stats = [
            ('A', self.anger),
            ('R', self.reason),
            ('C', self.charm),
        ]
        stats = filter(lambda s: s[1] != 0, stats)
        return ' '.join(map(lambda s: '-' * -s[1] + s[0] if s[1] < 0 else s[0] + '+' * s[1], stats))

    def jobs_string(self):
        return ''


class TavernJobs(Base):
    __tablename__ = 'tavern_jobs'

    id = Column(Integer, primary_key=True)
    job = Column(Enum(Jobs), nullable=False)
    level = Column(Integer, nullable=False, default=0)


class TavernLog(Base):
    __tablename__ = 'tavern_logs'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('arcusers.id'))
    user = relationship('ArcUser', back_populates='tavern_logs', lazy='joined')
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

    active = Column(Boolean, default=True, nullable=False)


class TavernDungeon(Base):
    __tablename__ = 'tavern_dungeons'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    secret = Column(Boolean, default=True, nullable=False)

    floors = relationship('TavernFloor', back_populates='dungeon',
                          order_by='TavernFloor.number', lazy='joined')
    traits = relationship('TavernDungeonTrait', back_populates='dungeon', lazy='joined')

    def __str__(self):
        return self.name


class TavernDungeonTrait(Base):
    __tablename__ = 'tavern_dungeon_traits'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dungeon_id = Column(Integer, ForeignKey('tavern_dungeons.id'), nullable=False)
    dungeon = relationship('TavernDungeon', back_populates='traits', lazy='joined')


class TavernFloor(Base):
    __tablename__ = 'tavern_floors'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    dungeon_id = Column(Integer, ForeignKey('tavern_dungeons.id'), nullable=False)
    dungeon = relationship('TavernDungeon', back_populates='floors', lazy='joined')
    monsters = relationship('TavernMonster', back_populates='floor', lazy='joined')

    def __str__(self):
        return "{} F{}".format(self.dungeon.name, self.number)


class TavernMonster(Base):
    __tablename__ = 'tavern_monsters'

    id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False)
    stock = Column(String, nullable=False)
    modifier = Column(String, nullable=True)

    floor_id = Column(Integer, ForeignKey('tavern_floors.id'), nullable=False)
    floor = relationship('TavernFloor', back_populates='monsters', lazy='joined')

    def __str__(self):
        species = self.stock
        if self.modifier:
            species = self.modifier + " " + species
        return "L{} {}".format(self.level, species)
