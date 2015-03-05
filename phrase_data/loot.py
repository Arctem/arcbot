data = {
  'loot' : {
        'template' : ['{opening}, {encounter}'],

        'opening' : ['While {adventuring} {place}'],
        'adventuring' : ['delving into', 'journeying through',
            'sneaking through', 'exploring'],
        'place' : ['a {big_creature}\'s lair'],

        'encounter' : ['you find {item} {location}!'],
        'location' : ['under a {dungeon_thing}', 'inside a {dungeon_container}'],

        'dungeon_thing' : ['{creature} skeleton', '{dungeon_container}'],
        'dungeon_container' : ['treasure chest', 'crate',
            'dead {creature}\'s {personal_container}'],
        'personal_container' : ['pouch', 'backpack', 'satchel'],

        'creature' : ['adventurer', 'goblin', 'orc', 'elf', 'dwarf', 'kobold'],
        'big_creature' : ['dragon', 'troll'],

        'item' : ['a {equipment}', '{Dnd/relic}'],
        'equipment' : ['{weapon}', '{armor}'],

        'weapon' : ['{general_adj,weapon_adj} {weapon}',
            '{general_adj,weapon_adj,blunt_adj} {blunt_weapon}',
            '{general_adj,weapon_adj,slash_adj} {slash_weapon}',
        	'{general_adj,weapon_adj,stab_adj} {stab_weapon}'],

        'blunt_weapon' : ['mace', 'hammer', 'warhammer', 'club'],
        'slash_weapon' : ['{sword}', 'dagger', 'katana', 'axe'],
        'stab_weapon' : ['spear', 'shiv', 'pike', 'halberd'],

        'sword' : ['sword', 'bastard sword', 'greatsword', 'longsword'],

        'general_adj' : ['flaming', 'demonic', 'ancient', 'holy', 'vibrating',
            'screaming', 'glowing', 'dank', 'miniature', 'toy',
            'erotic', 'invisible', 'hovering', 'opinionated', 'heavy',
            '{attr_change} to {char_stat}', '{metal}', '{odd_material}',
            'illusory', 'vorpal', 'totally ordinary', 'illuminated',
            'sultry', 'orgasmatronic'],
        'weapon_adj' : ['notched', 'rusted', 'two-handed', 'double-sided',
            '{attr_change} to {weapon_stat}'],
        'blunt_adj' : ['spiked'],
        'slash_adj' : ['razor-thin', 'dull'],
        'stab_adj' : ['collapsible'],
        'armor_adj' : ['{clothing_material}', 'reinforced',
            'one-size-fits-all', '{attr_change} to {armor_stat}', 'too tight',
            'revealing', 'gender-neutral', 'men\'s', 'women\'s'],
        'torso_adj' : ['{attr_change} to {torso_stat}', 'fitted'],
        'head_adj' : ['tall', 'feathered'],
        'limb_adj' : ['assless', '{attr_change} to {limb_stat}'],
        'foot_adj' : ['kicking', 'climbing'],
        'hand_adj' : ['punching', 'climbing'],

        'attr_change' : ['+1', '-1', '+2'],
        'char_stat' : ['strength', 'dexterity', 'wisdom', 'intelligence',
            'charisma', 'consitution', 'seduction', 'jumping', 'not dying',
            'dancing', 'yodeling', 'plumbing'],
        'weapon_stat' : ['swinging wildly in all directions'],
        'armor_stat' : ['deflection', 'wearing armor'],
        'torso_stat' : ['bust size', 'boobs', 'abs'],
        'limb_stat' : ['mail enhancement', 'male enhancement'],

        'armor' : ['{general_adj,armor_adj} {armor}',
            '{general_adj,armor_adj,torso_adj} {torso_armor}',
            '{general_adj,armor_adj,head_adj} {head_armor}',
            '{general_adj,armor_adj,limb_adj} {limb_armor}',
            '{general_adj,armor_adj,foot_adj} {foot_armor}',
            '{general_adj,armor_adj,hand_adj} {hand_armor}'],

        'torso_armor' : ['breastplate', 'chainmail',
            '{clothing_material} armor'],
        'head_armor' : ['helm', 'cap'],
        'limb_armor' : ['bracer', 'greaves', 'leggings', 'pants'],
        'foot_armor' : ['shoes', 'boots', 'slippers'],
        'hand_armor' : ['gloves', 'gauntlets'],

        'clothing_material' : ['{metal}', '{odd_material}', '{soft_material}'],
        'metal' : ['silver', 'iron', 'steel', 'bronze', 'copper', 'gold',
            'mithril'],
        'odd_material' : ['ice', 'stone', 'ebony', 'flame', 'marble', 'uranium',
            'cheese'],
        'soft_material' : ['leather', 'cloth', 'silk'],
    }
}