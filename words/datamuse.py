import json
from urllib import request, parse

API_ENDPOINT = 'https://api.datamuse.com/words'

MEANS_LIKE = 'ml'
SOUNDS_LIKE = 'sl'
SPELLED_LIKE = 'sp'
SYNONYM = 'rel_syn'
ANTONYM = 'rel_ant'
HYPERNYM = 'rel_spc'
HYPONYM = 'rel_gen'
PERFECT_RHYME = 'rel_rhy'
HOMOPHONE = 'rel_hom'

ENDPOINTS = [
    MEANS_LIKE,
    SOUNDS_LIKE,
    SPELLED_LIKE,
    SYNONYM,
    ANTONYM,
    HYPERNYM,
    HYPONYM,
    PERFECT_RHYME,
    HOMOPHONE
]

def get_words(params):
    params = parse.urlencode(params)
    req = request.Request(API_ENDPOINT + '?' + params,
        headers={ 'User-Agent': "Python's arcbot: The Ultimate Botting Machine!" })
    req = request.urlopen(req)
    return json.loads(req.read().decode("utf-8"))
