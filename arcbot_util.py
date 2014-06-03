import signal
from contextlib import contextmanager

'''Markov data is stored in the following format: 2 word key. Words separated by ','. Rest of words will be separated by '|'. Only whitespace is linebreaks, which lead to a new key.'''

PHRASE_SPLITTER = '.;:;.'
WORD_SPLITTER = ':;.;:'
TUPLE_SPLITTER = '~|~|~|~'

def load_markov(name):
    #try:
        f = open(name, 'r')
        lines = f.read().split()
        f.close()
        dict = {}
        for i in lines:
            words = i.split(WORD_SPLITTER)
            phrase = tuple(words[0].split(PHRASE_SPLITTER))
            dict[phrase] = []
            for k in words[1:]:
                if TUPLE_SPLITTER in k:
                    dict[phrase].append(tuple(k.split(TUPLE_SPLITTER)))
                else:
                    dict[phrase].append(k)
        print(' Loaded markov dictionary with {} phrases.'.format(len(dict)))
        return dict
    #except:
     #   print ' Could not load file {}.'.format(name)
      #  return {}
        

def save_markov(data, name):
    f = open(name, 'w')
    keys = data.keys()
    for i in keys:
        f.write('{}{}{}'.format(i[0], PHRASE_SPLITTER, i[1]))
        words = data[i]
        for k in words:
            if type(k) is tuple:
                f.write('{}{}{}{}'.format(WORD_SPLITTER, k[0], TUPLE_SPLITTER, k[1]))
            else:
                f.write('{}{}'.format(WORD_SPLITTER, k))
        f.write('\n')
    f.close()

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)