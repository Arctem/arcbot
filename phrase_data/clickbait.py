data = {
    'clickbait': {
        'template': ['{crazy_event} {emote_stinger}',
                     '{crazy_question} {evidence_stinger}', '{crazy_question}',
                     '{list_of_things}', '{amazing_find}'],

        'crazy_event': ['{Singular_person,Celebrity} {verb} ' +
                        '{normal_action,odd_action} {singular_object,singular_animal}!'],
        'crazy_question': ['Was {Old_celebrity} a {bad_thing,weird_thing}?',
                           'Is {Current_celebrity} a {bad_thing,weird_thing}?'],

        'list_of_things': ['{gen/number} {things} that look like {celebrity}.',
                           '{gen/number} {topic} tips that any {person} should know!'],

        'amazing_find': ['This {evidence} will show that you\'ve been ' +
                         '{actioning} wrong your entire life!'],

        #'stinger' : [],
        'evidence_stinger': ['this {evidence,person} {shows} {the_truth}.',
                             'this {evidence} will {change_state} you!',
                             'the answer will {change_state} you!'],
        'emote_stinger': ['first you\'ll {emote,be_state}, then you\'ll ' +
                          '{emote,be_state}!', 'You won\'t believe what happens next.'],

        'singular_person': ['this {person}'],
        'person': ['dad', 'mom', 'grandpa', 'grandfather', 'grandma',
                   'grandmother', 'politician', 'teenager', 'high schooler', 'pastor',
                   'rabbi', 'teacher', 'toddler'],
        'relation': ['boyfriend', 'girlfriend', 'fuckbuddy', 'mom', 'dad'],
        'celebrity': ['{old_celebrity}', '{current_celebrity}'],
        'old_celebrity': ['Gandhi', 'Hitler', 'Abraham Lincoln',
                          'Albert Einstein', 'Stalin'],
        'current_celebrity': ['Jack Black', 'Obama', 'Bill Murray',
                              'Hannah Montana', 'Mittens the Cat', 'Hamdy', '{gen/karst}',
                              '{gen/Username}'],

        'evidence': ['video', 'website'],
        'the_truth': ['the truth'],  # need better name for this category

        'verb': ['tried to'],
        'normal_action': ['protect', 'fight', 'high five'],
        'odd_action': ['make love to', 'castrate', 'capture', 'kiss'],
        'shows': ['shows', 'reveals', 'knows'],
        'actioning': ['stealing {things}', 'cooking {things}',
                      'eating {things}', 'kissing {things}', 'kissing your {relation}',
                      'talking', 'learning', 'teaching', 'masturbating', 'hugging'],

        'singular_object': ['a {object}'],
        'object': ['toaster', 'fire truck', 'flower', 'dildo', 'sandwich'],
        'bad_thing': ['Nazi', 'fascist', 'Communist', 'pedophile',
                      'nymphomaniac'],
        'weird_thing': ['zombie', 'alien', 'painter', 'American'],

        'things': ['{objects}', '{bad_things}', '{weird_things}', '{animals}'],
        'objects': ['toasters', 'fire trucks', 'flowers', 'dildos',
                    'sandwiches'],
        'bad_things': ['Nazis', 'fascists', 'Communists', 'pedophiles',
                       'nymphomaniacs'],
        'weird_things': ['zombies', 'aliens', 'painters', 'Americans'],

        'singular_animal': ['a {animal}'],
        'animal': ['tiger', 'gorilla', 'dolphin', 'hippo', 'panda', 'duck'],
        'animals': ['tigers', 'gorillas', 'dolphins', 'hippos', 'pandas',
                    'ducks'],

        'be_state': ['be {stated}'],
        'change_state': ['shock', 'impress', 'convince'],
        'stated': ['shocked', 'impressed', 'happy'],
        'emote': ['laugh', 'cry'],

        'topic': ['sex', 'cooking', 'driving', 'fashion', 'make-up', 'Dota',
                  'gaming', 'seduction', 'relationship', 'shopping'],
    }
}
