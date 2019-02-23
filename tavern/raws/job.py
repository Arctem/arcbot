

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
    Job('bard',  # Good against things they can talk to
        adjectives={'charismatic', 'lyrical', 'musical'},
        nouns={'bard', 'charmer'},
        ),
    Job('commoner',  # No particular strengths or weaknesses
        adjectives={'mundane', 'ordinary'},
        nouns={'citizen', 'commoner'},
        ),
    Job('druid',  # Good against natural things, bad against technology
        adjectives={'all-seeing', 'druidic'},
        nouns={'auspex', 'druid', 'woods-watcher'},
        ),
    Job('monk',  # Good against fast things, bad against things it can't touch
        adjectives={'holy', 'noble'},
        nouns={'monk'},
        ),
    Job('rogue',  # Good against big things
        adjectives={'sneaky', 'thieving', 'tricky'},
        nouns={'bandit', 'cutpurse', 'trickster'},
        ),
    Job('scholar',  # Good against old things
        adjectives={'knowledgeable', 'well-read'},
        nouns={'antiquarian', 'professor', 'scholar', 'teacher'},
        ),
    Job('wizard',  # Good against magic things
        adjectives={'ancient', 'magical'},
        nouns={'witch', 'wizard'},
        ),
}

jobs = {j.name: j for j in jobs}
