data = {
    'plan': {
        'template': ['{premise} {execution}'],

        'premise': ['If we want to {goal} then', "When we reach {location}, we won't have much time to {goal}:"],
        'goal': ['{generic_verb,person_verb} {target_person,target_people}', '{generic_verb,object_verb} {target_object}', 'prove that {target_person} is {secret_identity}', '{enter_verb,generic_verb} {place}', 'get {target_person} a job as a {profession}', '{defeat} {target_person} at {competition}', '{generic_verb,poke_verb} that {pokemon}', '{generic_verb,evil_verb} {evil_being}', '{get} {target_person} {person_action}'],

        'generic_verb': ['pee on', 'defenestrate', 'photograph', 'draw {drawings} on'],
        'person_verb': ['kidnap', 'kill', 'mug', 'mildly annoy', 'seduce'],
        'object_verb': ['destroy', 'steal', 'deface'],
        'enter_verb': ['sneak into', 'get to', 'invade'],
        'poke_verb': ['catch', 'evolve', 'release', 'photograph'],
        'evil_verb': ['summon', 'imprison', 'become one with', 'save {place} from', 'banish'],
        'defeat': ['beat', 'defeat', 'best'],
        'get': ['get', 'convince'],
        'person_action': ['to {goal}'],

        'custom': ['kidnap {target_person} from {location}', 'get {irc_member} to be active in IRC again', 'catch them all', 'remember the Alamo', 'find Carmen Sandiego', 'hack the planet', 'self-defenestrate'],

        'drawings': ['dicks', 'boobs', 'a complex mathematical proof'],

        'amount': ['dozens of', 'thousands of dollars worth of', 'some', '{approximation} {number}'],
        'approximation': ['exactly', 'precisely', 'approximately', 'about', 'around', 'no more than', 'no less than', 'at least', 'anything but'],
        'number': ['three', 'two', 'four and a half', '9¾', 'nine million, nine hundred ninety-nine thousand, nine hundred and ninety-eight'],
        'volumes': ['gallons', 'quarts', 'barrels', 'cups', 'thimbles', 'teaspoons'],

        'target_person': ['the {important_title}', '{famous_person}', '{irc_member}', 'a {person_adjective} version of {famous_person,irc_member}'],
        'target_people': ['{amount} {kidnap_targets}'],
        'important_title': ['President', 'Queen', 'King', 'pope', 'ambassador', 'Harbinger of Destruction', 'senator'],
        'famous_person': ['Obama', 'Trump', 'John Cena', 'Steve Buscemi', 'Jan-Michael Vincent', 'Frodo', 'Gandalf', 'Godzilla', 'Hitler', 'your mom', 'Guy Fieri', 'Ash', 'Brock', 'Misty', 'Nurse Joy', 'Nixon', 'Jesus', 'Godzilla'],
        'irc_member': ['arcbot', 'Andrew', 'Baer', 'Chris', 'Duncan', 'Elliot', 'Flan', 'Ian', 'Jesse', 'Jett', 'Quartermaster', 'Rob', 'Russell', 'Spencer'],
        'kidnap_targets': ['Jan-Michael Vincents', 'children', 'strippers', 'seamen'],
        'person_adjective': ['naked', 'clothed', 'tall', 'short', 'overdressed', 'gay', 'straight', 'flamboyant', 'sexy', 'aroused', 'well-endowed', 'self-conscious'],
        'profession_adjective': ['{person_adjective}', 'professional', 'amateur', 'highly-paid', 'child', 'luxury', 'cut-rate', 'internationally-recognized', 'high-ranking', 'male', 'female'],
        'profession': ['{profession_adjective} {profession}'] * 5 + ['porn star', 'wrestler', 'astronaut', 'actor', 'model', 'spy', 'author', 'stripper', 'human cannonball', 'president', 'dictator', 'Pokémon trainer', 'sailor'],
        'pokemon': ['Pikachu', 'Onyx', 'Blastoise', 'Charizard', 'Clefairy', 'Venusaur', 'Bulbasaur', 'Charmander', 'Squirtle', 'Mew', 'Caterpie', 'Meowth', 'Snorlax', 'Rattata', 'Pidgey', 'Psyduck'],
        'evil_being': ['{famous_person}', 'the corrupted soul of {famous_person,irc_member}', 'The Prince of Darkness', 'Dagon', 'Satan', 'Santa', 'The Nameless One', 'He Who Watches', 'The Black Sea God', 'Saint Malevolent'],

        'secret_identity': ['the {the_secret_id}', 'a {a_secret_id}', '{famous_person}'],
        'the_secret_id': ['Zodiac Killer', 'Batman'],
        'a_secret_id': ['robot', 'lizard', '{cult} member'],
        'cult': ['KKK', 'Illuminati'],

        'target_object': ['{dnd/relic}', '{loot/item}', "{famous_person,irc_member}'s {body_part}", 'the {famous_item}', 'a {item}', '{amount} {items}'],
        'famous_item': ['unit circle', "Pope's hat", 'Millenium Falcon', 'Holy Grail', 'Ring', 'Horcrux', 'MacGuffin'],
        'item': ['{container} of {items}', '{body_part}', 'Bagger 288', 'dildo', 'AOL Free Trial CD', 'mint-condition Beanie Baby', 'quadcopter',  'boat', 'Poké Ball'],
        'items': ['{volumes} of {liquid}', 'Bagger 288s', 'dildos', 'AOL Free Trial CDs', 'quadcopters', 'bratwurst', 'MacBooks', 'boats', 'Poké Balls'],
        'liquid': ['milk', 'goo', 'slime', 'vodka', 'alcoholic beverages', 'Red Bull™'],
        'body_part': ['face', 'chest', 'forehead', 'arms'],
        'container': ['sack', 'bucket', 'bag', 'chest'],

        'attribute': ['strong', 'blue', 'explosive', 'potent', 'colorful'],

        'execution': ['{someone_will} need to {instructions}.', "you'd better hope {condition}."],
        'someone_will': ["we'll", '{irc_member} will'],
        'instructions': ['{premade_instruction}', 'get some help from {target_person,target_people}', "make sure {target_person} doesn't find out", 'get {target_object} first', 'find out when the {event} starts', 'get a map of {place}', 'sacrifice {target_person,target_people} to {evil_being}'],
        'premade_instruction': ['keep it secret, keep it safe', 'stop blinking', 'put on some pants', 'get naked'],
        'condition': ['{premade_condition}', '{famous_person,irc_member} remembers to bring {target_object}', '{famous_person,irc_member} comes through for us', 'our {item} lasts through the {event}', 'our {item} is {attribute} enough', "we don't run out of {items}", "{famous_person,irc_member} is {secret_identity,person_adjective,target_person}", "{target_person} {actions} in time"],
        'premade_condition': ['the stars are right', "you're adopted", 'our Kickstarter gets funded', 'the terrorists win', 'jet fuel can melt steel beams', 'the proof is both necessary and sufficient', 'grandma accepts your apology', 'the phasers are set to stun'],
        'actions': ['fixes the bugs', 'hides the evidence', 'sends the nudes', "can believe it's not butter"],

        'competition': ['the World Series of {Game}', '{game}'],
        'game': ['ping pong', 'cricket', 'crochet', 'chess', 'hop-scotch', 'tag'],

        'location': ['{place}', 'the {event}', "{target_person}'s {event}"],
        'event': ['orgy', 'parade', 'sacrifice', 'birthday party', 'ceremony', 'wrestling match'],
        'place': ['Poland', 'Austria', 'Germany', 'Kansas', 'Burrito Tyme', 'Vatican City', 'The Anti-Vatican', 'Russia', 'Australia', 'Europe', 'Mars', "R'lyeh", 'the International Space Station', 'Prague', 'the world', 'Earth', 'The Place Where We All Are'],
    }
}
