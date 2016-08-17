from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ircbot.storage import Base

class Factoid(Base):
    __tablename__ = 'factoids'

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('arcusers.id'))
    creator = relationship('ArcUser', back_populates='factoids', lazy='joined')
    channel = Column(String)
    creation_time = Column(DateTime)

    trigger = Column(String)
    reply = Column(String)
    #special verbs are <reply>, <action>, and <'s>. All others are used as stored.
    verb = Column(String)
