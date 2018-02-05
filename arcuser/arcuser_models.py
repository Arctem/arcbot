from sqlalchemy import Column, Boolean, Integer, Date, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from ircbot.storage import Base


class ArcUser(Base):
    __tablename__ = 'arcusers'

    id = Column(Integer, primary_key=True)
    base_id = Column(Integer, ForeignKey('users.id'), unique=True)
    base = relationship('User', lazy='joined')
    gender = Column(String, default='name')

    factoids = relationship('Factoid', back_populates='creator')
    items = relationship('Item', back_populates='creator')
