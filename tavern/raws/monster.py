
class MonsterStock:

    def __init__(self, name, min_level, max_level, weaknesses=set(), strengths=set()):
        self.name = name
        self.min_level = min_level
        self.max_level = max_level
        self.weaknesses = weaknesses
        self.strengths = strengths


class MonsterModifier:

    def __init__(self, name, level=0, weaknesses=set(), strengths=set()):
        self.name = name
        self.level = level
        self.weaknesses = weaknesses
        self.strengths = strengths

stocks = {
    MonsterStock('ghost',
                 2, 4,
                 weaknesses={'scholar', 'wizard'},
                 strengths={'barbarian'},
                 ),
    MonsterStock('lizard',
                 2, 4,
                 weaknesses={'monk', 'druid'},
                 strengths={'bard'},
                 ),
    MonsterStock('frogman',
                 1, 8,
                 weaknesses={'barbarian', 'bard', 'druid'},
                 ),
    MonsterStock('minotaur',
                 7, 13,
                 weaknesses={'bard', 'rogue', 'wizard'},
                 ),
    MonsterStock('rat',
                 1, 1,
                 weaknesses={'barbarian', 'druid'},
                 strengths={'bard'},
                 ),
    MonsterStock('skeleton',
                 1, 5,
                 weaknesses={'barbarian', 'scholar', 'wizard'},
                 ),
    MonsterStock('slime',
                 1, 10,
                 weaknesses={'druid', 'wizard'},
                 strengths={'bard'},
                 ),
    MonsterStock('spider',
                 1, 5,
                 weaknesses={'barbarian', 'druid', 'monk'},
                 strengths={'bard'},
                 ),
    MonsterStock('troll',
                 5, 10,
                 weaknesses={'bard', 'rogue'},
                 ),
}
stocks = {s.name: s for s in stocks}

modifiers = {
    MonsterModifier('ancient',
                    level=2,
                    weaknesses={'scholar'},
                    ),
    MonsterModifier('dire',
                    level=3,
                    ),
    MonsterModifier('clever',
                    level=2,
                    weaknesses={'bard'},
                    strengths={'barbarian'},
                    ),
    MonsterModifier('dumb',
                    strengths={'bard'},
                    ),
    MonsterModifier('giant',
                    weaknesses={'rogue'},
                    ),
    MonsterModifier('hunting',
                    level=3,
                    weaknesses={'monk'},
                    strengths={'rogue'},
                    ),
    MonsterModifier('fire',
                    level=5,
                    weaknesses={'wizard'},
                    strengths={'monk'},
                    ),
    MonsterModifier('poison',
                    level=1,
                    weaknesses={'druid'},
                    strengths={'barbarian'},
                    ),
    MonsterModifier('quick',
                    level=1,
                    weaknesses={'monk'},
                    strengths={'barbarian'},
                    ),
    MonsterModifier('undead',
                    level=2,
                    weaknesses={'wizard'},
                    ),
    MonsterModifier('shaman',
                    level=3,
                    weaknesses={'scholar', 'wizard'},
                    strengths={'druid'},
                    ),
}
modifiers = {m.name: m for m in modifiers}


def get_monster_options(required, optional):
    options = {
        'stocks': {stocks[stock] for stock in required | optional if stock in stocks},
        'required_stocks': {stocks[stock] for stock in required if stock in stocks},
        'optional_stocks': {stocks[stock] for stock in optional if stock in stocks},

        'modifiers': {modifiers[modifier] for modifier in required | optional if modifier in modifiers},
        'required_modifiers': {modifiers[modifier] for modifier in required if modifier in modifiers},
        'optional_modifiers': {modifiers[modifier] for modifier in optional if modifier in modifiers},
    }
    options['required'] = options['required_stocks'] | options['required_modifiers']
    options['optional'] = options['optional_stocks'] | options['optional_modifiers']
    return options
