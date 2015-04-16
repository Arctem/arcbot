import sys
import random
import pickle
import re

from ircbot.command import IRCCommand

class Markov(IRCCommand):
    def __init__(self, filename = None):
        IRCCommand.__init__(self, 'markov', None)
        self.filename = filename
        self.forward = {}
        self.backward = {}
        self.start = []
        self.end = []
        self.min_length = 5

        self.triggers['PRIVMSG'] = (9, self.privmsg)

        if self.filename:
            self.load()

    def privmsg(self, prefix, args):
        channel = args[0]
        args = args[1]
        user = prefix.split('!')[0]

        reg = re.compile('^{}[:,] markov'.format(self.owner.nick))
        trig = bool(reg.match(args))

        if trig:
            msg = self.get_string(user, args.split()[2:] or None)
            self.owner.send_privmsg(channel, msg)

        elif len(args.split()) > self.min_length and\
                self.owner.nick not in args.split()[0]:
            self.add_string(args)
            if self.filename:
                self.save()

        return trig

    def save(self):
        data = [self.forward, self.backward, self.start, self.end]
        with open(self.filename, 'wb') as load_file:
            pickle.dump(data, load_file)

    def load(self):
        try:
            with open(self.filename, 'rb') as load_file:
                data = pickle.load(load_file)
            self.forward, self.backward, self.start, self.end = data
        except FileNotFoundError:
            print(' Could not load markov file {}.'.format(self.filename))

    def add_string(self, string):
        if type(string) is str:
            string = string.split()
        if len(string) < self.min_length:
            print(' Avoided adding {}-word string to markov data.'.format(len(string)))
            return

        for i in range(len(string) - 2):
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
        #print(output)
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

                #print('Foward: {}'.format(for_pos))
                #print('Backward: {}'.format(back_pos))
                if len(for_pos) is not 0:
                    output.append(random.choice(for_pos))

                if len(back_pos) is not 0:
                    output.insert(0, random.choice(back_pos))

            #print('In end:', output[-1] in self.end)
            #print('In begin:', output[0] in self.start)

            count = 0
            #Add to the end first.
            while output[-1] not in self.end or count < 5:
                phrase = (output[-2], output[-1])
                if phrase in self.forward.keys():
                    output.append(random.choice(self.forward[phrase]))
                    count += 1
                else:
                    #print(phrase)
                    #print()
                    break

            count = 0
            #Add to beginning.
            while output[0] not in self.start or count < 5:
                phrase = (output[0], output[1])
                if phrase in self.backward.keys():
                    output.insert(0, random.choice(self.backward[phrase]))
                    count += 1
                else:
                    #print(phrase)
                    #print()
                    break
            return ' '.join(output)
        except IndexError:
            if user:
                return '{}: No valid markov chain.'.format(user)
            else:
                return 'No valid markov chain.'
