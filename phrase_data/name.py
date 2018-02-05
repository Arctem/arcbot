data = {
    'name': {
        'template': ['{boss}', '{cog}', '{dwarf}'],  # '{native}', ],

        # TEMPLATES
        'cog': ['{Brit_first} {Cog_last}'],
        'native': ['{Native_first} {Native_last}', '{Native_verbs} With {Native_animals}'],
        'boss': ['{Boss_first} {Boss_last}'],
        'dwarf': ['{Dwarf_first} {Dwarf_last}', '{dwarf}, {dwarf_epithet}'],

        # STEAMPUNK NAMES
        'brit_first': ['{brit_first_male}', '{brit_first_fem}'],
        'brit_first_male': ['Mr.', 'Sir', 'wilbert', 'mudd', 'rooster', 'ruddigore', 'brick', 'thaddeus', 'bollox', 'zebulon', 'egress', 'winston', 'manfred', 'edwind', 'hammond'],
        'brit_first_fem': ['Miss', 'Lady', 'zylphia', 'bellis', 'ada', 'penny', 'kimberly', 'mimsy', 'hattie'],

        'brit_last_premade': ['chuzzlewit', 'warddle', 'scadde', 'beamish', 'toves', 'chuddlewick', 'hammond'],
        'brit_last_ending': ['son', 'bottom'],

        'cog_last': ['{metal}{component}', '{component}{component}', '{metal}{brit_last_ending}', '{component}{brit_last_ending}', '{cog_last_premade}', '{brit_last_premade}'],
        'cog_last_premade': ['bootstrappe', 'coalscofle', 'matchelocke'],

        'metal': ['brass', 'coal', 'steel', 'bronze', 'iron', 'ash', 'salt', 'silver', 'copper'],
        'component': ['cog', 'gimbal', 'gear', 'widget', 'locke', 'saw', 'pipe', 'mill', 'tack', 'whistle'],

        # NATIVE NAMES (unused)
        'native_first': ['{native_verbing}'],
        'native_verbing': ['flying', 'speeding', 'riding', 'hunting', 'dancing', 'laughing'],
        'native_verbs': ['flies', 'runs', 'rides', 'hunts', 'dances', 'laughs'],

        'native_last': ['{native_adj}{native_animal}', '{native_last_premade}'],
        'native_last_premade': ['bullet'],
        'native_adj': ['fast', 'quick', 'hungry', 'big', 'small'],
        'native_animal': ['rabbit', 'buffalo', 'hawk', 'wolf', 'eagle', 'owl'],
        'native_animals': ['rabbits', 'bison', 'hawks', 'wolves', 'eagles', 'owls'],

        # VIDEO GAME BOSS NAMES
        'boss_first': ['{boss_prefix}{boss_first}', '{boss_first}{boss_postfix}', '{boss_title}', '{boss_weather}', '{boss_animal}'],
        'boss_title': ['commander', 'sergeant', 'dr.', 'grand moff'],
        'boss_weather': ['blizzard', 'thunder', 'blaze', 'burn', 'firestorm', 'glacier', 'gravity', 'volt'],
        'boss_animal': ['rabbit', 'buffalo', 'hawk', 'wolf', 'snail', 'stingray', 'beetle', 'eagle', 'octopus', 'ostrich', 'gator', 'hammond'],
        'boss_prefix': ['omni', 'mega', 'giga', 'ultra', 'tri'],
        'boss_postfix': ['oid', 'saurus'],

        'boss_last': ['{boss_prefix}{boss_last}', '{boss_last}{boss_postfix}', '{boss_animal}', '{boss_word}', '{boss_weather}'],
        'boss_word': ['doppler', 'psyche', 'hunter', 'slash', 'dynamo', 'hammond'],

        # DWARVEN NAMES
        'dwarf_first': ['{dwarf_male}', '{dwarf_female}', '{dwarf_syllabic}'],
        'dwarf_male': ['{dwarf_syllable}grim', 'Alaric', 'Benji', 'Dirk', 'Fili', 'Josef', 'Snorri', 'Thorin'],
        'dwarf_female': ['{dwarf_male}a', 'Helga', 'Urist'],
        'dwarf_syllabic': ['{dwarf_syllable}{dwarf_syllable}', '{dwarf_syllabic}{dwarf_syllable}'] * 6 + ["{dwarf_syllabic}'{dwarf_syllabic}"],
        'dwarf_syllable': ['ar', 'ba', 'bom', 'bur', 'brin', 'dwa', 'ell', 'fur', 'ga', 'gara', 'gim', 'grar', 'grim', 'grom' 'grung', 'got' 'hi', 'in', 'ler', 'li', 'lin', 'mal', 'ni', 'ther', 'thor', 'u', 'un', 'ur'],

        'dwarf_last': ['Mc{Profession}', '{dwarf_valuable,metal}{dwarf_actioner}'],
        'profession': ['miner', 'farmer', 'grower', 'weaver', '{weapon}dwarf', 'fisher', 'smith'],
        'dwarf_actioner': ['beater', 'hammerer', 'smither', 'smeller', 'knower', 'keeper', 'shaper'],
        'weapon': ['axe', 'hammer', 'dwarf', 'spear'],

        'dwarf_epithet': ['the {Dwarf_noun,Dwarf_actioner}', '{Relative,Apprentice} of {Dwarf_first} {Dwarf_last}'],
        'dwarf_noun': ['{dwarf_adjective} {dwarf_noun}', '{weapon}', '{dwarf_valuable}', '{metal}', 'deep', 'grim'],
        'dwarf_adjective': ['{metal}', 'granite', 'rock', 'stone', 'elder', 'dark', 'grim'],
        'dwarf_valuable': ['oath', 'grudge', 'horde'],
        'dwarf_title': ['Fist', 'Grom', 'Hammerer', 'Longbeard', '{Metal}breaker', 'Thunderer', 'Quarreller', 'Warden'],

        'relative': ['son', 'daughter', 'dottir', 'heir', 'cousin', 'kin', 'pact-brother', 'pact-sister'],
        'apprentice': ['first {weapon,dwarf_title}', 'regent', 'protege', 'blessed', 'ward'],

        # DWARVEN PLACES
        'dwarf_place': ['the {Dwarf_adjective}{fortress}'],
        'fortress': ['fort', 'keep', 'burrow'],
    }
}
