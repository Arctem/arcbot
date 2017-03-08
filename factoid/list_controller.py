from datetime import datetime
from sqlalchemy.sql.expression import func

import ircbot.storage as db
from factoid.list_models import List, ListEntry

@db.atomic
def make_list(creator, channel, name, s=None):
	s.add(creator)
