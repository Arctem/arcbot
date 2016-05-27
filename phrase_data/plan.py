data = {
    'plan' : {
        'template' : ['{premise} {execution}'],

        'premise' : ['If we want to {goal} then', "When we reach the {event}, we won't have much time to {goal}:"],
        'goal' : ['{generic_verb,person_verb} {target_person,target_people}', '{generic_verb,object_verb} {target_object}', 'prove that {target_person} is {secret_identity}', '{enter_verb,generic_verb} {place}'],

        'generic_verb' : ['pee on', 'defenestrate', 'photograph', 'draw {drawings} on'],
        'person_verb' : ['kidnap', 'kill', 'mug', 'mildly annoy'],
        'object_verb' : ['destroy', 'steal', 'deface'],
        'enter_verb' : ['sneak into', 'get to', 'invade'],

        #TODO: custom things like 'kidnap {target} from the {event}

        'drawings' : ['dicks', 'boobs', 'a complex mathematical proof'],

        'amount' : ['dozens of', 'thousands of dollars worth of', 'some'],

        'target_person' : ['the {important_title}', '{famous_person}', '{irc_member}'],
        'target_people' : ['{amount} {kidnap_targets}'],
        'important_title' : ['President', 'Queen', 'King', 'Pope', 'ambassador', 'Harbinger of Destruction', 'senator'],
        'famous_person' : ['Obama', 'Trump', 'John Cena', 'Steve Buscemi', 'Jan-Michael Vincent', 'Frodo', 'Gandalf', 'Godzilla', 'Hitler', 'your mom', 'Guy Fieri'],
        'irc_member' : ['arcbot', 'Andrew', 'Baer', 'Chris', 'Duncan', 'Elliot', 'Flan', 'Ian', 'Jesse', 'Jett', 'Quartermaster', 'Rob', 'Russell', 'Spencer'],
        'kidnap_targets' : ['Jan-Michael Vincents', 'children', 'strippers'],

        'secret_identity' : ['the {the_secret_id}', 'a {a_secret_id}', '{famous_person}'],
        'the_secret_id' : ['Zodiac Killer', 'Batman'],
        'a_secret_id' : ['robot', 'lizard', '{cult} member'],
        'cult' : ['KKK', 'Illuminati'],

        'target_object' : ['{dnd/relic}', '{loot/item}', 'the {famous_item}', 'a {item}', '{amount} {items}'],
        'famous_item' : ['unit circle', "Pope's hat", 'Millenium Falcon', 'Holy Grail', 'Ring', 'Horcrux', 'MacGuffin'],
        'item' : ['Bagger 288', 'dildo', 'AOL Free Trial CD', 'mint-condition Beanie Baby', 'quadcopter',  'boat', "{famous_person,irc_member}'s {body_part}"],
        'items' : ['Bagger 288s', 'dildos', 'AOL Free Trial CDs', 'quadcopters', 'bratwurst', 'MacBooks', 'boats'],
        'body_part' : ['face', 'chest', 'forehead', 'arms'],

        'execution' : ["we'll need to {instructions}.", "you'd better hope {condition}."],
        'instructions' : ['get some help from {target_person,target_people}', "make sure {target_person} doesn't find out", 'get {target_object} first', 'find out when the {event} starts', 'get a map of {place}'],
        'condition' : ['{premade_condition}', '{famous_person,irc_member} remembers to bring {target_object}', '{famous_person,irc_member} comes through for us', 'our {item} lasts through the {event}', "we don't run out of {items}", "{target_person} is {secret_identity}", "{target_person} {actions} in time"],
        'premade_condition' : ['the stars are right', "you're adopted", 'our Kickstarter gets funded', 'the terrorists win', 'jet fuel can melt steel beams', 'the proof is both necessary and sufficient', 'grandma accepts your apology', 'the phasers are set to stun'],
        'actions' : ['fixes the bugs', 'hides the evidence', 'sends the nudes', "can believe it's not butter"],

        'event' : ['orgy', 'parade', 'sacrifice', 'birthday party', 'ceremony', 'wrestling match'],

        'place' : ['Poland', 'Austria', 'Germany', 'Kansas', 'Burrito Time', 'Vatican City', 'The Anti-Vatican', 'Russia', 'Australia', 'Europe', 'Mars', "R'lyeh"],
    }
}
