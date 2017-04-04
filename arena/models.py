from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session

from ircbot.storage import Base


class ArenaObject(Base):
    __tablename__ = 'arena_objects'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    attributes = relationship('ArenaAttribute', back_populates='subject', lazy='joined')

    owner_id = Column(Integer, ForeignKey('arena_objects.id'))
    owner = relationship('ArenaObject', back_populates='objects', lazy='joined', remote_side=[id])
    objects = relationship('ArenaObject', back_populates='owner', lazy='joined')

    employer_id = Column(Integer, ForeignKey('arcusers.id'))
    employer = relationship('ArcUser', lazy='joined')

    # probably a bad idea
    def __getattr__(self, name):
        try:
            return getattr(super(ArenaObject, self), name)
        except AttributeError:
            possibles = list(filter(lambda a: a.attribute == name, list(self.attributes)))  # .filter_by(attribute=name)
            if len(possibles) == 1:
                return possibles[0]
            elif len(possibles) > 1:
                return possibles
            raise

    # definitely a bad idea
    def a__setattr__(self, name, value):
        try:
            setattr(super(ArenaObject, self), name, value)
        except AttributeError:
            s = Session.object_session(self)
            possibles = s.query(ArenaAttribute).filter_by(subject=self, attribute=name)
            if possibles.count() == 1:
                possibles.first().value = value
            else:
                possible = ArenaAttribute(subject=self, attribute=name, value=value)


class ArenaAttribute(Base):
    __tablename__ = 'arena_attributes'

    id = Column(Integer, primary_key=True)

    subject_id = Column(Integer, ForeignKey('arena_objects.id'))
    subject = relationship('ArenaObject', back_populates='attributes', lazy='joined')
    attribute = Column(String)
    value = Column(String)
