import random
import re
import sys

data = {
    #Generic stuff phrases for everything.
    'gen' : {
        'template' : ['this is only so tests don\'t crash'],

        'vowel' : list('aeiouy'),
        'consonant' : list('bcdfghjklmnpqrstvwxyz'),
        'karst' : ['Karst', 'Flannery', 'Flanneroo'],

        'num_either' : ['{number}', '{roman_number}'],
        
        'number' : ['{digit}{number}', '{digit}'],
        'digit' : '1234567890',

        'roman_number' : ['{roman_ones}']*3 + ['{roman_tens}{roman_ones}'],
        'roman_tens' : ['X'],
        'roman_ones' : ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
    },

    'fate' : {
        'template' : ['{opening} {event} {battle}! {death}.'],
    
        'enemy_mod' : ['very {enemy_mod}', 'undead', 'giant', 'poison', 'green', 'gaping', 'iron', 'flying', 'fire-breathing', 'asylum', 'diseased', 'hollow', 'fearsome', 'scaly', 'rotten', 'armored', 'enemy', 'shadow', 'jade', 'glacial', 'savage', 'baleful', 'great', 'steel', 'tiny', 'raging', 'annoyed', 'purple', 'sexy', 'naked'],
        'creature' : ['{enemy_mod} {creature}']*5 + ['skeleton', 'wyvern', 'rat', 'assassin', 'bookshelf', 'drake', 'dragon', 'demon', 'butterfly', 'dog', 'wolf', 'zombie', 'man', 'woman', 'snake', 'lizard', 'giant', 'treant', 'crab', 'bullsquid', 'hunter', 'ant lion', 'donkey', 'monkey', 'USS Wahoo', 'Agnaktor', 'Barroth', 'Qurupeco', 'Arzuros', 'Jaggi', 'Barioth', 'Deviljho', 'Diablos', 'Duramboros', 'Gigginox', 'Gobul', 'Baggi', 'Wroggi', 'Lagombi', 'Ludroth', 'Rathian', 'Rathalos', 'Plesioth', 'Uragaan', 'Volvidon', 'Nibelsnarf', 'drug dealer', 'bear', 'rhino', 'minotaur'],
        'creatures' : ['skeletons', 'rats', 'dragons', 'demons', 'butterflies', 'wolves', 'zombies', 'men', 'women', 'snakes', 'crabs', 'ants', 'donkeys', 'submarines', 'cats', 'kittens', 'bears', 'rhino', 'bees', 'cheerleaders'],
        'user_body' : ['arm', 'leg', 'toe', 'chest', 'head', 'finger', 'hand', 'foot', 'eye', 'groin'],
        'enemy_body' : ['hide', 'shell', 'claws', 'horn', 'armor'],
        'location' : ['Undead Asylum', 'Firelink Shrine', 'Undead Burg', 'Undead Parish', 'Depths', 'Blighttown', 'Quelaag\'s Domain', 'The Great Hollow', 'Ash Lake', 'Sen\'s Fortress', 'Anor Londo', 'Painted World of Ariamis', 'Darkroot Garden', 'Darkroot Basin', 'New Londo Ruins', 'The Duke\'s Archives', 'Crystal Cave', 'Demon Ruins', 'Lost Izalith', 'The Catacombs', 'Tomb of Giants', 'Black Mesa', 'City 17', 'The Pacific Ocean', 'Castamere', 'The Wall', 'Westeros', 'Essos', 'Hammond Industries'],
        'hazard_any' : ['a {hazard}', '{hazards}'],
        'hazard' : ['spike', 'swinging axe', 'fire', 'acid pool', 'bottomless pit', 'chasm', 'banana peel', 'horde of {creatures}', '{container} of {creatures}'],
        'hazards' : ['spikes', 'flames', 'spikes', 'banana peels'],
        'container' : ['cage', 'pit', 'basket', 'chamber', 'nest'],
        'damaged' :  ['poisoned', 'exploded', 'killed', 'murderified', 'castrated', 'defenestrated', 'torpedoed', 'severely inconvenienced', 'pierced', 'severed'],
        'initiated' : ['charged', 'roared', 'threw its {weapon_enemy}[enemy_wep]'],
        'weapon_enemy' : ['{enemy_mod} {weapon_enemy}']*4 + ['claws', 'battle axe', 'spear', 'dart gun', 'teeth', 'bazooka', 'breath', 'katana', 'tentacles', 'club', 'torpedo', 'beak', 'tail', 'tongue'],
        'weapon_user' : ['battle axe', 'spear', 'shield', 'katana', 'club', 'fist', 'large rock', 'rubber chicken', 'greatsword', 'nunchucks', 'claymore', 'impressive genitalia'],

        #For battle
        'start' : ['that {initiated} at {Username}[name]'],
        'fight' : ['{Username}[name] {user_atk}, but the {creature}[enemy] {enemy_react}', 'the {creature}[enemy] {enemy_atk} and {user_react}', 'a nearby {creature} interfered, and {damaged} {Username}[name]\'s {user_body}'],
        'morefight' : [', then {fight}'],
        'user_atk' : ['swung their {weapon_user}[user_wep]', 'dove towards the {creature}[enemy] in a daring attack'],
        'enemy_atk' : ['pushed {Username}[name] towards {hazard_any}', 'attacked with its {weapon_enemy}[enemy_wep]'],
        'user_react' : ['{Username}[name] screamed in pain', '{Username}[name]\'s {user_body} was {damaged}', '{Username}[name] narrowly avoided being {damaged}{morefight}', '{Username}[name] blocked with their {weapon_user}[user_wep], which was damaged beyond repair{morefight}'],
        'enemy_react' : ['dodged the mighty blow{morefight}', 'blocked the strike with its {weapon_enemy}[enemy_wep]{morefight}', 'let {Username}\'s {weapon_user}[user_wep] glance harmlessly off its {enemy_body}{morefight}', 'turned the attack back on {Username}[name], and {user_react}'],

        #For death
        'life' : ['life-blood', 'will to live', 'soul', 'energy', 'grip on reality'],
        'fading' : ['fading', 'slipping away', 'flowing out of them', 'vanishing'],
        'celebrated' : ['laughed', 'looked on hungrily', 'prepared to feast', 'hunted for its next victim'],

        'opening' : ['Whilst wandering through {location}, {Username}[name]'],
        'event' : ['came across a {enemy_mod} {creature}[enemy]', 'was set upon by a {enemy_mod} {creature}[enemy]'],
        'battle' : ['{start}! {fight}'],
        'death' : ['{Username}[name] felt their {life} {fading} as the {creature}[enemy] {celebrated}', '{Username}[name]\'s broken corpse tumbled into {hazard_any}'],
        #'death' : ['that {damaged} him with its {weapon_enemy}[enemy_wep]!', 'and fled mindlessly into {hazard_any}, spelling his end.'],
    },
    
    'cyber' : {
        'template' : ['{opening} {middle} and {end}'],# + ["Hey baby, I'm gonna {karst} your {karst} all night and {karst} your {karst} in the morning."],
        
        'adverb' : ['wistfully', 'lustfully', 'fruitfully', 'nakedly', 'quickly', 'hungrily'],
        'adjective' : ['intelligent', 'incredible', 'strange', 'dragon', 'sexy', 'naked', 'pointy', 'sharp', 'moist', 'based', 'foxy', 'tight', 'wet', 'slick', 'flaccid', 'erect', 'smooth'],
        
        'nick' : ['{username}', '{adjective} {nick}', '{nick} von {nick}', 'Honey-{nick}', 'sugar-{nick}', 'dirty {nick}', 'sex-{nick}', '{Nick} Master',  '{nick}-face', 'sexy', 'smurf', 'Pokemon Master', 'baby', 'bunny', 'kitten', 'waifu', '{adjective} whore', 'slut'],
        'action' : ['{adverb} {action}']*8 + ['tickle', 'shove a potato in', 'shove a {thing} in', 'cook', 'eat', 'fondle', 'stare {adverb} at', 'strip', 'ravage', 'whip', 'flog', 'spank', 'bite', 'nip', 'yiff', 'have an {adjective} conversation with', 'suckle', 'nuzzle', 'Shrek', 'wreck', 'devour', 'tongue', 'diddle', 'twiddle', 'caress', 'flick', 'pinch', 'squeeze', 'dildo', 'sniff', 'headbutt', 'smurf', 'shock', 'penetrate', 'quiz', 'fuck', 'pope', 'dingle'],
        'thing' : ['{adjective} {thing}']*5 + ['{gen/karst}', 'penis', 'vagina', 'face', 'monkey', 'butt', 'tits', 'murrhole', 'potato', 'nipple', 'balls', 'pussy', 'dick', 'crotch area', 'nethers', 'no-no zone', 'special place', 'boobs', 'titties', 'love pillow', 'waifu', 'man-meat', 'yiffstick', 'cherry'],
        'time' : ['late {time}', 'morning', 'night', 'evening', 'dusk', 'afternoon', 'class'],
        'location' : ['West Hall', 'the {location} bathroom', 'a public {location}', 'space', 'White House', 'between dimensions', 'heaven', 'hell', 'Vatican', 'Atlantis', 'Anti-Atlantis'],
        'substance' : ['{thing}-juice', 'jello', 'cum', 'whipped cream', 'honey', 'gravy', 'mayo', 'chocolate', 'hot sauce'],
        
        'opening' : ['Hey {nick},', '{nick},'],
        'middle' : ["I'm gonna {action} your {thing} all {time}", "I'm gonna cover your {thing} in {substance}"],
        'end' : ['{action} your {thing} in the {time}.', 'go to {location} to {action} your {thing} until {time}.'],
    },

    'dnd': {
        'template' : ['{opening} {middle} {end}'],

        'char' : ['{Name/template}', '{Title} {Name}', '{Name}{name}', '{Name} {Name}', '{Name}{epithet}'],
        'name' : ['{gen/vowel}{name}', '{gen/consonant}{name}', '{name}{gen/vowel}', '{name}{gen/consonant}']*6 + ['{username}', '{gen/karst}', 'fish', 'thor', 'aztec', 'boros', 'beau', 'nyx', 'cyka', 'dagon'],
        'title' : ['Lieutenant', 'Lord', 'Sergeant', 'Colonel', 'Overlord', 'Professor', 'Doctor', 'Janitor', "{God}'s Favored", 'Admiral', 'Prince', 'Princess'],
        'race' : ['half-{monster}', 'half-{race}', 'were{race}', 'were{monster}', 'hobbit', 'halfling', 'human', 'elf', 'monkey', 'jewish', 'canadian', 'drow', 'dwarf', 'gnome', 'dorf', 'tauren'],
        'class' : ['paladin', 'monk', 'rogue', 'warrior', 'fighter', 'knight', 'wizard', 'sorceror', 'pirate', 'samurai', 'ranger', '{adjective} dancer', '{adjective} Magus', 'sandwich', 'lumberjack', 'ninja', 'programmer', '{thing}omancer', 'witcher', 'biologist', 'gentleman', 'lady', 'aristocrat', 'disciple of {God}', 'cowboy', 'companion', 'seductress', 'stripper', 'druid', 'bard', 'barbarian', 'cleric of {God}', 'alchemist', 'cavalier', 'oracle', 'summoner', 'witch', 'necromancer'],
        'adjective' : ['{adj_bad}', '{adj_good}', '{adj_neutral}']*4 + ['very {adjective}'],
        'adj_bad' : ['zombie', 'giant', 'fiery', 'tiny', 'demon', 'possessed', 'marauding', 'angry'],
        'adj_good' : ['eternal', 'all-knowing', 'immortal', 'magical', 'blessed', 'holy', 'mighty', 'heroic', 'charismatic', 'legendary'],
        'adj_neutral' : ['stone', 'enchanted', 'ancient', 'giant', 'elder', 'bumbling', 'inadequate', 'flabbergasted', 'horny', 'naked', 'nude', 'frozen', 'boiled'],
        'adj_land' : ['land', '{adj_good} realm'],
        'enemies' : ['a {group} of {monsters}', '{Title} {Monster} and {number} {monsters}'],
        'monster' : ['{adj_bad} {monster}', '{adj_neutral} {monster}', 'orc', 'dragon', 'demon', 'goblin', 'kobold', 'giant', 'yeti', 'kitten', 'succubus', 'incubus', 'rat', 'vampire', 'bee', '{thing} elemental', 'kraken'],
        'monsters' : ['{adj_bad} {monsters}', '{adj_neutral} {monsters}', 'orcs', 'dragons', 'demons', 'goblins', 'kobolds', 'giants', 'yetis', 'kittens', 'rats', 'vampires', 'bees', '{thing} elementals', 'krakens'],
        'animal' : ['elk', 'bear', 'alligator', 'tiger', 'vulture', 'lion', 'wolf', 'direwolf', 'duck', 'kitten'],
        'group' : ['swarm', 'clan', 'band', 'gang', 'horde', 'army', 'harem'],
        'thing' : ['{adjective} {thing}', '{animal}', 'potato', 'steak', 'burger', 'sword', 'anvil', 'flame', 'breakfast', 'bag of holding', 'staff', 'wand', 'dildo', 'gemstone', 'axe', 'shield', 'spear', 'bra', 'airship', '{monster} statue', 'painting', 'katana', 'breastplate', 'helmet', '{animal} sausage', '{animal} sandwich', '{body_part}plate'],
        'activity' : ['killing {monsters}', 'training {class} novices'],
        'achievement' : ['ate a {thing}', 'ate a {monster}', 'bested {Char} the {Title} {Monster} in battle', 'recovered the {Adjective} {Thing} from the {adj_land} of {location}', 'defeated {enemies}', 'tamed a {animal}'],
        'alignment' : ['{Order} {Morality}'],
        'order' : ['lawful', 'neutral', 'true', 'chaotic', 'green', 'badass', 'moderately', 'technically'],
        'morality' : ['good', 'neutral', 'evil', 'badass', 'canadian'],
        'story' : ['legends', 'stories', 'the {adjective} scrolls', 'tales'],
        'location' : ['{Adj_good} {Place}'],
        'place' : ['flooded {place}', 'woods', 'forest', 'hills', 'ruins', 'mountain', 'ridge', 'valley', 'cliffs', 'steppe', 'plains', 'sea', 'pillars', 'waterfalls', 'brothel', 'dimension'],
        'malady' : ['{thing} allergies', '{monster}-rot'],
        'god' : ['Pelor', 'Asmodeus', 'Dagon', 'Cthulhu', 'Nektor', 'Nyctasha', 'Atropos', 'Chadde', 'Voldemort', 'Your Mom', 'Azathoth', 'Shub-Niggurath', 'Yog-Sothoth', 'Nyarlathotep', 'Yig', 'Mordiggian', 'Eul', 'Hammond', '{Gen/karst}'],
        'relic' : ['the {Adjective} {Thing}', '{God}\'s {Thing}', 'the {Thing} of {Adjective} {Place}', '{God}\'s {Body_part}'],
        'number' : ['two', 'three', 'four', 'countless', 'many'],
        'body_part' : ['arm', 'leg', 'chest', 'breast', 'groin', 'head', 'nose', 'ear', 'finger', 'toe', 'torso', 'knee', 'elbow'],
        'epithet' : [' the {Adjective},', ', the {Title},', ' of the {Location}'],

        'opening' : ['{Char} is a {Race} {Class}', '{Story} tell of a {Class}'],
        'middle' : ['who specializes in {activity}', 'who is {alignment}', 'who hails from {location}', 'who suffers from {malady}', 'who worships {God}', 'who has a {Adjective} {Animal} companion', 'whose {body_part} is {adjective}'],
        'end' : ['and once {achievement}.', 'and quests for {Relic}.'],
    }, 

    'name' : {
        'template' : ['{cog}', '{boss}'], #'{native}', ],

        'cog' : ['{Brit_first} {Cog_last}'],
        'native' : ['{Native_first} {Native_last}', '{Native_verbs} With {Native_animals}'],
        'boss' : ['{Boss_first} {Boss_last}'],

        'brit_first' : ['{brit_first_male}', '{brit_first_fem}'],
        'brit_first_male' : ['Mr.', 'Sir', 'wilbert', 'mudd', 'rooster', 'ruddigore', 'brick', 'thaddeus', 'bollox', 'zebulon', 'egress', 'winston', 'manfred', 'edwind', 'hammond'],
        'brit_first_fem' : ['Miss', 'Lady', 'zylphia', 'bellis', 'ada', 'penny', 'kimberly', 'mimsy', 'hattie'],

        'brit_last_premade' : ['chuzzlewit', 'warddle', 'scadde', 'beamish', 'toves', 'chuddlewick', 'hammond'],
        'brit_last_ending' : ['son', 'bottom'],

        'cog_last' : ['{metal}{component}', '{component}{component}', '{metal}{brit_last_ending}', '{component}{brit_last_ending}', '{cog_last_premade}', '{brit_last_premade}'],
        'cog_last_premade' : ['bootstrappe', 'coalscofle', 'matchelocke'],

        'metal' : ['brass', 'coal', 'steel', 'bronze', 'iron', 'ash', 'salt', 'silver', 'copper'],
        'component' : ['cog', 'gimbal', 'gear', 'widget', 'locke', 'saw', 'pipe', 'mill', 'tack', 'whistle'],

        'native_first' : ['{native_verbing}'],
        'native_verbing' : ['flying', 'speeding', 'riding', 'hunting', 'dancing', 'laughing'],
        'native_verbs' : ['flies', 'runs', 'rides', 'hunts', 'dances', 'laughs'],

        'native_last' : ['{native_adj}{native_animal}', '{native_last_premade}'],
        'native_last_premade' : ['bullet'],
        'native_adj' : ['fast', 'quick', 'hungry', 'big', 'small'],
        'native_animal' : ['rabbit', 'buffalo', 'hawk', 'wolf', 'eagle', 'owl'],
        'native_animals' : ['rabbits', 'bison', 'hawks', 'wolves', 'eagles', 'owls'],
        
        'boss_first' : ['{boss_prefix}{boss_first}', '{boss_first}{boss_postfix}', '{boss_title}', '{boss_weather}', '{boss_animal}'],
        'boss_title' : ['commander', 'sergeant', 'dr.'],
        'boss_weather' : ['blizzard', 'thunder', 'blaze', 'burn', 'firestorm', 'glacier', 'gravity', 'volt'],
        'boss_animal' : ['rabbit', 'buffalo', 'hawk', 'wolf', 'snail', 'stingray', 'beetle', 'eagle', 'octopus', 'ostrich', 'gator', 'hammond'],
        'boss_prefix' : ['omni', 'mega', 'giga'],
        'boss_postfix' : ['oid', 'saurus'],
        
        'boss_last' : ['{boss_prefix}{boss_last}', '{boss_last}{boss_postfix}', '{boss_animal}', '{boss_word}', '{boss_weather}'],
        'boss_word' : ['doppler', 'psyche', 'hunter', 'slash', 'dynamo', 'hammond'],
    },

    'movie' : {
        'template' : ['{start}: {subtitle}'],

        'protaganist' : ['{Name}', '{Name} and {Name}', '{Formal_title} {Name}'],
        'protag_group_single' : ['The Gang'],
        'protag_group_plural' : ['The Guys', 'The Girls', 'We'],
        'name' : ['Alien', 'Andrew', 'arcbot', 'Ben', 'Benji', 'Celine', 'Chase', 'Chris', 'Elliot', 'Jett', 'Flannery', 'Ian', 'Jesse', 'Matt', 'Nico', 'Niko', 'Predator', 'Rob', 'Russell', 'Sarah', 'Jake', 'Stalin', 'Tyler Perry', '{Username}'],
        'famous_person' : ['Don Knotts', 'The Harlem Globetrotters', 'Carl Sagan', 'Tyler Perry', 'Darth Vader', 'Jar-Jar Binks', 'Jackie Chan', 'Dendi', 'Brock Samson', 'Hulk Hogan', 'Satan', 'Steve Buscemi', 'Sean Connery', 'Scott Chadde', 'Nicholas Cage', 'Dr. Hamdy Soliman', 'Batman', 'Spencer Brown', 'Gaben', 'The Dude'],

        'start' : ['{Start} Part {gen/num_either}', 'The Adventures of {protaganist}', '{protaganist}\'s {subtitle}'],

        'subtitle' : ['{sub_premade}', '{Name} vs. {Name}', '{Hype_noun}', 'The Search for {Item}', '{Title}, Where\'s My {Item}?', '{Name} Joins the {Organization}', '{Name} Visits {Place}', '{Name} and {Name} Go To {Place}', 'Escape From {Place}', '{Name}\'s Last Stand', 'The Return of {Name}', '{Protag_group_single} Meets {Famous_person}', '{Protag_group_plural} Meet {Famous_person}'],
        'sub_premade' : ['Destroy All Monsters', 'The Finale', 'There and Back Again', 'No Gay Shit'],

        'adjective' : ['more', 'extreme', 'awesome', 'sweet', 'sick'],
        'title' : ['{informal_title}', '{formal_title}'],
        'informal_title' : ['Dude', 'Doc', 'Bro', 'Broseph'],
        'formal_title' : ['Doctor', 'Rabbi'],
        'organization' : ['army', 'navy', 'government', 'Ku Klux Klan', 'Klan', 'bronies', 'Illuminati', 'Stone Masons', 'Na\'Vi'],
        'place' : ['Washington', 'the Congo', 'Space', 'Russia', 'Prison', 'Guantanamo Bay', 'West Hall', 'Alta 209', 'White Castle'],
        'item' : ['{adjective} {item}', 'money', 'dosh', 'pussy', 'dick', 'robot', 'pot', 'car', 'sex', 'porn', 'booze', 'dildo', 'fleshlight'],
        'hype_noun' : ['Excitement', 'Showdown', 'Arena', 'Reckoning', 'Electric Boogaloo', 'XXX', 'Triple X'],
    },

    'how' : {
        'template' : ['You should {verb} {adverb}.'],

        'verb' : ['masturbate', 'poop', 'fart'],
        'adverb' : open('adverbs.txt', 'r').read().split('\n')
    }
}


#Really stupid method to basically make a format that works better for what I'm doing.
def make(dict_name, name = 'Dudeface'):
    dict = data[dict_name]
    orig = random.choice(dict['template'])
    fixed_data = {}
    #regex = re.compile('{.+?}')
    regex = re.compile('''{.+?}(?:\[.+?\])?''')
    
    orig = replace_vars(dict, orig, regex, name, fixed_data)
    
    orig = fix_articles(orig)
    orig = fix_capitals(orig)
    orig = orig.split()
    orig[0] = orig[0].capitalize()
    return ' '.join(orig)

def replace_vars(dict, orig, regex, name, fixed_data):
    while len(regex.findall(orig)) > 0:
        to_replace = regex.findall(orig)[0]
        field = to_replace.strip('{}')
        field = field.split('}[') #Split if we have the optional arg
        cap = field[0] != field[0].lower()
        field[0] = field[0].lower()
        word = ''
        
        #Check for existing data.
        if len(field) > 1 and field[1] in fixed_data.keys():
            word = fixed_data[field[1]]
        elif '/' in field[0]:
            field[0] = field[0].split('/')
            word = random.choice(data[field[0][0]][field[0][1]])
            word = word.replace('{', '{' + field[0][0] + '/')
        elif field[0] not in dict.keys():
            if field[0] != 'username':
                print(field[0])
            #orig = orig.replace('{username}', name, 1)
            #orig = orig.replace('{Username}', name.capitalize(), 1)
            word = name
            #continue
        else:
            word = random.choice(dict[field[0]])
 
        #Handle all the extra vars inside the new word before we store it in fixed_data.
        word = replace_vars(dict, word, regex, name, fixed_data)

        if len(field) > 1 and field[1] not in fixed_data.keys():
            fixed_data[field[1]] = word

        if cap:
            word = make_capital(word)
        orig = orig.replace(to_replace, word, 1)
    return orig

def make_capital(orig):
    orig = orig.split()
    for i in range(len(orig)):
        if i is not 0 and orig[i] in ['of', 'the', 'a']:
            continue
        if orig[i][0] == '{':
            orig[i] = orig[i][0] + orig[i][1].capitalize() + orig[i][2:]
        else:
            orig[i] = orig[i][0].capitalize() + orig[i][1:]
    return ' '.join(orig)
    
#Makes sure sentences start with capitals.
def fix_capitals(orig):
    orig = orig.split()
    for i in range(len(orig) - 1):
        if i is 0 or orig[i - 1][-1] in '.?!':
            orig[i] = orig[i].capitalize()
    return ' '.join(orig)

def fix_articles(orig):
    orig = orig.split()
    for i in range(len(orig) - 1):
        if orig[i] == 'a' or orig[i] == 'an':
            if orig[i + 1][0].lower() in 'aeiou':
                orig[i] = 'an'
            else:
                orig[i] = 'a'
    return ' '.join(orig)

def get_categories(dict_name):
    if dict_name in data.keys():
        return '{}'.format(sorted(data[dict_name].keys()))
    else:
        return 'No database by that name.'

def main():
    if 'test' in sys.argv:
        test()
    elif 'demo' in sys.argv:
        demo()
    elif len(sys.argv) > 1:
        for i in range(5):
            print(make(sys.argv[1]))
    else:
        print(make('movie'))

def test():
    for key in sorted(data.keys()):
        print('Testing {}'.format(key))
        for i in range(10000):
            make(key)

def demo():
    for key in sorted(data.keys()):
        print('{}: {}'.format(key, make(key)))


if __name__ == '__main__':
    main()
