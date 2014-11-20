data = {
  'clickbait' : {
        'template' : ['{crazy_event} {emote_stinger}', '{crazy_event}', '{crazy_question} {evidence_stinger}', '{crazy_question}'],

        'crazy_event' : ['{Singular_person,Celebrity} {verb} {normal_action,odd_action} {singular_thing,singular_animal}!'],
        'crazy_question' : ['Was {Old_celebrity} a {bad_thing,weird_thing}?', 'Is {Current_celebrity} a {bad_thing,weird_thing}?'],

        #'stinger' : [],
        'evidence_stinger' : ['this {evidence,person} {shows} {the_truth}.', 'this {evidence} will {change_state} you!', 'the answer will {change_state} you!'],
        'emote_stinger' : ['first you\'ll {emote,be_state}, then you\'ll {emote,be_state}!', 'You won\'t believe what happens next.'],

        'singular_person' : ['this {person}'],
        'person' : ['dad', 'mom', 'grandpa', 'grandfather', 'grandma', 'grandmother', 'politician', 'teenager', 'high schooler', 'pastor', 'rabbi', 'teacher'],
        'celebrity' : ['{old_celebrity}', '{current_celebrity}'],
        'old_celebrity' : ['Gandhi', 'Hitler', 'Abraham Lincoln', 'Albert Einstein', 'Stalin'],
        'current_celebrity' : ['Jack Black', 'Obama', 'Bill Murray',
            'Mittens the Cat', 'Hamdy', '{gen/karst}', '{Username}'],

        'evidence' : ['video', 'website'],
        'the_truth' : ['the truth'], #need better name for this category

        'verb' : ['tried to'],
        'normal_action' : ['protect', 'fight', 'high five'],
        'odd_action' : ['make love to', 'castrate', 'capture', 'kiss'],
        'shows' : ['shows', 'reveals', 'knows'],

        'singular_thing' : ['a {thing}'],
        'thing' : ['toaster', 'fire truck', 'flower', 'dildo'],
        'singular_animal' : ['a {animal}'],
        'animal' : ['tiger', 'gorilla', 'dolphin', 'hippo', 'panda'],

        'be_state' : ['be {stated}'],
        'change_state' : ['shock', 'impress', 'convince'],
        'stated' : ['shocked', 'impressed', 'happy'],
        'emote' : ['laugh', 'cry'],
        'bad_thing' : ['Nazi', 'fascist', 'Communist', 'pedophile', 'nymphomaniac'],
        'weird_thing' : ['zombie', 'alien', 'painter', 'American'],
    }
}