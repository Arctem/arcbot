from ircbot.events import sendmessage, sendaction
from ircbot.command import IRCCommand

from arena import controller
from arcuser import arcuser_controller


class Arena(IRCCommand):

    def __init__(self):
        super(Arena, self).__init__('arena', self.arena,
                                    args='dunno yet',
                                    description='overly ambitious, probably')

    def arena(self, user, channel, message):
        arcuser = arcuser_controller.get_or_create_arcuser(user)
        cmd = message.split()
        if len(cmd) > 0:
            cmd = cmd[0]
        if cmd == 'create':
            new_hero = controller.create_hero(arcuser)
            self.fire(sendmessage(channel, "{}: Created {}.".format(user.nick, new_hero.name)))
        else:
            hero = controller.get_hero()
            self.fire(sendmessage(channel, "{}: You own {}. They are a {}.".format(user.nick, hero.name, hero.race)))
