import nltk
import random

from ircbot.plugin import IRCPlugin

class WordSwap(IRCPlugin):
    def __init__(self):
        IRCPlugin.__init__(self)

        self.triggers['PRIVMSG'] = self.privmsg
        self.clean_data()

    def privmsg(self, prefix, args):
        channel = args.pop(0)
        user = prefix.split('!')[0]

        phrase = nltk.word_tokenize(args[0])
        tagged = nltk.pos_tag(phrase)

        if random.randint(0, self.count) > 100:
            new_phrase = self.replace_word(tagged)
            self.owner.send_privmsg(channel, new_phrase)
            self.clean_data()
            return True
        else:
            self.add_data(tagged)

        return False

    def add_data(self, tagged):
        for word, tag in tagged:
            if tag not in self.data:
                self.data[tag] = []
            self.data[tag].append(word)

    def replace_word(self, tagged):
        while True:
            index = random.randrange(len(tagged))
            word = tagged[index][0]
            tag = tagged[index][1]
            if tag in self.data:
                replace = random.choice(self.data[tag])
                if replace != word:
                    phrase = list(map(lambda w: w[1], tagged))
                    phrase[index] = replace
                    return ' '.join(phrase)

    def clean_data(self):
        self.data = {}
        self.count = 0
