import math
from enum import Enum

"""Модуль с константами"""
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FPS = 120
TILE_SIZE = 64

FONT_NAME = './addons/monospace.ttf'
WHITE = (255, 255, 255)
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

# Player values
TIME_BETWEEN_INTERACT = 0.5
PLAYER_HITBOX_SIZE = (30, 30)
LEVELS_PROPERTIES = {
    1: {'max_health': 100, 'defence': 30, 'max_damage': 20, 'heal': 25},
    2: {'max_health': 120, 'defence': 50, 'max_damage': 30, 'heal': 30}
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
        "new_phase_enemies": []
    }
pig = {
        "image_path": "./sprites/enemies/pig/pig_fighting.png",
        "max_health": 100,
        "max_damage": 10,
        "defence": 20,
        "heal": 10,
        "new_phase_enemies": []
    }
keanu = {
        "image_path": "./sprites/enemies/tumbleweed/keanu.png",
        "max_health": 50,
        "max_damage": 15,
        "defence": 30,
        "heal": 15,
        "new_phase_enemies": []
    }
tumbleweed = {
        "image_path": "./sprites/enemies/tumbleweed/tumbleweed.png",
        "max_health": 30,
        "max_damage": 5,
        "defence": 10,
        "heal": 10,
        "new_phase_enemies": [keanu]
    }
varan = {
        "image_path": "./sprites/enemies/varan/varan_fighting.png",
        "max_health": 50,
        "max_damage": 15,
        "defence": 15,
        "heal": 15,
        "new_phase_enemies": []
    }

BATTLE_ENEMIES = {
    "mummy": mummy,
    "pig": pig,
    "keanu": keanu,
    "tumbleweed": tumbleweed,
    "varan": varan
}

DEFAULT_EFFECT_ANIM_SPEED = 0.2
