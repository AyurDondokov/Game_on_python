import random

import pygame.sprite
import game_object
import player
from timer import Timer
from properties import *


class BattleObject(pygame.sprite.Sprite):
    def __init__(self, position, battle, image_path, max_health, max_damage, defence):
        super().__init__(battle)

        # General settings
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect.center = self.image.get_rect(center=position)
        self.pos = pygame.math.Vector2(self.rect.center)

        # Timers
        self._timers = {
            "shake": Timer(BATTLE_SHAKE_TIME)
        }

        # Battle prams
        self.max_health = max_health
        self.health = max_health
        self.max_damage = max_damage
        self.defence = defence
        self.is_defencing = False

        self.start_pos = self.pos

    def _shake(self, intensity, speed, dt):
        x_direction = 1
        if self.pos.x >= self.start_pos + intensity:
            x_direction = -1
        elif self.pos.x <= self.start_pos - intensity:
            x_direction = 1
        self.pos.x += x_direction * speed * dt
        self.rect.centerx = round(self.pos.x)

    def take_damage(self, damage):
        if not self.is_defencing or not random.randint(0, 100) < self.defence:
            if self.health - damage > 0:
                self.health -= damage
                self._timers['shake'].activate()
            else:
                self.health = 0
                self.die()

    def die(self):
        self._timers['shake'].activate()
        pass

    def update(self, dt):
        if self._timers['shake'].active:
            self._shake(BATTLE_SHAKE_INTENSITY, BATTLE_SHAKE_SPEED, dt)


class BattlePlayer(BattleObject):
    def __init__(self, battle):
        super().__init__(
            position=BATTLE_PLAYER_POS,
            battle=battle,
            image_path=DEFAULT_PLAYER_BATTLE_SPRITE,
            max_health=LEVELS_PROPERTIES[1]['max_health'],
            max_damage=LEVELS_PROPERTIES[1]['max_damage'],
            defence=LEVELS_PROPERTIES[1]['defence']
        )


class Battle(pygame.sprite.Group):
    def __init__(self, player, enemies, bg_image_path):
        super().__init__()

        self.is_battle_start = False
        self.is_defeated_battle = False

        self.display_surf = pygame.display.get_surface()

        self.player = player
        self.enemies = enemies

        self.bg_image = pygame.image.load(bg_image_path)
        self.bg_rect = self.bg_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def start_battle(self):
        if self.is_defeated_battle:
            self.is_battle_start = True

    def end_battle(self):
        self.is_battle_start = False

    def custom_draw(self):
        self.display_surf.blit(self.bg_image, self.bg_rect)
        enemies_offset_x = SCREEN_HEIGHT / (len(self.enemies)+2)

        for enemy_index, enemy in enumerate(self.enemies):
            enemy_offset = pygame.math.Vector2()

            enemy_offset.x = 0
            enemy_offset.y = enemies_offset_x * (enemy_index+1)

            self.display_surf.blit(enemy.image, enemy.rect + enemy_offset)

        self.display_surf.blit(self.player.image, self.player.rect)

    def update(self, dt):
        if self.is_battle_start:
            self.custom_draw()
            self.player.update(dt)
            for enemy in self.enemies:
                enemy.update(dt)


STANDARD_BATTLE = Battle(bg_image_path='./images/menu/test_game.png',
                         player=BattlePlayer())