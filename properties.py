"""Модуль с константами"""
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 64
FONT_NAME = './addons/monospace.ttf'
WHITE = (255, 255, 255)

STANDARD_OBJ_ANIM_PACK = {
    'idle': []
}

# Characters values
DISTANCE_FOR_INTERACT = 100
DEFAULT_CHARACTER_SPEED = 220
DEFAULT_CHARACTER_ANIM_SPEED = {'idle': 0.8,
                                'walk': 0.2}
STANDARD_CHARACTER_ANIM_PACK = {
    'idle_down': [], 'idle_up': [], 'idle_right': [], 'idle_left': [],
    'walk_up': [], 'walk_down': [], 'walk_right': [], 'walk_left': []
}

# Dialog vales
DIALOG_WINDOW_POSITION = (SCREEN_WIDTH/2, SCREEN_HEIGHT-128)

# Player values
TIME_BETWEEN_INTERACT = 0.5
PLAYER_HITBOX_SIZE = (30, 30)
LEVELS_PROPERTIES = {
    1: {'max_health': 100, 'armor': 3, 'max_damage': 20},
    2: {'max_health': 120, 'armor': 5, 'max_damage': 30}
}

LAYERS = {
    'ground': 0,
    'back_decor': 1,
    'back_main': 2,
    'back_npc': 3,
    'player': 4,
    'forward_decor': 5,
    'forward_main': 6,
    'forward_npc': 7,
    'ux': 8
}

MAP = [
    ['c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c'],
    ['c', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['c', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['c', 'x', 'x', 'x', 'x', 'x', 's', 's', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['c', 'x', 'x', 'x', 'x', 's', 's', 's', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['c', 'x', 'x', 'x', 's', 'x', 's', 'x', 'x', 'x', 's', 's', '', 'x', 'x'],
    ['c', 'x', 's', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 's', 's', '', '', ''],
    ['c', 's', 's', 's', 'x', 'c', 'x', 'x', 'x', 'x', 's', '', '', '', ''],
    ['c', 'x', 's', 'x', 'c', 'x', 's', 'x', 'x', 'x', 's', '', '', '', ''],
    ['c', 'x', 'x', 'x', 'x', 'c', 's', 'x', 'x', 'x', 's', '', '', '', ''],
    ['c', 'x', 'x', 'x', 'x', 'x', 's', 's', 'x', 'x', 's', '', '', 'x', 'x'],
    ['c', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['c', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['c', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['c', 's', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c']
]
