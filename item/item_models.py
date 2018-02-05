from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ircbot.storage import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('arcusers.id'))
    creator = relationship('ArcUser', back_populates='items', lazy='joined')
    channel = Column(String)
    creation_time = Column(DateTime)

    name = Column(String)
    deleted = Column(Boolean, default=False)

    def __str__(self):
        return self.name
