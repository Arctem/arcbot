import urllib2
import json
import random
from datamuse.datamuse import Datamuse

def get_rhyme(word):
    request = Datamuse.get_perfect_rhymes(word)
    results = json.loads(request.read().decode("utf-8"))
    return str(random.choice(results)['word'])

def define_word(word):
    request = urllib2.urlopen('http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=' + word)
    results = json.loads(request.read().decode("utf-8"))
    entry = random.choice(results['results'])
    definition = random.choice(entry['senses'][0]['definition'])
    return str(definition)

def define_command(args):
    word = args.split()[0]

    rhyme_word = get_rhyme(word)
    while rhyme_word == word:
        rhyme_word = get_rhyme(word)

    definitions = [define_word(word), define_word(rhyme_word)]
    while definitions[0] == definitions[1]:
        definitions = [define_word(word), define_word(rhyme_word)]

    random.shuffle(definitions)
    response = "It either means: '" + definitions[0] + "'\nOr: '" + definitions[1] + "'"
    return response

class Define(IRCCommand):
    def __init__(self):
        super(Define, self).__init__('define', self.define,
            args='<word_to_define>',
            description='Define a word. Probably.')
        Datamuse()

    def define(self, user, channel, args):
        try:
            self.fire(sendmessage(channel, '{}: {}'.format(user.nick, define_command(args))))
        except Exception as err:
            self.fire(sendmessage(channel, '{}: Error defining: {}'.format(user.nick, err)))
            raise
