import json
import random
import threading
from urllib import request, parse

import inflection

from ircbot.command import IRCCommand
from ircbot.events import sendmessage

# API details here: http://www.datamuse.com/api/
API_ENDPOINT = 'https://api.datamuse.com/words'
MAX_RESULTS = 10

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

    param = random.choice(['ml', 'sl', 'sp'])
    params = {param: word, 'max': MAX_RESULTS}
    if lc:
        params['lc'] = lc
    if rc:
        params['rc'] = rc

    params = parse.urlencode(params)
    req = request.Request(API_ENDPOINT + '?' + params,
        headers={ 'User-Agent': "Python's arcbot: The Ultimate Botting Machine!" })
    req = request.urlopen(req)

    results = json.loads(req.read().decode("utf-8"))
    if not results:
        return word
    result = random.choice(results)

    if upper:
        return result['word'].upper()
    if capital:
        return result['word'].capitalize()
    return result['word']

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
