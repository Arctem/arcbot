from ircbot.command import IRCCommand
from ircbot.events import sendmessage

import phrase_maker.phrase_maker as phrase_maker

import phrase_data

PHRASES = ['clickbait', 'cyber', 'dnd', 'fate', 'how', 'insult', 'loot', 'movie', 'name', 'plan', 'ration']

def get_phrase_commands():
    commands = []

    for name in PHRASES:
        commands.append(PhraseCommand(name))
    return commands


class PhraseCommand(IRCCommand):
    def __init__(self, phrase):
        super(PhraseCommand, self).__init__(phrase, self.fun)
        self.phrase = phrase

    def fun(self, user, chan, args):
        response = phrase_maker.make(self.phrase, args or user.nick)
        self.fire(sendmessage(chan, response))
