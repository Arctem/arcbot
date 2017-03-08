from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ircbot.storage import Base

class List(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('arcusers.id'))
    creator = relationship('ArcUser', back_populates='created_lists', lazy='joined')
    owner_id = Column(Integer, ForeignKey('arcusers.id'))
    owner = relationship('ArcUser', back_populates='owned_lists', lazy='joined')
    channel = Column(String)
    creation_time = Column(DateTime)

    name = Column(String)
    locked = Column(Boolean)

class ListEntry(Base):
    __tablename__ = 'list_entries'

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('arcusers.id'))
    creator = relationship('ArcUser', back_populates='list_entries', lazy='joined')
    channel = Column(String)
    creation_time = Column(DateTime)

    value = Column(String)
