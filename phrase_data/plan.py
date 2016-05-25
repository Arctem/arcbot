data = {
    'plan' : {
        'template' : ['{premise} {execution}'],

        'premise' : ['If we want to {goal}'],
        'goal' : ['{generic_verb,person_verb} {target_person}', '{generic_verb,object_verb} {target_object}'],

        'generic_verb' : ['pee on', 'defenestrate', 'photograph', 'draw {drawings} on'],
        'person_verb' : ['kidnap', 'kill', 'mug', 'mildly annoy'],
        'object_verb' : ['destroy', 'steal', 'deface'],

        'drawings' : ['dicks', 'boobs', 'a complex mathematical proof'],

        'amount' : ['dozens of', 'thousands of dollars worth of', 'some'],

        'target_person' : ['the {important_title}', '{famous_person}', '{irc_member}', '{amount} {kidnap_targets}'],
        'important_title' : ['President', 'Queen', 'King', 'Pope', 'ambassador', 'Harbinger of Destruction', 'senator'],
        'famous_person' : ['Obama', 'Trump', 'John Cena', 'Steve Buscemi', 'Jan-Michael Vincent', 'Frodo', 'Gandalf', 'Godzilla', 'Hitler'],
        'irc_member' : ['arcbot', 'Andrew', 'Baer', 'Chris', 'Duncan', 'Elliot', 'Flan', 'Jesse', 'Jett', 'Quartermaster', 'Rob', 'Russell', 'Spencer'],
        'kidnap_targets' : ['Jan-Michael Vincents', 'children', 'strippers'],

        'target_object' : ['{dnd/relic}', '{loot/item}', 'the {famous_item}', 'a {item}', '{amount} {items}'],
        'famous_item' : ['unit circle', "Pope's hat", 'Millenium Falcon', 'Holy Grail', 'Ring', 'Horcrux', 'MacGuffin'],
        'item' : ['Bagger 288', 'dildo', 'AOL Free Trial CD', 'mint-condition Beanie Baby'],
        'items' : ['Bagger 288s', 'dildos', 'AOL Free Trial CDs'],

        'execution' : ["we'll need to {instructions}.", "you'd better hope {condition}."],
        'instructions' : ['get some help from {target_person}', "make sure {target_person} doesn't find out", 'get {target_object} first'],
        'condition' : ['the stars are right', '{famous_person,irc_member} remembers to bring {target_object}'],
    }
}
