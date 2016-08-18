from datetime import datetime
from sqlalchemy.sql.expression import func

import ircbot.storage as db
from factoid.factoid_models import Factoid

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
