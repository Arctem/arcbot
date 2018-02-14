from tavern.raws.raws import TavernException


class DungeonType:

    def __init__(self, name, adjectives=set(), nouns=set(), epithets=set(), monster_reqs=set(), monster_opts=set()):
        self.name = name
        self.adjectives = adjectives
        self.nouns = nouns
        self.epithets = epithets
        self.monster_reqs = monster_reqs
        self.monster_opts = monster_opts


types = {
    DungeonType('cave',
                adjectives={'dank', 'deep', 'subterranean', 'sunken'},
                nouns={'cave', 'mines'},
                epithets={'the underworld', 'the earthmother', 'the mole mother', 'rocks and dirt'},
                monster_reqs={'rat', 'troll'},
                monster_opts={'ancient', 'giant'},
                ),
    DungeonType('jungle',
                adjectives={'overgrown', 'tropical'},
                nouns={'jungle', 'wilds'},
                epithets={'frogs', 'lizard-kings'},
                monster_reqs={'spider', 'lizard', 'frogman'},
                monster_opts={'poison', 'shaman'},
                ),
    DungeonType('magical',
                adjectives={'arcane', 'magic', 'occult'},
                nouns={'nexus', 'sanctum', 'obelisk'},
                epithets={'power', 'knowledge'},
                monster_reqs={'slime'},
                monster_opts={'fire', 'giant', 'shaman'},
                ),
    DungeonType('maze',
                adjectives={'labyrinthian', 'tangled', 'unknown', 'vast', 'confused'},
                nouns={'maze', 'labyrinth', 'warren'},
                epithets={'hedges', 'lost souls', 'the ever wanderer', 'minos'},
                monster_reqs={'rat', 'minotaur', 'hunting'},
                monster_opts={'ancient', 'troll'},
                ),
    DungeonType('tomb',
                adjectives={'ancestral', 'necrotic', 'sacrosanct'},
                nouns={'necropolis', 'tomb', 'crypt'},
                epithets={'ancient kings', 'dead gods', 'the fallen'},
                monster_reqs={'ghost', 'undead', 'skeleton'},
                monster_opts={'ancient', 'rat'},
                ),
}

types = {t.name: t for t in types}
