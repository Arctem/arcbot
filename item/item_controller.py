from datetime import datetime
from sqlalchemy.sql.expression import func

import ircbot.storage as db

from item.item_models import Item
from arcuser.arcuser_models import ArcUser


@db.atomic
def add_item(creator, channel, name, s=None):
    s.add(creator)
    item = Item(creator=creator, channel=channel, name=name, creation_time=datetime.now())
    s.add(item)
    return item


@db.needs_session
def get_item(channel, s=None):
    print("Searching" + channel)
    return s.query(Item).filter(Item.channel == channel).filter(Item.deleted == False).order_by(func.random()).first()


@db.atomic
def pop_item(channel, s=None):
    item = get_item(channel, s=s)
    if item:
        item.deleted = True
    return item


@db.atomic
def purge_item(name, s=None):
    return s.query(Item).filter(Item.name == name).delete() > 0


@db.needs_session
def count_items(arcuser=None, include_deleted=False, s=None):
    q = s.query(Item)
    if not include_deleted:
        q = q.filter(Item.deleted == False)
    if arcuser:
        q = q.filter(Item.creator == arcuser)
    return q.count()


@db.needs_session
def get_all_arcusers_with_items(s=None):
    return s.query(ArcUser).join(ArcUser.items).all()
