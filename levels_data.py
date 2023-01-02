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
    "music": "music_and_sound/music/level/embient.mp3"
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
        "rocks": "./levels_data/graphics/decoration2/SandLight.png",
        "sand": "./levels_data/graphics/decoration2/SandLight.png",
        'water': 'levels_data/graphics/decoration/water/hub_water.png',
        'limiters': './levels_data/graphics/decoration2/SandLight.png',
    },
    "TMXData": "levels_data/levels/1/level_1__objects.tmx",
    "move_to": 0,
    "music": "music_and_sound/music/level/Desert theme.mp3"

}

levels = {
    0: level_0,
    1: level_1
}
