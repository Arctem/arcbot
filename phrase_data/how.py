import os

directory = os.path.dirname(__file__)

data = {
    'how': {
        'template': ['You should {verb} {adverb}.'],

        'verb': ['masturbate', 'poop', 'fart'],
        'adverb': open(os.path.join(directory, 'adverbs.txt'), 'r').read().split('\n')
    }
}
