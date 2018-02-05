data = {
    'insult': {
        'template': ['{introduction}, {insult}.', '{insult}.', '{dismissal}, for {direct}.', '{special}'],

        'introduction': ['Oh {title} of {holding}'],
        'special': ['{curse} and {curse}.', 'Not even a {bad_profession} could miss that {direct}.'],

        'title': ['{Title_qualifier} {rank}', '{Bad_adjective} {rank}', '{rank}'],
        'title_qualifier': ['grand', 'misled', 'deranged', 'mad', 'fell'],
        'rank': ['Duke', 'King', 'Lord'],

        'dismissal': ['You are barely worth my notice', 'How dare you enter my presence'],

        'holding': ['{bad_place}', '{Bad_objects}', "{Bad_person}'s {bad_object,bad_objects}"],
        'bad_place': ['the {Bad_adjective} {Terrain}', ],

        'insult': ['{direct}', '{curse}'],

        'direct': ['your {good_object} is naught but a {bad_object}!',
                   'you are nothing but a {bad_object,bad_profession}!', 'you are no better than {bad_person}'],

        'curse': ['{emploration} your {good_object} {become} a {bad_object}',
                  '{emploration} your {good_objects} {become} {bad_objects}',
                  '{emploration} your {good_object} {bad_transformation}'],

        'emploration': ['may'],

        'object': ['{good_object}', '{bad_object}'],
        'good_object': ['firstborn {child}', '{relative}', 'castle', 'horse'],
        'good_objects': ['children', 'accomplishments', 'pants', 'lands'],
        'bad_object': ['dung beetle', 'dick', '{bad_object}-face', 'butt', 'degenerate', 'toad', 'coward', 'rapscallion', 'ruffian', 'taint'],
        'bad_objects': ['locusts', 'dust', 'dicks', 'refuse', 'gonads', 'mud'],

        'bad_person': ['Satan', 'Lucifer', 'Hitler', '{Gen/username}'],
        'bad_profession': ['hobo', 'leper', 'heathen', 'vagabond', '{bad_adjective} {person}', 'sycophant', 'beast'],

        'person': ['man', 'woman', 'child', 'boy', 'girl'],

        'adjective': ['{good_adjective}', '{bad_adjective}', '{neutral_adjective}'],
        'bad_adjective': ['slimey', 'rotten', 'barren', 'defiled', 'blind'],
        'good_adjective': [],
        'neutral_adjective': [],

        'terrain': ['Mountain', 'Highlands', 'Peak', 'Pass', 'Plains', 'Valley'],

        'delicacy': ['porn', 'wine', 'cheese'],

        'become': ['be', 'turn into', 'become naught but', 'be revealed to be'],

        'bad_transformation': ['crumble to dust {condition}'],

        'condition': ['as you watch', 'all around you', 'while you {preoccupation}'],
        'preoccupation': ['can do nothing to stop it'],

        'child': ['child', 'son', 'daughter'],
        'relative': ['mother', 'father', 'grandfather', 'grandmother'],
    }
}
