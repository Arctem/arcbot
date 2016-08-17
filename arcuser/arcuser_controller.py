import ircbot.storage as db
from ircbot.models import User, Message
import ircbot.user_controller as parent

from arcuser.arcuser_models import ArcUser

@db.atomic
def get_arcuser(user, s=None):
    s.add(user)
    arcuser = s.query(ArcUser).filter_by(base=user).one_or_none()
    return arcuser

@db.atomic
def get_or_create_arcuser(user, s=None):
    s.add(user)
    arcuser = get_arcuser(user, s=s)
    if not arcuser:
        arcuser = ArcUser(base=user)
        s.add(arcuser)
    return arcuser
