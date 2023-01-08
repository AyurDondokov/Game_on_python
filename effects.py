import pygame as pygame

from properties import *
from support import *


class EffectGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()

    def custom_draw(self):
        for effect in self.sprites():
            if effect.is_animated:
                self.display_surf.blit(effect.image, effect.rect)


class Effect(pygame.sprite.Sprite):
    def __init__(self, pos, folder_with_anim_path, effect_group,
                 anim_speed: float = DEFAULT_EFFECT_ANIM_SPEED):
        super().__init__(effect_group)
        self._animation_frames = import_surfaces_from_folder(folder_with_anim_path)
        self._anim_speed = anim_speed

        self._current_frame_index = 0
        self._is_animation_run = False

        self.image = self._animation_frames[0]
        self.rect = self.image.get_rect(center=pos)

    def start(self):
        self._current_frame_index = 0
        self._is_animation_run = True

    def update(self, dt):
        self._current_frame_index += 1 / self._anim_speed * dt
        if self._current_frame_index >= len(self._animation_frames):
            self._current_frame_index = 0
            self._is_animation_run = False
        self.image = self._animation_frames[int(self._current_frame_index)]

    @property
    def is_animated(self):
        return self._is_animation_run
