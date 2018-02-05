data = {
    'fate': {
        'template': ['{opening} {event} {battle}! {death}.'],

        'enemy_mod': ['very {enemy_mod}', 'undead', 'giant', 'poison', 'green', 'gaping', 'iron', 'flying', 'fire-breathing', 'asylum', 'diseased', 'hollow', 'fearsome', 'scaly', 'rotten', 'armored', 'enemy', 'shadow', 'jade', 'glacial', 'savage', 'baleful', 'great', 'steel', 'tiny', 'raging', 'annoyed', 'purple', 'sexy', 'naked'],
        'creature': ['{enemy_mod} {creature}'] * 5 + ['skeleton', 'wyvern', 'rat', 'assassin', 'bookshelf', 'drake', 'dragon', 'demon', 'butterfly', 'dog', 'wolf', 'zombie', 'man', 'woman', 'snake', 'lizard', 'giant', 'treant', 'crab', 'bullsquid', 'hunter', 'ant lion', 'donkey', 'monkey', 'USS Wahoo', 'Agnaktor', 'Barroth', 'Qurupeco', 'Arzuros', 'Jaggi', 'Barioth', 'Deviljho', 'Diablos', 'Duramboros', 'Gigginox', 'Gobul', 'Baggi', 'Wroggi', 'Lagombi', 'Ludroth', 'Rathian', 'Rathalos', 'Plesioth', 'Uragaan', 'Volvidon', 'Nibelsnarf', 'drug dealer', 'bear', 'rhino', 'minotaur'],
        'creatures': ['skeletons', 'rats', 'dragons', 'demons', 'butterflies', 'wolves', 'zombies', 'men', 'women', 'snakes', 'crabs', 'ants', 'donkeys', 'submarines', 'cats', 'kittens', 'bears', 'rhino', 'bees', 'cheerleaders'],
        'user_body': ['arm', 'leg', 'toe', 'chest', 'head', 'finger', 'hand', 'foot', 'eye', 'groin'],
        'enemy_body': ['hide', 'shell', 'claws', 'horn', 'armor'],
        'location': ['Undead Asylum', 'Firelink Shrine', 'Undead Burg', 'Undead Parish', 'Depths', 'Blighttown', 'Quelaag\'s Domain', 'The Great Hollow', 'Ash Lake', 'Sen\'s Fortress', 'Anor Londo', 'Painted World of Ariamis', 'Darkroot Garden', 'Darkroot Basin', 'New Londo Ruins', 'The Duke\'s Archives', 'Crystal Cave', 'Demon Ruins', 'Lost Izalith', 'The Catacombs', 'Tomb of Giants', 'Black Mesa', 'City 17', 'The Pacific Ocean', 'Castamere', 'The Wall', 'Westeros', 'Essos', 'Hammond Industries'],
        'hazard_any': ['a {hazard}', '{hazards}'],
        'hazard': ['spike', 'swinging axe', 'fire', 'acid pool', 'bottomless pit', 'chasm', 'banana peel', 'horde of {creatures}', '{container} of {creatures}'],
        'hazards': ['spikes', 'flames', 'spikes', 'banana peels'],
        'container': ['cage', 'pit', 'basket', 'chamber', 'nest'],
        'damaged':  ['poisoned', 'exploded', 'killed', 'murderified', 'castrated', 'defenestrated', 'torpedoed', 'severely inconvenienced', 'pierced', 'severed'],
        'initiated': ['charged', 'roared', 'threw its {weapon_enemy}[enemy_wep]'],
        'weapon_enemy': ['{enemy_mod} {weapon_enemy}'] * 4 + ['claws', 'battle axe', 'spear', 'dart gun', 'teeth', 'bazooka', 'breath', 'katana', 'tentacles', 'club', 'torpedo', 'beak', 'tail', 'tongue'],
        'weapon_user': ['battle axe', 'spear', 'shield', 'katana', 'club', 'fist', 'large rock', 'rubber chicken', 'greatsword', 'nunchucks', 'claymore', 'impressive genitalia'],

        # For battle
        'start': ['that {initiated} at {gen/Username}'],
        'fight': ['{gen/Username} {user_atk}, but the {creature}[enemy] {enemy_react}', 'the {creature}[enemy] {enemy_atk} and {user_react}', 'a nearby {creature} interfered, and {damaged} {gen/Username}\'s {user_body}'],
        'morefight': [', then {fight}'],
        'user_atk': ['swung their {weapon_user}[user_wep]', 'dove towards the {creature}[enemy] in a daring attack'],
        'enemy_atk': ['pushed {gen/Username} towards {hazard_any}', 'attacked with its {weapon_enemy}[enemy_wep]'],
        'user_react': ['{gen/Username} screamed in pain', '{gen/Username}\'s {user_body} was {damaged}', '{gen/Username} narrowly avoided being {damaged}{morefight}', '{gen/Username} blocked with their {weapon_user}[user_wep], which was damaged beyond repair{morefight}'],
        'enemy_react': ['dodged the mighty blow{morefight}', 'blocked the strike with its {weapon_enemy}[enemy_wep]{morefight}', 'let {gen/Username}\'s {weapon_user}[user_wep] glance harmlessly off its {enemy_body}{morefight}', 'turned the attack back on {gen/Username}, and {user_react}'],

        # For death
        'life': ['life-blood', 'will to live', 'soul', 'energy', 'grip on reality'],
        'fading': ['fading', 'slipping away', 'flowing out of them', 'vanishing'],
        'celebrated': ['laughed', 'looked on hungrily', 'prepared to feast', 'hunted for its next victim'],

        'opening': ['Whilst wandering through {location}, {gen/Username}'],
        'event': ['came across a {enemy_mod} {creature}[enemy]', 'was set upon by a {enemy_mod} {creature}[enemy]'],
        'battle': ['{start}! {fight}'],
        'death': ['{gen/Username} felt their {life} {fading} as the {creature}[enemy] {celebrated}', '{gen/Username}\'s broken corpse tumbled into {hazard_any}'],
        #'death' : ['that {damaged} him with its {weapon_enemy}[enemy_wep]!', 'and fled mindlessly into {hazard_any}, spelling his end.'],
    },
}
