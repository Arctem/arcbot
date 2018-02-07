import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ircbot.storage import Base


class Jobs(enum.Enum):
    barbarian = 'Barbarian'
    rogue = 'Rogue'
    monk = 'Monk'
    wizard = 'Wizard'
    bard = 'Bard'
    druid = 'Druid'


class Tavern(Base):
    __tablename__ = 'taverns'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('arcusers.id'), nullable=False, unique=True)
    owner = relationship('ArcUser', back_populates='tavern', lazy='joined')
    creation_time = Column(DateTime, nullable=False)

    name = Column(String, nullable=False)
    money = Column(Integer, nullable=False)

    resident_hero_id = Column(Integer, ForeignKey('tavern_heroes.id'))
    resident_hero = relationship('TavernHero', back_populates='patron', lazy='joined')

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
    patron = relationship('Tavern', back_populates='resident_hero', lazy='joined')

    def __str__(self):
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


class TavernAdventure(Base):
    __tablename__ = 'tavern_adventure'

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('tavern_heroes.id'), nullable=False)
    hero = relationship('TavernHero', back_populates='adventures', lazy='joined')

    active = Column(Boolean, default=True, nullable=False)


class TavernBoss(Base):
    __tablename__ = 'tavern_boss'

    id = Column(Integer, primary_key=True)
