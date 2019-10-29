class DungeonType:

    def __init__(self, name, adjectives=set(), nouns=set(), epithets=set(), monster_reqs=set(), monster_opts=set()):
        self.name = name
        self.adjectives = adjectives
        self.nouns = nouns
        self.epithets = epithets
        self.monster_reqs = monster_reqs
        self.monster_opts = monster_opts

# Ideas for dungeons:
# Normal: dingy, cult
# Rare:
# Joke: Bureaucratic, meme (steamed as adjective)

types = {
    DungeonType('cave',
                adjectives={'dank', 'deep', 'subterranean', 'sunken'},
                nouns={'cave', 'mines'},
                epithets={'the underworld', 'the earthmother', 'the mole mother', 'rocks and dirt'},
                monster_reqs={'rat', 'troll'},
                monster_opts={'ancient', 'giant'},
                ),
    DungeonType('clockwork',
                adjectives={'clockwork', 'mechanized'},
                nouns={'contraption', 'engine', 'machine'},
                epithets={'endless gears', 'perpetual motion'},
                monster_reqs={'automaton', 'golem', 'wind-up'},
                monster_opts={'quick', 'reconstructed'},
                ),
    DungeonType('feyland',
                adjectives={'half-forgotten', 'ever-fading', 'mythic'},
                nouns={'dream', 'fable'},
                epithets={'wonders', 'hidden desires', 'the fey'},
                monster_reqs={'fairy', 'pixie', 'shapeshifter', 'unicorn'},
                monster_opts={'clever'},
                ),
    DungeonType('flesh',
                adjectives={'blinking', 'bloody', 'fleshy', 'ruptured'},
                nouns={'growth', 'maw', 'tumor'},
                epithets={'clotted corpses', 'maggots', 'meat', 'tendons', 'tissue', 'skittering things'},
                monster_reqs={'pimple', 'gurgler', 'toothy'},
                monster_opts={'pulsating'},
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
                monster_reqs={'slime', 'elemental'},
                monster_opts={'fire', 'giant', 'shaman'},
                ),
    DungeonType('manor',
                adjectives={'aristocratic', 'majestic', 'noble', 'regal'},
                nouns={'castle', 'estate', 'manor', 'palace'},
                epithets={'king friedrich v', 'duchess gwendolynn', "the queen's retreat" 'the royal hunt'},
                monster_reqs={'guard', 'knight', 'esteemed'},
                monster_opts={'ancient', 'servile', 'hunting'},
                ),
    DungeonType('maze',
                adjectives={'labyrinthian', 'tangled', 'unknown', 'vast', 'confused'},
                nouns={'maze', 'labyrinth', 'warren'},
                epithets={'hedges', 'lost souls', 'the ever wanderer', 'minos'},
                monster_reqs={'rat', 'minotaur', 'hunting'},
                monster_opts={'ancient', 'troll'},
                ),
    # DungeonType('nightmare',
    #             adjectives={'illogical'},
    #             nouns={'abomination', 'void'},
    #             epithets={'a thousand eyes', 'abominations'},
    #             monster_reqs={'abomination', 'imposter'},
    #             monster_opts={},
    #             ),
    DungeonType('tomb',
                adjectives={'ancestral', 'necrotic', 'sacrosanct'},
                nouns={'necropolis', 'tomb', 'crypt'},
                epithets={'ancient kings', 'dead gods', 'the fallen'},
                monster_reqs={'ghost', 'undead', 'skeleton'},
                monster_opts={'ancient', 'rat'},
                ),
    DungeonType('volcano',
                adjectives={'burning', 'erupting'},
                nouns={'crucible', 'volcano'},
                epithets={'endless fire', 'lava'},
                monster_reqs={'fire', 'elemental', 'dragon'},
                monster_opts={'lizard'},
                ),
}

types = {t.name: t for t in types}
