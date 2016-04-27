from ircbot.command import IRCCommand

import phrase_maker.phrase_maker as phrase_maker

import phrase_data

PHRASES = ['cah', 'clickbait', 'cyber', 'dnd', 'fate', 'how', 'loot', 'movie', 'name']

def get_phrase_commands():
    commands = []

    for name in PHRASES:
        commands.append(PhraseCommand(name))
    return commands


class PhraseCommand(IRCCommand):
    def __init__(self, phrase):
        def fun(user, chan, args):
            response = phrase_maker.make(self.phrase, user)
            self.owner.send_privmsg(chan, response)

        IRCCommand.__init__(self, phrase, fun)
        self.phrase = phrase
