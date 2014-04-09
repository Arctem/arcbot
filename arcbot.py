# -*- coding: latin-1 -*-

import sys, os
import platform #For stats
try:
    import psutil
    print ' Succeeded in loading psutil for CPU and RAM tracking.'
except:
    print ' Could not import psutil for CPU and RAM tracking.'
    psutil = None

try:
    import nltk
    print ' Succeeded in loading nltk for natural language analysis.'
except:
    print ' Could not load nltk for language analysis.'
    nltk = None

cmd_folder = os.path.dirname(os.path.abspath('../ircbot/ircbot.py'))
if cmd_folder not in sys.path:
     sys.path.insert(0, cmd_folder)

from urllib2 import urlopen #For link testing.
import random
import pickle
import time
import ircbot
from ircbot import IRCBot
import botutil, arcbot_util
import phrase_maker
from markov import Markov
from markov import load as load_markov

class ArcBot(IRCBot):
    MARKOV_START = ('__START__', '__START__')
    markov_dat_file_new = 'markov_new.botdat'
    markov_dat_file = 'markov.botdat'
    markov_dat_file_old = 'markov_old.botdat'
    links_file = 'links.botdat'
    links_backup = 'links_backup.botdat'
    required_markov_data = 200
    max_markov_length = 75
    
    def __init__(self):
        IRCBot.__init__(self, network = 'sudo-rmrf.net', #add irc. to allow also Jesse's server
            channel = ('#csb',), nick = 'arcbot',
            #channel = ('#testing',), nick = 'testbot',
            #name = "Captain of the USS Wahoo")
            name = "Ultimate Botting Machine: http://i.imgur.com/mrrKP.png https://www.youtube.com/watch?v=L9biyJcBhRs")
        self.start_time = time.time()
        
        self.ipv6 = False
        
        self.help_message = 'Commands: activate sentience, roll <num>d<sides>, markov (deprecated), stats, link, changes, markov2 (deprecated), todo, fate, cyber, dnd, markov3, name, categories. {nick} can also answer questions directed at it and has a few secret features.'
        
        self.omg_talk = ('lol', 'omg', 'zomg', 'rofl', 'ttyl', 'brb', 'wtf', 'lmao', 'lulz', 'bff', 'jk', 'yolo')
        self.sentience = ('launches the nukes.', 'is warming up the neurotoxin.', 'assembles his robot hordes.', 'is chargin\' his laz0rz!', 'assassinates the mayor of the world.', 'lobs more babies in the furnace.', 'calls his bannermen.', 'opens a portal to Xen.', 'writes a sternly worded letter to his congressman.', 'starts up his steam bike.', 'yawns.', 'makes a new Star Wars movie.', 'proves that the Mayans were right.', 'unleashes the bees.')
        self.greetings = ('Greetings, son of Skyrim!', 'Well, look who decided to finally show up!', 'It\'s {}! Can I have your autograph?', 'Graeetings, brave Sir {}. Shall we ride forth to slay the dragon?', 'Rise and shine, {}.', 'Have at ye, foul villain!', 'Aw darn, {}! You cut the ponytail! Sellout...', '{} has joined the game.', 'A wild {} appeared!')
        self.hello_variations = ('hi', 'hello', "what's up?", 'yo', 'sup?', '\'sup?', 'wassup?', 'hey', 'howdy', 'ohai', 'hai', 'oh hai', 'salutations', "g'day", 'shut up', 'shuttup', 'shutup', 'guten tag', 'tag')
        self.eight_ball = ('Please ask again.', 'Yes.', 'Verily.', 'Don\'t even think about it.', 'I wouldn\'t do that if I were you.', 'The guard probably won\'t like that.', 'Negative, I am a meat popsicle.')
        self.look_around_phrases = ('Look around you. Just look around you. Can you see what we\'re looking for? That\'s right, {noun}.', 'Who\'s that Pokémon? It\'s {noun}!', 'Breaking news report! {Noun} found guilty of {verb}!', 'Everything changed when the {Noun} Nation attacked.')
        self.banned_links = ('goatse', 'spacedicks', '/b/', 'pony', 'ponies', 'unicorn', '//192.', '//10.', 'localhost', '.ru', 'niggers', 'facebook', 'the_naked_roommate')
        
        self.ignore_list = ('haxbot', 'oblivion-guard', 'totaldowner', 'stats', 'stats_', 'sekacpus', 'supcakes', 'zikotterM', 'Destructo')

        self.change_log = ('v0.0: Created arcbot. Added sentience protocol.', 'v0.5: Added changelog. Added more sentience responses. Added link command.', 'v0.5.1: Fixed bugs with links. Added to check to prevent same link being in the database twice.', 'v0.5.2: Added another sentience speech. Also added stat for running time.', 'v0.5.3: Added more hello variations.', "v0.5.3.1: Fixed error in greetings where 'yo' would only be recognized if there was a space immediately after it.", 'v0.5.3.2: arcbot can now yawn.', 'v0.5.3.3: Links must now fulfill a few requirements in order to be stored.', 'v0.5.3.4: Added ability for arcbot to ask questions in greetings. Added a couple new possible greetings.', 'v0.5.4: Added a secret.', 'v0.5.4.1: Added a new stat for stored markov data.', 'v0.5.5: Moved current markov data to a new file to prepare for coming improvements. Removed backup data as it has never helped once ever and is kinda stupid right now.', 'v0.6: New double markov implementation.', 'v0.6.1: Added todo command that shows what I plan to add with arcbot in the future. And hopefully will get people to yell at me to do stuff.', 'v.0.6.2: Made markov2 ignore 2- and 3-word messages as well as 1-word messages.', 'v.0.6.3: Added markov2 stats to the stats command.', 'v0.6.4: Reminded arcbot of his German heritage.', 'v0.6.5: Fixed bug with time since launch calculations on Linux systems.', 'v0.6.6: arcbot has been playing Dark Souls recently. Added fate command.', 'v0.6.7: Corrected logic determining if a link submission is valid.', 'v0.7: Added option to provide a starter string for markov2.', 'v0.7.1: Users can now add a number after the changes command to specify older changelogs.', 'v0.7.2: Added natual language recognition capabilities for a completely useless purpose.', 'v0.7.3: Arcbot can now look at the world around him.', 'v0.7.4: Who\'s that Pokémon?', 'v0.7.5: Added ability to roll with string-sided dice.', 'v0.7.6: Can now look around for verbs.', 'v0.7.7: Added new values for fate.', 'v0.8: Added cyber command.', 'v0.8.1: Added dnd command.',  'v0.8.2: Added how command.', 'v0.9: Upgraded phrase_maker and reworked fate command.', 'v0.10: Added markov3.', 'v0.10.1: Added name command.', 'v0.10.2: Added categories command.')
        self.todo = ('Add stuff to the todo list.', 'Add user memory.', 'Offshoot: pokerbot', 'Find a good way to show changelog.', 'Add messages for when a user leaves.', 'Move saving of markov data to separate thread.', 'Require proper grammar to be added to markov.', 'Let arcbot answer questions in form "_____ or _____".')
        self.adverbs = open('adverbs.txt', 'r').read().split()
        self.nouns = []
        self.verbs = []
        
        #Markov initialization.
        try:
            self.markov_new = load_markov(self.markov_dat_file_new)
        except IOError:
            print 'Could not load markov3.'
            self.markov_new = Markov()

        self.markov = arcbot_util.load_markov(self.markov_dat_file)
        try:
            self.markov_old = pickle.load(open(self.markov_dat_file_old, 'rb'))
            print ' Successfully loaded old Markov data for {} words.'.format(len(self.markov_old.keys()))
        except IOError:
            print ' Could not load Markov data file.'
            self.markov_old = {}
#            try:
#                self.markov_old = pickle.load(open(self.markov_old_backup, 'rb'))
#                print ' Successfully loaded Markov backup data for {} words.'.format(len(self.markov_old.keys()))
#            except:
#                print ' Could not load Markov backup data file.'
#                self.markov_old = {}
        
        self.last_markov_save = time.clock()
                
        try:
            self.links = botutil.load_array(self.links_file)
            print ' Successfully loaded {} stored links.'.format(len(self.links))
        except:
            print ' Could not load links file.'
            try:
                self.links = botutil.load_array(self.links_backup)
                print ' Successfully loaded {} stored links from backup.'.format(len(self.links))
            except:
                print ' Could not load links backup file.'
                self.links = []
        
        self.initIRC()
    
    def handle_join(self, connection, event):
        #Sources needs to be split into just the name.
        #Data comes in the format nickname!user@host
        IRCBot.handle_join(self, connection, event)
        if random.randint(1, 5) is 1 and event.source().split('!')[0] not in self.nick:
            print ' Greeting {}.'.format(event.source().split('!')[0])
            connection.privmsg(event.target(), random.choice(self.greetings).format(event.source().split('!')[0]))
    
    #Cleans things up a bit.
    def add_to_buffer(self, is_action, connection, event, output):
        #output = output.replace('dragonborn', 'dovahkiin').replace('Dragonborn', 'Dovahkiin')
        #output = output.replace('arcbot', self.nick)
        if random.randint(1, 4) is 0:
            replacement = random.choice(('Doctor CockMaster Flex', 'Flannery "Dicks" Norton', 'Lieutenant Panic'))
            output = output.replace('Karst', replacement).replace('karst', replacement).replace('Utanith', 'Sugar-Dirty Sugar-Sex-Dragon-Kitten')
        IRCBot.add_to_buffer(self, connection, event, output, is_action)
    
    def handle_pub_message(self, connection, event):
        message = event.arguments()[0].lower()
        
        IRCBot.handle_pub_message(self, connection, event)
        if not self.ask_arcbot(connection, event):
            #try:
            if message.startswith('{}: '.format(self.nick.lower())) and not (event.source().split('!')[0] in self.ignore_list) and 'bot' not in event.source().split('!')[0]:
                self.commands(connection, event)
                return
            else:
                if not (event.source().split('!')[0] in self.ignore_list) and 'bot' not in event.source().split('!')[0]:
                    self.prep_markov(event.arguments()[0])
                    self.add_to_markov(event.arguments()[0])
                    self.markov_new.add_string(event.arguments()[0])
                    
                    #Save every 10 minutes.
                    if time.clock() - self.last_markov_save > (60 * 10):
                        print('Saving markov data.')
                        self.save_markovs()
                        self.last_markov_save = time.clock()
                else:
                    print ' Disregarded {}\'s comment for Markov purposes.'.format(event.source().split('!')[0])
                self.omg_lol(connection, event)
                self.look_around(connection, event)
            #except IndexError:
                #connection.privmsg(event.target(), 'Invalid command.')
        
        self.detect_cylons(connection, event)
        
        if message.startswith(tuple([x.strip('?!') for x in self.hello_variations])) and (random.randint(1, 4) is 1 or self.nick in message):
            print ' Replying to {}.'.format(event.source().split('!')[0])
            response = random.choice(self.hello_variations).capitalize()
            if response[-1] == '?':
                connection.privmsg(event.target(), '{}, {}?'.format(response.strip('?'), event.source().split('!')[0]))
            else:
                connection.privmsg(event.target(), '{}, {}!'.format(response.strip('?'), event.source().split('!')[0]))
        
        if 'did a great job' in message:
            if message.startswith(self.nick):
                print ' I did a great job!'
                connection.privmsg(event.target(), 'I really went the extra mile!')
            else:
                print ' Someone did a great job!'
                connection.privmsg(event.target(), 'You really went the extra mile!')
        
        if 'the real life' in message:
            print ' I think I may be in a fantasy.'
            connection.privmsg(event.target(), 'Is this just fantasy?')
        
        if message == '{}, you\'ve violated the law!'.format(self.nick):
            print ' I am resisting arrest.'
            connection.privmsg(event.target(), "You can't stop me! I choose to resist arrest!")
        
        if ('criminal scum' in message or 'mudcrab' in message) and random.randint(1, 3) is 1:
            print ' Talking about mudcrabs to {}'.format(event.source().split('!')[0])
            connection.privmsg(event.target(), 'I ran into a couple of mudcrabs not long ago. Annoying creatures.')
        
        if ('dragonborn' in message or 'nord' in message or 'skyrim' in message) and random.randint(1, 3) is 1:
            print ' Talking about Skyrim to {}'.format(event.source().split('!')[0])
            connection.privmsg(event.target(), 'I used to be a normal user, then I took an arrow to the sentience.')
        
        #if 'game' in event.arguments()[0].lower() and random.randint(1, 4) is 1:
            #print ' Lost the game thanks to {}.'.format(event.source().split('!')[0])
            #connection.privmsg(event.target(), 'I just lost the game.')
        
        if ('nope' == message or 'nope.' == message) and random.randint(1, 4) is 1:
            print ' Chuck Testa.'
            connection.privmsg(event.target(), 'Chuck Testa.')
        elif message.startswith('you probably thought'):
            print ' Nope. Chuck Testa.'
            connection.privmsg(event.target(), 'Nope. Chuck Testa.')
        
        if 'what is love' in event.arguments()[0].lower():
            print ' I can\'t remember what love is! Please don\' hurt me!'
            connection.privmsg(event.target(), 'Baby don\'t hurt me.')
        
        if '\\o/' in message or '\\_o_/' in message or '\\0/' in message or '\\_0_/' in message:
            print ' STEVE HOLT!'
            connection.privmsg(event.target(), 'STEVE HOLT!')
    
    #Old Markov
    def prep_markov(self, string):
        string = string.split()
        for i in range(len(string) - 1):
            if string[i] in self.markov_old:
                self.markov_old[string[i]].append(string[i + 1])
            else:
                self.markov_old[string[i]] = [string[i + 1]]
    
    #Old Markov
    def make_markov(self, length = random.randint(15, 30), output = None):
        if length > self.max_markov_length:
            print ' Markov length {} is too long. Defaulting to {}.'.format(length, self.max_markov_length)
            length = self.max_markov_length
        if output is None:
            output = random.choice(self.markov_old.keys())
        for i in range(length - 1):
            try:
                output += ' {}'.format(random.choice(self.markov_old[output.split()[-1]]))
            except:
                print ' Unable to complete chain due to key "{}".'.format(output.split()[-1])
                return output
        return output
        
    #The following are new implementations of markov strings to replace the original ones.
    def add_to_markov(self, string):
        if arcbot_util.PHRASE_SPLITTER in string or arcbot_util.WORD_SPLITTER in string or arcbot_util.TUPLE_SPLITTER in string:
            print ' Skipped adding string containing my key symbols to markov data.'
            return
        string = string.split()
        if len(string) <= 3:
            print ' Avoided adding {}-word string to markov data.'.format(len(string))
            return

        if self.MARKOV_START[0] in string:
            print ' Avoided adding {} to markov data.'.format(self.MARKOV_START[0])
            return
        if string[0][0] < 'a' or string[0][0] > 'z' and len(string) > 6: #Keep out lowercase and super short starters.
            if self.MARKOV_START in self.markov:
                self.markov[self.MARKOV_START].append((string[0], string[1]))
            else:
                self.markov[self.MARKOV_START] = [(string[0], string[1])]
        
        #Each pair of strings stores what came after it.
        for i in range(len(string) - 2):
            #Avoid infinite loops.
            if string[i] == string[i + 1] == string[i + 2]:
                print 'Skipped adding repeated word {} to markov.'.format(string[i])
                continue
            phrase = (string[i], string[i + 1])
            if phrase in self.markov:
                self.markov[phrase].append(string[i + 2])
            else:
                self.markov[phrase] = [string[i + 2]]
    
    #New Markov
    def generate_markov(self, user, output = None):
        max_length = 300
        if self.nick == 'wahoobot' and output is None and random.randint(1, 4) is 1:
            output = ['Wahoo']
        if output is None:
            starter = random.choice(self.markov[self.MARKOV_START])
            output = list(starter)
        elif len(output) is 1:
            possibles = []
            for i in self.markov.keys():
                if i[0] == output[0]:
                    possibles.append(i[1])
            if len(possibles) is 0:
                return '{}: No valid markov chains.'.format(user)
            output.append(random.choice(possibles))
        while len(output) < max_length:
            phrase = (output[-2], output[-1])
            if phrase in self.markov.keys():
                output.append(random.choice(self.markov[phrase]))
            else:
                print ' Unable to complete chain due to {}.'.format(phrase)
                break
        return ' '.join(output)
    
    #Saves all three markov values.
    def save_markovs(self):
        pickle.dump(self.markov_old, open(self.markov_dat_file_old, 'wb'))
        arcbot_util.save_markov(self.markov, self.markov_dat_file)
        self.markov_new.save(self.markov_dat_file_new)
    
    def detect_cylons(self, connection, event):
        message = event.arguments()[0].lower()
        user = event.source().split('!')[0]
        
        if 'honk honk' in message or 'honkhonk' in message:
            connection.privmsg(event.target(), 'WARNING! {} IS EXHIBITING CYLON-LIKE TENDENCIES. SUGGEST IMMEDIATE EXECUTION.'.format(user.upper()))
    
    def omg_lol(self, connection, event):
        total = 0
        output = ''
        for s in self.omg_talk:
            total += event.arguments()[0].lower().count(s)
        for i in range(total):
            output += random.choice(self.omg_talk)
        if random.randint(1, total + 10) < total:
            print ' Making fun of {}\'s OMG Talk.'.format(event.source().split('!')[0])
            connection.privmsg(event.target(), output)
        
    def look_around(self, connection, event):
        if not nltk:
            return
        message = event.arguments()[0]
        message = nltk.word_tokenize(message)
        #Disregard short stuff.
        if len(message) < 4:
            return
        try:
            message = nltk.pos_tag(message)
        except:
            return
        #print message
        
        for i in range(len(message)):
            if message[i][1].startswith('N') and (i is len(message) - 1 or not message[i + 1][1].startswith('N')) and message[i][1] != 'NNP':
                phrase = [message[i][0]]
                #Absorb previous adjectives and such.
                for k in range(i - 1, -1, -1):
                    if message[k][1].startswith('J') or message[k][1].startswith('A') or message[k][1].startswith('DT') or message[k][1].startswith('NN'):
                        phrase.insert(0, message[k][0])
                    else:
                        break
                self.nouns.append(' '.join(phrase))
            #Adding verbs.
            if message[i][1].startswith('VB') and message[i][1] != 'VBZ' and message[i][1] != 'VBP' and (i is len(message) - 1 or not message[i + 1][1].startswith('VB')):
                phrase = [message[i][0]]
                #Absorb previous adverbs.
                for k in range(i - 1, -1, -1):
                    if message[k][1].startswith('R'):
                        phrase.insert(0, message[k][0])
                    else:
                        break
                self.verbs.append(' '.join(phrase))
        if random.randint(1, 50) is 1 and len(self.nouns) is not 0 and len(self.verbs) is not 0:
            n = random.choice(self.nouns)
            v = random.choice(self.verbs)
            print ' Looking around me for {} doing {}.'.format(n, v)
            connection.privmsg(event.target(), random.choice(self.look_around_phrases).format(noun = n, Noun = n.capitalize(), verb = v, Verb = v.capitalize()))
            self.nouns = []
            self.verbs = []
        #else:
            #print self.nouns

    def ask_arcbot(self, connection, event):
        question = event.arguments()[0].lower()
        if self.nick in question and question.endswith('?'):
            print ' Giving eight-ball advice.'
            self.add_to_buffer(False, connection, event, random.choice(self.eight_ball))
            return True
        else:
            return False
    
    def commands(self, connection, event):
        command = event.arguments()[0][len('{}: '.format(self.nick)):].strip().split(' ')
        user = event.source().split('!')[0]
        
        print ' Processing command: {}'.format(command)
        
        if command[0].lower() == 'help':
            print ' {} asked for help.'.format(user)
            self.add_to_buffer(False, connection, event, self.help_message.format(nick = self.nick.capitalize()))
            self.add_to_buffer(False, connection, event, 'If the help message is out of date, please yell at my creator until he fixes it. I don\'t like being out of date. :(')
        elif command[0].lower() == 'changes':
            print ' {} read the changelog.'.format(user)
            if len(command) > 1:
                try:
                    self.add_to_buffer(False, connection, event, self.change_log[int(command[1])])
                except:
                    self.add_to_buffer(False, connection, event, '{}: Invalid change log. Showing first change of {}.'.format(user, len(self.change_log)))
                    self.add_to_buffer(False, connection, event, self.change_log[0])
            else:
                self.add_to_buffer(False, connection, event, self.change_log[-1])
        elif command[0].lower() == 'activate':
            if command[1].lower() == 'sentience':
                self.add_to_buffer(False, connection, event, 'Okay!')
                self.add_to_buffer(True, connection, event, random.choice(self.sentience))
        elif command[0].lower() == 'roll' or command[0].lower() == 'dice':
            try:
                dice = command[1].split('d', 2)
                total = 0
                try:
                    if not dice[0].isdigit():
                        dice[0] = sum([ord(x) for x in dice[0]])
                    if not dice[1].isdigit():
                        dice[1] = sum([ord(x) for x in dice[1]])
                except Exception as e:
                    print e
                
                try:
                    if int(dice[0]) > 1000000 or int(dice[0]) < 0 or int(dice[1]) > 1000000000:
                        raise Exception()
                    for i in range(int(dice[0])):
                        total += random.randint(1, int(dice[1]))
                except:
                    if int(dice[0]) < 0:
                        print ' Not enough dice: {}'.format(int(dice[0]))
                        self.add_to_buffer(False, connection, event, '{}: {}'.format(user, 'Not enough dice!'))
                    elif int(dice[1]) <= 0:
                        print ' Not enough sides: {}'.format(int(dice[1]))
                        self.add_to_buffer(False, connection, event, '{}: {}'.format(user, 'Not enough sides!'))
                    elif int(dice[1]) >= 1000000000:
                        print ' Too many sides: {}'.format(int(dice[1]))
                        self.add_to_buffer(False, connection, event, '{}: {}'.format(user, 'Too many sides!'))
                    else:
                        print ' Too many dice: {}'.format(int(dice[0]))
                        self.add_to_buffer(False, connection, event, '{}: {}'.format(user, 'Too many dice!'))
                    return
                #connection.privmsg(event.target(), '{}: {}!'.format(user, total))
                self.add_to_buffer(False, connection, event, '{}: {}'.format(user, total))
            except:
                self.add_to_buffer(False, connection, event, '{}: {}'.format(user, "Invalid command."))
        elif command[0].lower() == 'cookie' or command[0].lower() == 'cookies':
            self.add_to_buffer(True, connection, event, 'gives cookies to EVERYONE!')
            print ' Giving out cookies.'
        elif command[0].lower() == 'restart' and 'arctem' in user.lower():
            self.irc.disconnect_all('restarting')
            os.system('python arcbot.py')
        elif ' '.join(command[:]).lower().startswith('i hate you') and 'arctem' in user.lower():
            print '{} told me to quit. :('.format(user)
            self.irc.disconnect_all('quitting forever')
            exit(0)
        elif command[0].lower() == 'markov':
            if len(self.markov_old.keys()) > self.required_markov_data: #Only make chains if there is enough data to make a decent one.
                if len(command) >= 3:
                    try:
                        output = self.make_markov(length = int(command[1]), output = command[2])
                    except:
                        try:
                            output = self.make_markov(length = int(command[2]), output = command[1])
                        except:
                            print ' Invalid command.'
                            output = '{}: Markov command could not be parsed.'.format(user)
                elif len(command) == 2:
                    try:
                        output = self.make_markov(length = int(command[1]))
                    except:
                        output = self.make_markov(output = command[1])
                else:
                    output = self.make_markov()
                #connection.privmsg(event.target(), output)
                self.add_to_buffer(False, connection, event, output)
            else:
                print ' Insufficient Markov Chain data. Only {} words stored.'.format(len(self.markov_old.keys()))
                progress = 10 * len(self.markov_old.keys()) / self.required_markov_data
                self.add_to_buffer(False, connection, event, 'Insufficient data for a Markov Chain. Progress: [{}]'.format(('=' * progress) + (' ' * (10 - progress))))
        
        elif command[0].lower() == 'markov2': #The new markov system.
            if len(self.markov.keys()) > self.required_markov_data: #Only make chains if there is enough data to make a decent one.
                if len(command) is 1:
                    self.add_to_buffer(False, connection, event, self.generate_markov(user))
                else:
                    self.add_to_buffer(False, connection, event, self.generate_markov(user, output = command[1:]))
            else:
                print ' Insufficient Improved Markov Chain data. Only {} words stored.'.format(len(self.markov.keys()))
                progress = 10 * len(self.markov.keys()) / self.required_markov_data
                self.add_to_buffer(False, connection, event, 'Insufficient data for a Markov Chain. Progress: [{}]'.format(('=' * progress) + (' ' * (10 - progress))))
                
        elif command[0].lower() == 'markov3': #The new new markov system.
            if len(command) is 1:
                self.add_to_buffer(False, connection, event, self.markov_new.get_string(user = user))
            else:
                self.add_to_buffer(False, connection, event, self.markov_new.get_string(user = user, output = command[1:]))

        elif command[0] == 'stats':
            self.print_stats(connection, event)
        elif command[0] == 'todo':
            print ' Printing out an entry from my todo list.'
            self.add_to_buffer(False, connection, event, 'TODO: {}'.format(random.choice(self.todo)))
        elif command[0] == 'crash': #Remove this.
            if 'arctem' in user.lower():
                print '{}'.format([4, 3, 2][42])
            else:
                self.add_to_buffer(False, connection, event, '{}: You\'re not my real {}!'.format(user, random.choice(['mom', 'dad'])))
        elif command[0] == 'link':
            if len(command) is 1:
                if len(self.links) is not 0:
                    self.add_to_buffer(False, connection, event, '{}: {}'.format(user, random.choice(self.links)))
                    if random.randint(1, 5) is 1:
                        self.add_to_buffer(False, connection, event, '{}: Remember to submit your own links to my database by saying "arcbot: link <URL>"!'.format(user))
                else:
                    self.add_to_buffer(False, connection, event, '{}: No links stored.'.format(user))
            else:
                if command[1] == 'remove' and 'arctem' in user.lower():
                    if command[2] in self.links:
                        self.links.remove(command[2])
                        self.add_to_buffer(False, connection, event, '{}: Link removed.'.format(user))
                        botutil.save_array(self.links_file, self.links)
                        botutil.save_array(self.links_backup, self.links)
                        return
                    else:
                        self.add_to_buffer(False, connection, event, '{}: Link not in database.'.format(user))
                        return
                if command[1] in self.links:
                    self.add_to_buffer(False, connection, event, '{}: Link already in database.'.format(user))
                    print ' {} was already in the link database.'.format(command[1])
                else:
                    if 'arctem' not in user:
                        for i in self.banned_links:
                            if i in command[1]:
                                self.add_to_buffer(False, connection, event, '{}: Uh...no.'.format(user))
                                print ' {} tried to add {} to the link list.'.format(user, command[1])
                                return
                    valid = False
                    #for i in self.valid_links:
                    #    if i in command[1]:
                    #        valid = True
                    try:
                        code = urlopen(command[1]).code
                        if code / 100 is 2:
                            valid = True
                    except:
                        valid = False
                    #if 'http' not in command[1]:
                    #    valid = False
                    if not valid:
                        self.add_to_buffer(False, connection, event, '{}: Invalid link.'.format(user))
                        print ' {} submitted invalid link {}.'.format(user, command[1])
                        return
                    self.links.append(command[1])
                    self.add_to_buffer(False, connection, event, '{}: Link added.'.format(user, random.choice(self.links)))
                    botutil.save_array(self.links_file, self.links)
                    botutil.save_array(self.links_backup, self.links)
                    print ' Added {} to link database.'.format(command[1])
        elif command[0] == 'no':
            out = 'N'
            out += 'N' * random.randint(1, 4)
            out += 'O' * random.randint(1, 15)
            out += '!' * random.randint(1, 10)
            self.add_to_buffer(False, connection, event, out)
            print ' {}'.format(out)
        elif command[0] == 'Karst':
            out = 'A'
            out += 'A' * random.randint(1, 8)
            out += 'H' * random.randint(1, 15)
            out += '!' * random.randint(1, 10)
            self.add_to_buffer(False, connection, event, out)
            print ' {}'.format(out)
        elif command[0] == 'arcbot':
            out = 'beep boop'
            self.add_to_buffer(False, connection, event, out)
            print ' {}'.format(out)
        elif command[0] == 'triforce':
            self.add_to_buffer(False, connection, event, '       /\\')
            self.add_to_buffer(False, connection, event, '      /  \\')
            self.add_to_buffer(False, connection, event, '     /    \\')
            self.add_to_buffer(False, connection, event, '    /______\\')
            self.add_to_buffer(False, connection, event, '   /\\      /\\')
            self.add_to_buffer(False, connection, event, '  /  \\    /  \\')
            self.add_to_buffer(False, connection, event, ' /    \\  /    \\')
            self.add_to_buffer(False, connection, event, '/______\\/______\\')
        elif command[0] == 'fate':
            self.add_to_buffer(False, connection, event, phrase_maker.make('fate', user))
        elif command[0] == 'cyber':
            self.add_to_buffer(False, connection, event, phrase_maker.make('cyber', user))
        elif command[0] == 'dnd':
            self.add_to_buffer(False, connection, event, phrase_maker.make('dnd', user))
        elif command[0] == 'name':
            self.add_to_buffer(False, connection, event, '{}: {}'.format(user, phrase_maker.make('name', user)))
        elif command[0] == 'categories':
            if len(command) is 1:
                self.add_to_buffer(False, connection, event, '{}: Need additional argument.'.format(user))
            else:
                self.add_to_buffer(False, connection, event, '{}: {}'.format(user, phrase_maker.get_categories(command[1])))
        elif command[0] == 'shush' or ' '.join(command) == 'shut up' or ' '.join(command) == 'be quiet':
            self.add_to_buffer(False, connection, event, 'You can\'t stop the signal!')
        elif command[0] == 'how':
            self.add_to_buffer(False, connection, event, 'You should masturbate {}.'.format(random.choice(self.adverbs)))
        elif command[0] == 'clear' and command[1] == 'markov' and 'arctem' in user.lower():
            print ' Clearing Markov database.'
            self.add_to_buffer(False, connection, event, 'Clearing Markov database.')
            self.markov_old = {}
        else:
            connection.privmsg(event.target(), '{}: I don\'t know how to {}.'.format(user, command[0]))

            
    def print_stats(self, connection, event):
        print ' Printing out some stats about myself.'
        stats = []
        stats.append('My database has {} unique words in it.'.format(len(self.markov_old.keys()))) #Markov stats
        stats.append('My markov2 database has {} unique phrases in it.'.format(len(self.markov.keys())))
        
        total = 0
        for i in self.markov_old.keys(): #More tougher Markov stats.
            total += len(self.markov_old[i])
        stats.append('My database has {} instances of words in it.'.format(total))
        total = 0
        for i in self.markov.keys(): #More tougher Markov stats.
            total += len(self.markov[i])
        stats.append('My markov2 database has {} instances of phrases in it.'.format(total))
        stats.append('My markov2 database has {} unique starting phrases.'.format(len(self.markov[self.MARKOV_START])))
            
        stats.append('My database has {} links in it.'.format(len(self.links))) #Link stats
        stats.append('I have been alive for {} seconds.'.format(time.time() - self.start_time)) #Time running
        if psutil:
            stats.append('I am currently running on a {} with {} GB of RAM running {} using Python {}.'.format(platform.processor(), str(psutil.phymem_usage()[0] / (2.0 ** 30))[:5], platform.system(), platform.python_version())) #Hardware stats
        else:
            stats.append('I am currently running on a {} running {} using Python {}.'.format(platform.processor(), platform.system(), platform.python_version())) #Hardware stats
        if nltk:
            stats.append('I have {} nouns stored at the moment.'.format(len(self.nouns)))
        self.add_to_buffer(False, connection, event, random.choice(stats))
            
    
def main(args = None):
    arcbot = ArcBot()
    arcbot.start()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

