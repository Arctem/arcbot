data = {
    'ration' : {
        'template' : ['You open a {size} {type} and find: {contents}'],

        'size' : ['small', 'tiny', 'big', 'large', 'medium', 'gigantic'],

        'type' : ['{date} k-ration', 'meal, combat, individual ration',
            '{nationality} c-ration'],

        # because age starts with a vowel and date doesn't
        'date' : ['practically ancient', 'extremely old', 'vintage',
            'well-aged', 'pretty old', 'mostly still edible', 'recentish',
            'brand new', 'nearly expired', 'questionable'],

        'nationality' : ['German', 'Russian', 'Japanese', 'Korean',
            'Norwegian', 'British', 'Italian', 'US'],

        'contents' : ['{acc_package}, {entree}, {side}, {desert}, {extras}',
            '{acc}, {entree}, {desert}', '{substitute_entree}, {extras}',
            '{acc_package}, {entree}, {desert}', '{substitute_entree}'],

        'acc_package' : ['{acc}, {acc1}, {acc2}'],

        'acc' : ['a spork', 'a spoon', 'a sugar packet', 'a creamer packet',
            'toilet paper'],

        'acc1' : ['a pack of cigarettes', 'chewing gum',
            'water purification tablets'],

        'acc2' : ['vitamins', 'a matchbook', 'toothpaste'],

        'entree' : ['a {date} can of {entree_meat}',
            'a {date} can of biscuits'],

        'entree_meat' : ['spaghetti and meatballs', 'bacon', 'cured ham',
            'beef stew'],

        'side' : ['a can of peanut butter', 'a {date} can of {fruit}',
            'a can of {fruit} jelly', 'a {date} jelly bar',
            'a {date} can of {vegetable}'],

        'fruit' : ['pineapple', 'apple', 'pear', 'lemon', 'lime'],

        'vegetable' : ['corn', 'carrots', 'potatoes', 'cabbage'],

        'desert' : ['a vanilla cream disk', 'a chocolate cream disk',
            'a malted milk-dextrose bar', 'an unnamed hard candy',
            'a roll of Smarties', 'a chocolate bar'],

        'extras' : ['a flameless ration heater', 'a plastic bag',
            'a list of the contents', 'a P-38 can opener'],

        'substitute_entree' : ['3 boullion cubes', 'a compressed food bar',],
    },
}
