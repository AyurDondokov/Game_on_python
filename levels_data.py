"""информация о уровнях"""
"""Порядок в MAP важен!!"""

level_0 = {
    "MAP": {
        'limiters': 'levels_data/levels/0/level_0__limiters.csv',
        'sky': 'levels_data/levels/0/level_0__layer_with_sky.csv',
        'island ends': 'levels_data/levels/0/level_0__layer_with_ends_of_the_island.csv',
        'grass': 'levels_data/levels/0/level_0__layer_with_grass.csv',
        'sand': 'levels_data/levels/0/level_0__layer_with_sand.csv',
        'sand hole': 'levels_data/levels/0/level_0__layer_with_sand_hole.csv',
        'crater': 'levels_data/levels/0/level_0__layer_with_crater.csv',
        'water': 'levels_data/levels/0/level_0__layer_with_water.csv',
        'character': 'levels_data/levels/0/level_0__layer_with_character.csv',

    },

    "TileSet": {
        'portal components': 'levels_data/graphics/decoration/ruined_portal/destroy_portal_components.png',

        'island ends': 'levels_data/graphics/decoration/ends_of_island/ends_of_island.png',
        'grass': 'levels_data/graphics/decoration/grass/hub_grass.png',
        'rocks': ['levels_data/graphics/decoration/rocks/rock1.png', 'levels_data/graphics/decoration/rocks/rock2.png'],
        'sand': 'levels_data/graphics/decoration/sand/hub_sand.png',
        'sand hole': 'levels_data/graphics/decoration/sand/water_hole.png',
        'sky': 'levels_data/graphics/decoration/sky/sky.png',
        'water': 'levels_data/graphics/decoration/water/hub_water.png',
        'limiters': 'levels_data/graphics/decoration/limiters/limiters.png',
        'crater': 'levels_data/graphics/decoration/crater/hub_crater.png'
    },
    "TMXData": "levels_data/levels/0/level_objects.tmx",
    "move_to": 1,
    "music": "music_and_sound/music/level/embient.mp3",
    "battles": {
        0: {"enemies": ["tumbleweed", "tumbleweed"],
            "music_path": "./music_and_sound/music/fighting/Nctrnm - Cactus.mp3"},
        1: {"enemies": ["varan"], "music_path":
            "./music_and_sound/music/fighting/Frau Holle - Sand Cave.mp3"},
        2: {"enemies": ["mummy", "mummy"],
            "music_path": "./music_and_sound/music/fighting/Simon Mathewson - Sand.mp3"}
    }
}
level_1 = {
    "MAP": {
        "character": "levels_data/levels/1/level_1___character.csv",
        "limiters": "levels_data/levels/1/level_1___limiters.csv",
        "water": "levels_data/levels/1/level_1___water.csv",
        "sand": "levels_data/levels/1/level_1___sand_ground.csv",
        "rocks": "levels_data/levels/1/level_1___rocks.csv",
    },

    "TileSet": {
        "rocks": "./levels_data/graphics/desert_tileset/tileset.png",
        "footpath": "./levels_data/graphics/desert_tileset/tileset.png",
        "sand": "./levels_data/graphics/desert_tileset/tileset.png",
        'water': 'levels_data/graphics/desert_tileset/tileset.png',
        'limiters': './levels_data/graphics/decoration2/SandLight.png',
    },
    "TMXData": "levels_data/levels/1/level_1__objects.tmx",
    "move_to": 0,
    "music": "music_and_sound/music/level/Desert theme.mp3",
    "battles": {
        0: {"enemies": ["tumbleweed", "tumbleweed"],
            "music_path": "./music_and_sound/music/fighting/Nctrnm - Cactus.mp3"},
        1: {"enemies": ["varan"], "music_path":
            "./music_and_sound/music/fighting/Frau Holle - Sand Cave.mp3"},
        2: {"enemies": ["mummy", "mummy"],
            "music_path": "./music_and_sound/music/fighting/Simon Mathewson - Sand.mp3"}
    }
}

level_2 = {
    "MAP": {
        "character": "levels_data/levels/2/level_2__character.csv",
        "green": "levels_data/levels/2/level_2__green.csv",
        "limeters": "levels_data/levels/2/level_2__limeters.csv",
        "maze": "levels_data/levels/2/level_2__maze.csv",
        "pink": "levels_data/levels/2/level_2__pink.csv",
    },

    "TileSet": {
        "green": "./levels_data/graphics/decoration3/background/background_1.png",
        "pink": "./levels_data/graphics/decoration3/background/background_2.png",
        'maze': 'levels_data/graphics/decoration3/background/maze.png',
        'limiters': './levels_data/graphics/decoration3/limiters/limiters.png',
        "character":'levels_data/graphics/decoration3/character/start.png'
    },
    "TMXData": "levels_data/levels/2/level_2_object.tmx",
    "move_to": 0,
    "music": "music_and_sound/music/level/world2.mp3",
    "battles": {
        0: {"enemies": ["tumbleweed", "tumbleweed"],
            "music_path": "./music_and_sound/music/fighting/Nctrnm - Cactus.mp3"},
        1: {"enemies": ["varan"], "music_path":
            "./music_and_sound/music/fighting/Frau Holle - Sand Cave.mp3"},
        2: {"enemies": ["mummy", "mummy"],
            "music_path": "./music_and_sound/music/fighting/Simon Mathewson - Sand.mp3"}
    }
}

levels = {
    0: level_0,
    1: level_1,
    2: level_2,
}
