data = {
  'name' : {
        'template' : ['{cog}', '{boss}'], #'{native}', ],

        'cog' : ['{Brit_first} {Cog_last}'],
        'native' : ['{Native_first} {Native_last}', '{Native_verbs} With {Native_animals}'],
        'boss' : ['{Boss_first} {Boss_last}'],

        'brit_first' : ['{brit_first_male}', '{brit_first_fem}'],
        'brit_first_male' : ['Mr.', 'Sir', 'wilbert', 'mudd', 'rooster', 'ruddigore', 'brick', 'thaddeus', 'bollox', 'zebulon', 'egress', 'winston', 'manfred', 'edwind', 'hammond'],
        'brit_first_fem' : ['Miss', 'Lady', 'zylphia', 'bellis', 'ada', 'penny', 'kimberly', 'mimsy', 'hattie'],

        'brit_last_premade' : ['chuzzlewit', 'warddle', 'scadde', 'beamish', 'toves', 'chuddlewick', 'hammond'],
        'brit_last_ending' : ['son', 'bottom'],

        'cog_last' : ['{metal}{component}', '{component}{component}', '{metal}{brit_last_ending}', '{component}{brit_last_ending}', '{cog_last_premade}', '{brit_last_premade}'],
        'cog_last_premade' : ['bootstrappe', 'coalscofle', 'matchelocke'],

        'metal' : ['brass', 'coal', 'steel', 'bronze', 'iron', 'ash', 'salt', 'silver', 'copper'],
        'component' : ['cog', 'gimbal', 'gear', 'widget', 'locke', 'saw', 'pipe', 'mill', 'tack', 'whistle'],

        'native_first' : ['{native_verbing}'],
        'native_verbing' : ['flying', 'speeding', 'riding', 'hunting', 'dancing', 'laughing'],
        'native_verbs' : ['flies', 'runs', 'rides', 'hunts', 'dances', 'laughs'],

        'native_last' : ['{native_adj}{native_animal}', '{native_last_premade}'],
        'native_last_premade' : ['bullet'],
        'native_adj' : ['fast', 'quick', 'hungry', 'big', 'small'],
        'native_animal' : ['rabbit', 'buffalo', 'hawk', 'wolf', 'eagle', 'owl'],
        'native_animals' : ['rabbits', 'bison', 'hawks', 'wolves', 'eagles', 'owls'],
        
        'boss_first' : ['{boss_prefix}{boss_first}', '{boss_first}{boss_postfix}', '{boss_title}', '{boss_weather}', '{boss_animal}'],
        'boss_title' : ['commander', 'sergeant', 'dr.'],
        'boss_weather' : ['blizzard', 'thunder', 'blaze', 'burn', 'firestorm', 'glacier', 'gravity', 'volt'],
        'boss_animal' : ['rabbit', 'buffalo', 'hawk', 'wolf', 'snail', 'stingray', 'beetle', 'eagle', 'octopus', 'ostrich', 'gator', 'hammond'],
        'boss_prefix' : ['omni', 'mega', 'giga'],
        'boss_postfix' : ['oid', 'saurus'],
        
        'boss_last' : ['{boss_prefix}{boss_last}', '{boss_last}{boss_postfix}', '{boss_animal}', '{boss_word}', '{boss_weather}'],
        'boss_word' : ['doppler', 'psyche', 'hunter', 'slash', 'dynamo', 'hammond'],
    }
}