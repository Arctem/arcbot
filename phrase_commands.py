import imp, phrase_data

from ircbot.command import IRCCommand

import phrase_maker.phrase_maker as phrase_maker


def get_phrase_commands():
    commands = []
    mods = phrase_data.modules

    for mod_file in mods:
        if '__init__' in mod_file:
            continue
        else:
            mod = imp.load_source('test', mod_file)
            phrase_maker.load_module(mod)

            mod_name = mod_file.split('/')[-1].rsplit('.', 1)[0]
            
            commands.append(PhraseCommand(mod_name))
    return commands


class PhraseCommand(IRCCommand):
    def __init__(self, phrase):
        def fun(user, chan, args):
            response = phrase_maker.make(self.phrase, user)
            self.owner.send_privmsg(chan, response)

        IRCCommand.__init__(self, phrase, fun)
        self.phrase = phrase
