from urllib import urlencode
from urllib2 import urlopen
from json import loads

API_ENDPOINT = 'https://api.datamuse.com/words'

MEANS_LIKE = 'ml'
SOUNDS_LIKE = 'sl'
SPELLED_LIKE = 'sp'
SYNONYMS = 'rel_syn'
ANTONYMS = 'rel_ant'
HYPERNYMS = 'rel_spc'
HYPONYMS = 'rel_gen'
PERFECT_RHYMES = 'rel_rhy'
HOMOPHONES = 'rel_hom'

ENDPOINTS = [
    MEANS_LIKE,
    SOUNDS_LIKE,
    SPELLED_LIKE,
    SYNONYMS,
    ANTONYMS,
    HYPERNYMS,
    HYPONYMS,
    PERFECT_RHYMES,
    HOMOPHONES
]

def get_words(params):
    request = urlopen(API_ENDPOINT + '?' + urlencode(params))
    return loads(req.read().decode("utf-8"))
