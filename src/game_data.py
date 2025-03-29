# Dictionary containing monster information
MONSTERS = {
    1: {
        'name': 'Grass Monster',
        'type': 'grass',
        'weakness': 'grass_sword',
        'description': 'A creature made of twisted vines and leaves',
        'defeat_message': 'The grass sword slices through the plant monster!',
        'image': 'Grass Monster.png',
        'emoji_fallback': '🌿'
    },
    2: {
        'name': 'Fire Monster',
        'type': 'fire',
        'weakness': 'fire_sword',
        'description': 'A blazing entity of pure flame',
        'defeat_message': 'The fire sword extinguishes the flame monster!',
        'image': 'Fire Monster.png',
        'emoji_fallback': '🔥'
    },
    3: {
        'name': 'Water Monster',
        'type': 'water',
        'weakness': 'water_sword',
        'description': 'A fluid creature of rushing water',
        'defeat_message': 'The water sword disperses the water monster!',
        'image': 'Water Monster.png',
        'emoji_fallback': '💧'
    }
}

# Dictionary containing sword information
SWORDS = {
    'grass_sword': {
        'name': 'Grass Sword',
        'type': 'grass',
        'description': 'A blade infused with nature\'s power',
        'image': 'Grass Sword.png',
        'emoji_fallback': '🌿'
    },
    'fire_sword': {
        'name': 'Fire Sword',
        'type': 'fire',
        'description': 'A sword burning with eternal flame',
        'image': 'Fire Sword.png',
        'emoji_fallback': '🔥'
    },
    'water_sword': {
        'name': 'Water Sword',
        'type': 'water',
        'description': 'A blade flowing with liquid energy',
        'image': 'Water Sword.png',
        'emoji_fallback': '💧'
    }
}

# Dictionary containing item information
ITEMS = {
    'key': {
        'name': 'Magic Key',
        'description': 'Opens treasure chests containing elemental swords',
        'image': 'key.png',
        'emoji_fallback': '🔑'
    },
    'chest': {
        'name': 'Treasure Chest',
        'description': 'Contains powerful elemental swords',
        'image': 'Chest.png',
        'emoji_fallback': '📦'
    },
    'door': {
        'name': 'Magic Door',
        'description': 'Portal to the next level',
        'image': 'Door.png',
        'emoji_fallback': '🚪'
    }
}

def get_monster_info(level):
    """Get monster information for a specific level"""
    return MONSTERS.get(level, None)

def get_sword_info(sword_type):
    """Get sword information by type"""
    return SWORDS.get(sword_type, None)

def get_item_info(item_type):
    """Get item information by type"""
    return ITEMS.get(item_type, None)

def get_monster_description(level):
    """Get the description of a monster by level"""
    monster = MONSTERS.get(level, None)
    return monster['description'] if monster else "Unknown monster"

def get_sword_description(sword_type):
    """Get the description of a sword by type"""
    sword = SWORDS.get(sword_type, None)
    return sword['description'] if sword else "Unknown sword"

def get_defeat_message(level):
    """Get the defeat message for a monster by level"""
    monster = MONSTERS.get(level, None)
    return monster['defeat_message'] if monster else "Monster defeated!" 