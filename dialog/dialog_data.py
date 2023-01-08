import pygame
DIALOG_ICONS = {
    "???": {"idle": pygame.surface.Surface((10, 10))},
    "None": {"idle": pygame.surface.Surface((10, 10))},
    "Аюр": {
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
}
