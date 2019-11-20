

class Job:

    def __init__(self, name, adjectives=set(), nouns=set()):
        self.name = name
        self.adjectives = adjectives
        self.nouns = nouns

jobs = {
    Job('barbarian',  # Good against fragile things, bad against evasion
        adjectives={'angry', 'raging', 'ravenous'},
        nouns={'barbarian', 'berserker', 'hulk'},
        ),
    Job('bard',  # Good against things they can talk to, bad against things they can't
        adjectives={'charismatic', 'lyrical', 'musical'},
        nouns={'bard', 'charmer'},
        ),
    Job('commoner',  # No particular strengths or weaknesses
        adjectives={'mundane', 'ordinary'},
        nouns={'citizen', 'commoner'},
        ),
    Job('druid',  # Good against natural things, bad against civilization and technology
        adjectives={'all-seeing', 'druidic'},
        nouns={'auspex', 'druid', 'woods-watcher'},
        ),
    Job('monk',  # Good against fast things, bad against things it can't touch
        adjectives={'holy', 'noble'},
        nouns={'monk', 'ninja'},
        ),
    Job('rogue',  # Good against big things, bad against observant things
        adjectives={'sneaky', 'thieving', 'tricky'},
        nouns={'bandit', 'cutpurse', 'trickster'},
        ),
    Job('scholar',  # Good against old things, bad against that which should remain unknown
        adjectives={'knowledgeable', 'well-read', 'wizened'},
        nouns={'antiquarian', 'professor', 'scholar', 'teacher'},
        ),
    Job('wizard',  # Good against magic things, weak against mundane things
        adjectives={'ancient', 'magical'},
        nouns={'warlock', 'witch', 'wizard'},
        ),
}

jobs = {j.name: j for j in jobs}
