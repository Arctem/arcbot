from enum import Enum


class Type(Enum):
    RACE = 1
    WEAPON = 2

data = {
    # RACES
    'human': {
        'name': 'human',
        'type': Type.RACE,
    },

    # WEAPONS
    'spear': {
        'name': 'spear',
        'type': Type.WEAPON,
        'hands': 1,
        'range': 3,
    },
    'pike': {
        'name': 'pike',
        'type': Type.WEAPON,
        'hands': 2,
        'range': 4,
    },
    'short_sword': {
        'name': 'short sword',
        'type': Type.WEAPON,
        'hands': 1,
        'range': 2,
    },
}
