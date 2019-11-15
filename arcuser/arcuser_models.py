from sqlalchemy import (Boolean, Column, Date, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import backref, relationship

from ircbot.storage import Base


class ArcUser(Base):
    __tablename__ = 'arcusers'

    id = Column(Integer, primary_key=True)
    base_id = Column(Integer, ForeignKey('users.id'), unique=True)
    base = relationship('User', lazy='joined')
    gender = Column(String, default='name')

    factoids = relationship('Factoid', back_populates='creator')
    items = relationship('Item', back_populates='creator')
    tavern = relationship('Tavern', back_populates='owner')
    tavern_logs = relationship('TavernLog', back_populates='user')

    def __str__(self):
        return self.base.name
