data = {
    'ration' : {
        'template' : ['You open a {size} {type} and find: {contents}.'],

        'size' : ['small', 'tiny', 'big', 'large', 'medium', 'gigantic'],

        'type' : ['{date} k-ration', 'meal, combat, individual ration',
            '{nationality} c-ration'],

        # because age starts with a vowel and date doesn't
        'date' : ['practically ancient', 'extremely old', 'vintage',
            'well-aged', 'pretty old', 'mostly still edible', 'recentish',
            'brand new', 'nearly expired', 'questionable'],

        'nationality' : ['German', 'Russian', 'Japanese', 'Korean',
            'Norwegian', 'British', 'Italian', 'US'],

        'contents' : ['{acc_package}, {entree}, {side}, {desert}, and {extras}',
            '{acc}, {entree}, and {desert}', '{substitute_entree}, and {extras}',
            '{acc_package}, {entree}, and {desert}', '{substitute_entree}'],

        'coffee' : ['coffee, instant {coffee_type}',
            'Taster\'s Choice instant coffee',
            'coffee instant {coffee_type} {coffee_style}', 'instant coffee',
            'Nestle instant coffee'],

        'coffee_type' : ['type I', 'type II'],

        'coffee_style' : ['style I', 'style II', 'style A'],

        'acc_package' : ['{acc}, {acc1}, {acc2}, {coffee}'],

        'acc' : ['a spork', 'a spoon', 'a sugar packet', 'a creamer packet',
            'toilet paper'],

        'acc1' : ['a pack of cigarettes', 'chewing gum',
            'water purification tablets'],

        'acc2' : ['vitamins', 'a matchbook', 'toothpaste'],

        'entree' : ['a {date} can of {entree_meat}',
            'a {date} can of biscuits', 'a {smell} {entree_meat} bar'],

        'smell' : ['terrible smelling', 'slightly chemical scented', 'rancid'],

        'entree_meat' : ['spaghetti and meatballs', 'bacon', 'cured ham',
            'beef stew'],

        'side' : ['a can of peanut butter', 'a {date} can of {fruit}',
            'a can of {fruit} jelly', 'a {date} jelly bar',
            'a {date} can of {vegetable}', 'a cheese bar'],

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
