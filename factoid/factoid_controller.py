from datetime import datetime
from sqlalchemy.sql.expression import func

import ircbot.storage as db

from factoid.factoid_models import Factoid
from arcuser.arcuser_models import ArcUser

@db.atomic
def save_factoid(creator, channel, trigger, reply, verb, s=None):
    s.add(creator)
    factoid = Factoid(creator=creator, trigger=trigger, reply=reply, verb=verb)
    s.add(factoid)
    return factoid

#returns a random factoid that matches the given trigger
@db.needs_session
def find_factoid(trigger, channel, s=None):
    return s.query(Factoid).filter(Factoid.trigger == trigger).order_by(func.random()).first()

@db.needs_session
def get_factoid(id, s=None):
    return s.query(Factoid).get(id)

@db.atomic
def delete_factoid(id, s=None):
    return s.query(Factoid).filter(Factoid.id == id).delete() > 0

@db.needs_session
def count_factoids(arcuser=None, s=None):
	q = s.query(Factoid)
	if arcuser:
		q = q.filter(Factoid.creator == arcuser)
	return q.count()

@db.needs_session
def get_all_arcusers_with_factoids(s=None):
	return s.query(ArcUser).join(ArcUser.factoids).all()
