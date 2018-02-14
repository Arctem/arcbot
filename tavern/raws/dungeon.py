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
                adjectives={'deep', 'subterranean', 'sunken'},
                nouns={'cave', 'mines'},
                epithets={'the underworld'},
                monster_reqs={'rat', 'troll'},
                monster_opts={'ancient', 'giant'},
                ),
    DungeonType('tomb',
                adjectives={'ancestral', 'necrotic', 'sacrosanct'},
                nouns={'necropolis', 'tomb', 'crypt'},
                epithets={'ancient kings', 'dead gods', 'the fallen'},
                monster_reqs={'ghost', 'undead', 'skeleton'},
                monster_opts={'ancient', 'rat'},
                ),
    DungeonType('jungle',
                adjectives={'overgrown', 'tropical'},
                nouns={'jungle', 'wilds'},
                epithets={'frogs', 'lizard-kings'},
                monster_reqs={'spider'},
                monster_opts={'poison'},
                ),
    DungeonType('magical',
                adjectives={'arcane', 'magic', 'occult'},
                nouns={'nexus'},
                epithets={'power'},
                monster_reqs={'slime'},
                monster_opts={'fire', 'giant'},
                ),
}

types = {t.name: t for t in types}
