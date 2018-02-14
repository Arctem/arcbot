from tavern.tavern_models import Jobs


class MonsterStock:

    def __init__(self, name, hp, min_level, max_level, weaknesses=set(), resistances=set()):
        self.name = name
        self.hp = hp
        self.min_level = min_level
        self.max_level = max_level
        self.weaknesses = weaknesses
        self.resistances = resistances


class MonsterModifier:

    def __init__(self, name, hp=0, level=0, weaknesses=set(), resistances=set()):
        self.name = name
        self.hp = hp
        self.level = level
        self.weaknesses = weaknesses
        self.resistances = resistances

stocks = {
    MonsterStock('ghost',
                 5,
                 2, 4,
                 weaknesses={Jobs.Bard, Jobs.Wizard},
                 resistances={Jobs.Barbarian},
                 ),
    MonsterStock('rat',
                 3,
                 1, 1,
                 weaknesses={Jobs.Barbarian, Jobs.Druid},
                 ),
    MonsterStock('skeleton',
                 4,
                 1, 5,
                 weaknesses={Jobs.Barbarian, Jobs.Bard, Jobs.Wizard},
                 ),
    MonsterStock('slime',
                 4,
                 1, 10,
                 weaknesses={Jobs.Druid, Jobs.Wizard},
                 ),
    MonsterStock('spider',
                 2,
                 1, 5,
                 weaknesses={Jobs.Barbarian, Jobs.Druid, Jobs.Monk},
                 ),
    MonsterStock('troll',
                 10,
                 5, 10,
                 weaknesses={Jobs.Rogue},
                 ),
}
stocks = {s.name: s for s in stocks}

modifiers = {
    MonsterModifier('ancient',
                    level=2,
                    weaknesses={Jobs.Bard},
                    ),
    MonsterModifier('dire',
                    hp=5,
                    ),
    MonsterModifier('giant',
                    hp=10,
                    weaknesses={Jobs.Rogue},
                    ),
    MonsterModifier('fire',
                    level=5,
                    weaknesses={Jobs.Wizard},
                    resistances={Jobs.Monk},
                    ),
    MonsterModifier('poison',
                    level=1,
                    weaknesses={Jobs.Druid},
                    resistances={Jobs.Barbarian},
                    ),
    MonsterModifier('quick',
                    level=1,
                    weaknesses={Jobs.Monk},
                    resistances={Jobs.Barbarian},
                    ),
    MonsterModifier('undead',
                    level=2,
                    weaknesses={Jobs.Wizard},
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
