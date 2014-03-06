import sys
import random
import pickle

class Markov:
    def __init__(self, filename = None):
        self.forward = {}
        self.backward = {}
        self.start = []
        self.end = []
        self.min_length = 5

    def save(self, filename):
        pickle.dump(self, open(filename, 'wb'), 2) #protocol 2 for compatibility with python2

    def add_string(self, string):
        if type(string) is str:
            string = string.split()
        if len(string) < self.min_length:
            print(' Avoided adding {}-word string to markov data.'.format(len(string)))
            return

        for i in xrange(len(string) - 2):
            #Avoid infinite loops.
            if string[i] == string[i + 1] == string[i + 2]:
                print(' Skipped adding repeated word {} to markov.'.format(string[i]))
                continue

            #Add to forward list.
            phrase = (string[i], string[i + 1])
            if phrase in self.forward:
                self.forward[phrase].append(string[i + 2])
            else:
                self.forward[phrase] = [string[i + 2]]

            #Add to backward list.
            phrase = (string[i + 1], string[i + 2])
            if phrase in self.backward:
                self.backward[phrase].append(string[i])
            else:
                self.backward[phrase] = [string[i]]

        if string[0] == string[0].capitalize():
            self.start.append(string[0])        
        self.end.append(string[-1]) #TODO: check punctuation

    def get_string(self, user = None, output = None):
        if output is None:
            output = [random.choice(self.start + self.end)]
        print(output)
        try:
            if len(output) is 1:
                for_pos = []
                for i in self.forward.keys():
                    if i[0] == output[0]:
                        for_pos.append(i[1])

                back_pos = []
                for i in self.backward.keys():
                    if i[1] == output[0]:
                        back_pos.insert(0, i[0])

                #print(for_pos)
                #print(back_pos)
                if len(for_pos) is not 0:
                    output.append(random.choice(for_pos))

                if len(back_pos) is not 0:
                    output.insert(0, random.choice(back_pos))

            #Add to the end first.
            #for i in xrange(50):
            while output[-1] not in self.end:
                phrase = (output[-2], output[-1])
                if phrase in self.forward.keys():
                    output.append(random.choice(self.forward[phrase]))
                else:
                    print(phrase)
                    print()
                    break

            #Add to beginning.
            #for i in xrange(50):
            while output[0] not in self.start:
                phrase = (output[0], output[1])
                if phrase in self.backward.keys():
                    output.insert(0, random.choice(self.backward[phrase]))
                else:
                    print(phrase)
                    print()
                    break
            return ' '.join(output)
        except IndexError:
            if user:
                return '{}: No valid markov chain.'.format(user)
            else:
                return 'No valid markov chain.'
        
    def convert(self, filename):
        import arcbot_util
        old = arcbot_util.load_markov(filename)
        total = len(old.keys())
        count = 0
        print('Converting {} keys.'.format(total))
        for key in old.keys():
            count += 1
            if count % (total // 10) is 0:
                print('{}/{}'.format(count, total))
            #Ignore some weird error values.
            if len(key) is not 2:
                continue

            #Do special things with start values.
            if key == ('__START__', '__START__'):
                self.start = [x[0] for x in old[key]]
                continue

            #print('{} values for {}.'.format(len(old[key]), key))
            self.forward[key] = []
            for value in old[key]:
                #Add to forward list.
                self.forward[key].append(value)
                back_key = (key[1], value)
                if back_key in self.backward.keys():
                    self.backward[back_key].append(key[0])
                else:
                    self.backward[back_key] = [key[0]]


def load(filename):
    return pickle.load(open(filename, 'rb'))

def main():
    m = load('markov_new.botdat')
    print(m.get_string(user = 'joe', output = sys.argv[1:]))

def reimport():
    m = Markov()
    m.convert('markov.botdat')
    print(m.get_string(['Rob']))
    m.save('markov_new.botdat')
    #print(m.get_string(['Nate']))

    n = load('markov_new.botdat')
    print(n.get_string(['Rob']))
    n.save('markov_new.botdat')

if __name__ == '__main__':
    main()