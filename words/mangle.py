import json
import random
import threading

import inflection

from ircbot.command import IRCCommand
from ircbot.events import sendmessage

from words import datamuse

# API details here: http://www.datamuse.com/api/
API_ENDPOINT = 'https://api.datamuse.com/words'
BASE_RESULTS = 5
METHODS = {
            datamuse.MEANS_LIKE: BASE_RESULTS*3,
            datamuse.SOUNDS_LIKE: BASE_RESULTS*2,
            datamuse.SPELLED_LIKE: BASE_RESULTS*2,
            datamuse.SYNONYM: BASE_RESULTS,
            datamuse.ANTONYM: BASE_RESULTS,
            datamuse.HYPERNYM: BASE_RESULTS,
            datamuse.HYPONYM: BASE_RESULTS,
            datamuse.PERFECT_RHYME: BASE_RESULTS,
            datamuse.HOMOPHONE: BASE_RESULTS,
}

def mangle(original):
    title = original.istitle()
    human = inflection.humanize(original) == original

    mangled = ' '.join(map(mangle_word, original.split()))

    if title:
        return inflection.titleize(mangled)
    if human:
        return inflection.humanize(mangled)
    return mangled


def mangle_word(word, lc=None, rc=None):
    capital = word.capitalize() == word
    upper = word.isupper()

    results = []
    threads = []
    for method, count in METHODS.items():
        params = {method: word, 'max': count}
        if lc:
            params['lc'] = lc
        if rc:
            params['rc'] = rc
        t = threading.Thread(target=mangle_in_thread, args=(params, results))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if not results:
        return word
    result = random.choice(results)

    if upper:
        return result['word'].upper()
    if capital:
        return result['word'].capitalize()
    return result['word']

def mangle_in_thread(params, parent_list):
    results = datamuse.get_words(params)
    for r in results:
        parent_list.append(r)


class Mangle(IRCCommand):
    def __init__(self):
        super(Mangle, self).__init__('mangle', self.mangle_threaded,
            args='<phrase_to_mangle>',
            description='Mangle a phrase.')

    def mangle(self, user, channel, args):
        try:
            self.fire(sendmessage(channel, '{}: {}'.format(user.nick, mangle(args))))
        except Exception as err:
            self.fire(sendmessage(channel, '{}: Error mangling: {}'.format(user.nick, err)))
            raise

    def mangle_threaded(self, user, channel, args):
        threading.Thread(target=self.mangle, args=(user, channel, args)).start()
