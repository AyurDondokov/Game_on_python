import math
from enum import Enum

"""Модуль с константами"""
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FPS = 120
TILE_SIZE = 64

FONT_NAME = './addons/Roboto-Regular.ttf'
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)

VERTICAL_TILE_NUMBER = math.ceil(SCREEN_HEIGHT / TILE_SIZE)

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
DIALOG_WINDOW_POSITION = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 128)

# UI
HEALTH_BAR_POS = (-50, 0)
HEALTH_TEXT_POS = (15, 8)
EXP_BAR_POS = (-50, 40)
EXP_TEXT_POS = (25, 38)
HEALTH_BAR_SIZE = (240, 25)
EXP_BAR_SIZE = (240, 10)
EXP_BAR_COLOR = (0, 10, 240)
LEVEL_TEXT_POS = (SCREEN_WIDTH-100, 10)

# Player values
TIME_BETWEEN_INTERACT = 0.5
PLAYER_HITBOX_SIZE = (30, 30)
LEVELS_PROPERTIES = {
    1: {'max_health': 100, 'defence': 30, 'max_damage': 20, 'heal': 25, 'exp_to_next': 10},
    2: {'max_health': 120, 'defence': 50, 'max_damage': 30, 'heal': 30, 'exp_to_next': 10},
    3: {'max_health': 140, 'defence': 60, 'max_damage': 50, 'heal': 35, 'exp_to_next': 15},
    4: {'max_health': 160, 'defence': 80, 'max_damage': 60, 'heal': 45, 'exp_to_next': 15},
    5: {'max_health': 180, 'defence': 100, 'max_damage': 70, 'heal': 50, 'exp_to_next': 20},
    6: {'max_health': 200, 'defence': 120, 'max_damage': 80, 'heal': 55, 'exp_to_next': 20},
    7: {'max_health': 220, 'defence': 140, 'max_damage': 90, 'heal': 60, 'exp_to_next': 25},
    8: {'max_health': 240, 'defence': 160, 'max_damage': 100, 'heal': 65, 'exp_to_next': 25},
    9: {'max_health': 260, 'defence': 180, 'max_damage': 110, 'heal': 70, 'exp_to_next': 30},
    10: {'max_health': 280, 'defence': 200, 'max_damage': 120, 'heal': 80, 'exp_to_next': 30}
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

# Battle system
BATTLE_MOVES = Enum('BattleMoves', 'attack heal block run')
BATTLE_STATES = Enum('BattleStates', 'choose_move stash_damage selecting_enemy waiting')

BATTLE_PROG_BAR_SIZE = (220, 20)
BATTLE_PROG_BAR_COLOR = (220, 0, 0)

BATTLE_SHAKE_INTENSITY = 7
BATTLE_SHAKE_SPEED = 100
BATTLE_SHAKE_TIME = 500
BATTLE_ATTACK_TIME = 300

BATTLE_RUN_CHANCE = 20
BATTLE_MOVE_TIME = 600

BATTLE_ENEMY_POS_X = SCREEN_WIDTH * 0.25
BATTLE_PLAYER_POS = (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT / 2)

DEFAULT_PLAYER_BATTLE_SPRITE = "./sprites/main_character/fighting/fighting_readiness.png"

BATTLE_ACTIONS_BAR_POS = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
BATTLE_BUTTONS_POS = ((SCREEN_WIDTH / 5, SCREEN_HEIGHT - 100), (SCREEN_WIDTH / 5 * 2, SCREEN_HEIGHT - 100),
                      (SCREEN_WIDTH / 5 * 3, SCREEN_HEIGHT - 100), (SCREEN_WIDTH / 5 * 4, SCREEN_HEIGHT - 100))

BATTLE_SLIDER_POS = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200)
BATTLE_SLIDER_SPEED = 500

# Enemies
mummy = {
    "image_path": "./sprites/enemies/mummy/mummy_fighting.png",
    "max_health": 100,
    "max_damage": 10,
    "defence": 20,
    "heal": 5,
    "new_phase_enemies": [],
    "exp": 5
}
pig = {
    "image_path": "./sprites/enemies/pig/pig_fighting.png",
    "max_health": 100,
    "max_damage": 10,
    "defence": 20,
    "heal": 10,
    "new_phase_enemies": [],
    "exp": 5
}
keanu = {
    "image_path": "./sprites/enemies/tumbleweed/keanu.png",
    "max_health": 50,
    "max_damage": 15,
    "defence": 30,
    "heal": 15,
    "new_phase_enemies": [],
    "exp": 2
}
tumbleweed = {
    "image_path": "./sprites/enemies/tumbleweed/tumbleweed.png",
    "max_health": 30,
    "max_damage": 5,
    "defence": 10,
    "heal": 10,
    "new_phase_enemies": [keanu],
    "exp": 1
}
varan = {
    "image_path": "./sprites/enemies/varan/varan_fighting.png",
    "max_health": 50,
    "max_damage": 15,
    "defence": 15,
    "heal": 15,
    "new_phase_enemies": [],
    "exp": 20
}
stump = {
    "image_path": "./sprites/enemies/stump/stump_fighting.png",
    "max_health": 100,
    "max_damage": 10,
    "defence": 20,
    "heal": 10,
    "new_phase_enemies": [],
    "exp": 5
}
leaf = {
    "image_path": "./sprites/enemies/leaf/leaf_2.png",
    "max_health": 100,
    "max_damage": 10,
    "defence": 20,
    "heal": 10,
    "new_phase_enemies": [],
    "exp": 5
}
slug_mini1 = {
    "image_path": "./sprites/enemies/slug/mini/slug_1.png",
    "max_health": 100,
    "max_damage": 10,
    "defence": 20,
    "heal": 10,
    "new_phase_enemies": [],
    "exp": 5
}
slug_mini2 = {
    "image_path": "./sprites/enemies/slug/mini/slug_1.png",
    "max_health": 100,
    "max_damage": 10,
    "defence": 20,
    "heal": 10,
    "new_phase_enemies": [],
    "exp": 5
}
slug = {
    "image_path": "./sprites/enemies/slug/normal/slug_1.png",
    "max_health": 100,
    "max_damage": 10,
    "defence": 20,
    "heal": 10,
    "new_phase_enemies": [slug_mini1, slug_mini2],
    "exp": 5
}

BATTLE_ENEMIES = {
    "mummy": mummy,
    "pig": pig,
    "keanu": keanu,
    "tumbleweed": tumbleweed,
    "varan": varan,
    "stump": stump,
    "slug_mini1": slug_mini1,
    "slug_mini2": slug_mini2,
    "slug": slug,
    "leaf": leaf,

}

DEFAULT_EFFECT_ANIM_SPEED = 0.2
