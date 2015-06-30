import nltk
import random

from ircbot.plugin import IRCPlugin

class WordSwap(IRCPlugin):
    def __init__(self):
        IRCPlugin.__init__(self)

        self.triggers['PRIVMSG'] = (0, self.privmsg)
        self.clean_data()

    def privmsg(self, prefix, args):
        channel = args.pop(0)
        user = prefix.split('!')[0]

        phrase = nltk.word_tokenize(args[0])
        tagged = nltk.pos_tag(phrase)

        if random.randint(0, self.count) > 50 and len(phrase) > 10:
            try:
                orig_word, new_word = self.get_replacement(tagged)
                new_phrase = args[0].replace(orig_word, new_word)
                self.owner.send_privmsg(channel, new_phrase)
                self.clean_data()
                return True
            except NoSwapError:
                print("Could not swap {}.".format(tagged))
                return False
        else:
            self.add_data(tagged)
            self.count += 1

        return False

    def add_data(self, tagged):
        for word, tag in tagged:
            if len(word) < 5:
                continue
            if tag not in self.data:
                self.data[tag] = []
            self.data[tag].append(word)

    def get_replacement(self, tagged):
        possibles = list(filter(lambda tag: len(tag[0]) > 5, tagged))
        while possibles:
            word, tag = random.choice(possibles)
            if len(word) < 5 or tag not in self.data:
                possibles.remove((word, tag))
                continue
            return word, random.choice(self.data[tag])
        raise NoSwapError("Could not find a word to replace.")

    def clean_data(self):
        self.data = {}
        self.count = 0


class NoSwapError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
