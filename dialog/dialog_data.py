import pygame
DIALOG_ICONS = {
    "???": {"idle": pygame.surface.Surface((10, 10))},
    "None": {"idle": pygame.surface.Surface((10, 10))},
    "Лидер": {
        "idle": pygame.image.load("./sprites/dialog_icons/caravan_leader/carvan-leader-idle.png"),
        "angry": pygame.image.load("./sprites/dialog_icons/caravan_leader/carvan-leader-angry.png"),
        "laughter": pygame.image.load("./sprites/dialog_icons/caravan_leader/carvan-leader-laughter.png"),
    },
    "Ната": {
        "idle": pygame.image.load("./sprites/dialog_icons/main_character/main_character_idle.png"),
        "dissatisfied": pygame.image.load("./sprites/dialog_icons/main_character/main_character_dissatisfied.png"),
        "frustrasion": pygame.image.load("./sprites/dialog_icons/main_character/main_character_frustration.png"),
        "laughter": pygame.image.load("./sprites/dialog_icons/main_character/main_character_laughter.png"),
    },
    "ghost": {
        "idle": pygame.image.load("./sprites/dialog_icons/ghost/ghost_idle.png"),
        "booo": pygame.image.load("./sprites/dialog_icons/ghost/ghost_booo.png"),
        "wtf": pygame.image.load("./sprites/dialog_icons/ghost/ghost_wtf.png"),
        "laughing": pygame.image.load("./sprites/dialog_icons/ghost/ghost_laughing.png"),
        "surprised": pygame.image.load("./sprites/dialog_icons/ghost/ghost_surprised.png"),
    },
    "keeper": {
        "happy": pygame.image.load("./sprites/dialog_icons/keeper/keeper_happy.png"),
        "idle": pygame.image.load("./sprites/dialog_icons/keeper/keeper_idle.png"),
        "sad": pygame.image.load("./sprites/dialog_icons/keeper/keeper_sad.png"),
    },
    "fairy": {
        "happy": pygame.image.load("./sprites/dialog_icons/fairy/fairy_happy.png"),
        "idle": pygame.image.load("./sprites/dialog_icons/fairy/fairy_idle.png"),
        "angry": pygame.image.load("./sprites/dialog_icons/fairy/fairy_angry.png"),
    },
}
