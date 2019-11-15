import random

import nltk

from ircbot.events import debugout, sendmessage
from ircbot.plugin import IRCPlugin


class WordSwap(IRCPlugin):
    def __init__(self):
        super(WordSwap, self).__init__()

        self.clean_data()

    def generalmessage(self, user, channel, args):
        if user.bot:
            return False
        phrase = nltk.word_tokenize(args)
        tagged = nltk.pos_tag(phrase)

        if random.randint(0, self.count) > 100 and len(phrase) > 10:
            try:
                orig_word, new_word = self.get_replacement(tagged)
                new_phrase = args.replace(orig_word, new_word)
                self.fire(sendmessage(channel, new_phrase))
                self.clean_data()
            except NoSwapError:
                self.fire(debugout("Could not swap {}.".format(tagged)))
        else:
            self.add_data(tagged)
            self.count += 1

    def add_data(self, tagged):
        for word, tag in tagged:
            if len(word) < 5:
                continue
            if tag not in self.data:
                self.data[tag] = []
            self.data[tag].append(word)

    def get_replacement(self, tagged):
        possibles = filter(lambda tag: len(tag[0]) > 5, tagged)
        possibles = list(filter(lambda tag: tag[1] in self.data, possibles))
        while possibles:
            word, tag = random.choice(possibles)
            replacements = list(filter(lambda w: w != word, self.data[tag]))
            if not replacements:
                possibles.remove((word, tag))
                continue
            return word, random.choice(replacements)
        raise NoSwapError("Could not find a word to replace.")

    def clean_data(self):
        self.data = {}
        self.count = 0


class NoSwapError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
