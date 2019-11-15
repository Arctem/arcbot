
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
    MonsterStock('automaton',
                 1, 4,
                 weaknesses={'barbarian'},
                 strengths={'wizard'},
                 ),
    MonsterStock('bear',
                 3, 7,
                 weaknesses={'druid', 'rogue'},
                 strengths={'wizard'},
                 ),
    MonsterStock('dragon',
                 10, 15,
                 weaknesses={'scholar', 'rogue'},
                 strengths={'barbarian'},
                 ),
    MonsterStock('elemental',
                 2, 8,
                 weaknesses={'druid', 'wizard'},
                 strengths={'monk'},
                 ),
    MonsterStock('fairy',
                 2, 4,
                 weaknesses={'monk', 'bard'},
                 strengths={'barbarian'},
                 ),
    MonsterStock('ghost',
                 2, 4,
                 weaknesses={'scholar', 'wizard'},
                 strengths={'barbarian'},
                 ),
    MonsterStock('goat',
                 1, 3,
                 weaknesses={'druid'},
                 strengths={'wizard'},
                 ),
    MonsterStock('golem',
                 5, 8,
                 weaknesses={'rogue', 'wizard'},
                 strengths={'druid'},
                 ),
    MonsterStock('guard',
                 2, 5,
                 weaknesses={'bard', 'rogue'},
                 strengths={'druid', 'wizard'},
                 ),
    MonsterStock('gurgler',
                 3, 7,
                 weaknesses={},
                 strengths={'bard'},
                 ),
    MonsterStock('hogs',
                 3, 5,
                 weaknesses={'druid', 'monk'},
                 strengths={'bard', 'wizard'},
                 ),
    MonsterStock('knight',
                 5, 8,
                 weaknesses={'bard', 'rogue'},
                 strengths={'druid', 'monk', 'wizard'},
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
    MonsterStock('pimple',
                 1, 2,
                 weaknesses={'barbarian', 'druid'},
                 ),
    MonsterStock('pixie',
                 1, 1,
                 weaknesses={'monk', 'bard'},
                 strengths={'barbarian'},
                 ),
    MonsterStock('rat',
                 1, 1,
                 weaknesses={'barbarian', 'druid'},
                 strengths={'bard', 'wizard'},
                 ),
    MonsterStock('shapeshifter',
                 1, 10,
                 weaknesses={'bard'},
                 strengths={'barbarian'},
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
    MonsterStock('unicorn',
                 7, 10,
                 weaknesses={'druid', 'scholar', 'wizard'},
                 strengths={},
                 ),
    MonsterStock('wolf',
                 2, 4,
                 weaknesses={'druid', 'monk'},
                 strengths={'wizard'},
                 ),
    MonsterStock('yeti',
                 7, 8,
                 weaknesses={'rogue'},
                 ),
}
stocks = {s.name: s for s in stocks}

modifiers = {
    MonsterModifier('ancient',
                    level=2,
                    weaknesses={'scholar'},
                    ),
    MonsterModifier('clever',
                    level=2,
                    weaknesses={'bard'},
                    strengths={'barbarian'},
                    ),
    MonsterModifier('dire',
                    level=3,
                    ),
    MonsterModifier('dumb',
                    level=-1,
                    strengths={'bard'},
                    ),
    MonsterModifier('esteemed',
                    level=1,
                    strengths={'druid'},
                    ),
    MonsterModifier('feral',
                    level=2,
                    strengths={'bard'},
                    ),
    MonsterModifier('fire',
                    level=5,
                    weaknesses={'wizard'},
                    strengths={'monk'},
                    ),
    MonsterModifier('giant',
                    level=1,
                    weaknesses={'rogue'},
                    ),
    MonsterModifier('hunting',
                    level=3,
                    weaknesses={'monk'},
                    strengths={'rogue'},
                    ),
    MonsterModifier('ice',
                    level=2,
                    weaknesses={'barbarian', 'wizard'},
                    strengths={'monk'},
                    ),
    MonsterModifier('poison',
                    level=1,
                    weaknesses={'druid'},
                    strengths={'barbarian'},
                    ),
    MonsterModifier('pulsating',
                    level=2,
                    weaknesses={'rogue'},
                    ),
    MonsterModifier('quick',
                    level=1,
                    weaknesses={'monk'},
                    strengths={'barbarian'},
                    ),
    MonsterModifier('reconstructed',
                    level=3,
                    strengths={'scholar'},
                    ),
    MonsterModifier('servile',
                    weaknesses={'bard', 'barbarian', 'monk'},
                    strengths={'barbarian', 'druid', 'wizard'},
                    ),
    MonsterModifier('shaman',
                    level=3,
                    weaknesses={'scholar', 'wizard'},
                    strengths={'druid'},
                    ),
    MonsterModifier('tiny',
                    level=-1,
                    strengths={'barbarian', 'rogue'},
                    ),
    MonsterModifier('toothy',
                    level=2,
                    weaknesses={'barbarian'},
                    strengths={'druid'},
                    ),
    MonsterModifier('undead',
                    level=2,
                    weaknesses={'wizard'},
                    ),
    MonsterModifier('wind-up',
                    level=1,
                    weaknesses={'barbarian'},
                    strengths={'wizard'},
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
