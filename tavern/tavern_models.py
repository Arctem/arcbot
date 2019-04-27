import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String, DateTime, ForeignKey
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
    owner = relationship('ArcUser', back_populates='tavern', lazy='joined')
    creation_time = Column(DateTime, nullable=False)

    name = Column(String, nullable=False)
    money = Column(Integer, nullable=False)

    resident_hero_id = Column(Integer, ForeignKey('tavern_heroes.id'))
    resident_hero = relationship('TavernHero', back_populates='patron', lazy='joined', foreign_keys=[resident_hero_id])

    visiting_heroes = relationship('TavernHero', back_populates='visiting',
                                   lazy='joined', foreign_keys='[TavernHero.visiting_id]')

    hired_hero_id = Column(Integer, ForeignKey('tavern_heroes.id'))
    hired_hero = relationship('TavernHero', back_populates='employer', lazy='joined', foreign_keys=[hired_hero_id])
    adventures = relationship('TavernAdventure', back_populates='employer', lazy='joined')

    def __str__(self):
        return self.name

    def details_strings(self):
        info = []
        info.append('{name} is owned by {owner} and was founded on {creation_time:%d %B, %Y}.'.format(
            name=self.name, owner=self.owner, creation_time=self.creation_time))
        info.append('{gold} gold'.format(gold=self.money))
        if self.resident_hero is not None:
            info.append('Resident hero is {hero}.'.format(hero=self.resident_hero.name))
        if len(self.visiting_heroes) == 1:
            info.append('{} is visiting.'.format(self.visiting_heroes[0].name))
        elif len(self.visiting_heroes) > 1:
            info.append('{} are visiting.'.format(', '.format(self.visiting_heroes)))
        return info


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
    alive = Column(Boolean, default=True, nullable=False)
    cost = Column(Integer, nullable=False)

    primary_class = Column(String, nullable=False)
    secondary_class = Column(String, nullable=False)
    level = Column(Integer, nullable=False)

    adventures = relationship('TavernAdventure', back_populates='hero', lazy='joined')
    patron = relationship('Tavern', back_populates='resident_hero', lazy='joined',
                          uselist=False, foreign_keys=[Tavern.resident_hero_id])

    activity = Column(Enum(HeroActivity), nullable=False)
    visiting_id = Column(Integer, ForeignKey('taverns.id'))
    visiting = relationship('Tavern', back_populates='visiting_heroes', lazy='joined', foreign_keys=[visiting_id])
    employer = relationship('Tavern', uselist=False, back_populates='hired_hero', lazy='joined', foreign_keys=[Tavern.hired_hero_id])

    def __str__(self):
        return '{} the {}'.format(self.name, self.epithet)

    def details_strings(self):
        info = []
        info.append(self.name)
        if not self.alive:
            info.append('Dead.')
        info.append(self.activity_string())
        info.append(self.level_string())
        info.append('Demands {cost} gold.'.format(cost=self.cost))
        if self.patron:
            info.append('Patron of {patron}.'.format(patron=self.patron.name))
        info.append('Has been on {adv_count} adventures.'.format(adv_count=len(self.adventures)))
        return info

    def info_string(self):
        return '{name} | {stats}'.format(name=self.name, stats=self.level_string())

    def level_string(self):
        if self.secondary_class is not None:
            return 'level {lvl} {primary} {secondary}'.format(lvl=self.level, primary=self.primary_class.capitalize(), secondary=self.secondary_class.capitalize())
        return 'level {lvl} {primary}'.format(lvl=self.level, primary=self.primary_class.capitalize())

    def activity_string(self):
        return '{activity} at {location}'.format(activity=self.activity, location=self.visiting)


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

    employer_id = Column(Integer, ForeignKey('taverns.id'), nullable=False)
    employer = relationship('Tavern', back_populates='adventures', lazy='joined')

    dungeon_id = Column(Integer, ForeignKey('tavern_dungeons.id'), nullable=False)
    dungeon = relationship('TavernDungeon', back_populates='adventures', lazy='joined')

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

    adventures = relationship('TavernAdventure', back_populates='dungeon', lazy='joined')

    def __str__(self):
        return self.name

    def details_strings(self):
        info = []
        info.append('{} has {} floors.'.format(self.name, len(self.floors)))
        info.append('It is currently active.' if self.active else 'It is not currently active.')
        # TODO: Mention heroes inside.
        return info


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
