import os
import random

import pygame.sprite

import player as pl
import UI as ui
import effects as effects
from timer import Timer
from properties import *


# Абстрактный класс для участников боя
class BattleObject(pygame.sprite.Sprite):
    def __init__(self, position, battle_group, effect_group, image_path, max_health, max_damage, defence, health, heal,
                 attack_image_path: str = ''):
        super().__init__(battle_group)

        # Основные настройки.
        self.s_punch = None
        self._stay_image = pygame.image.load(image_path)
        if attack_image_path != '':
            self._attack_image = pygame.image.load(attack_image_path)
        else:
            self._attack_image = None
        self.image = self._stay_image
        self.rect = self.image.get_rect(center=position)
        self.pos = pygame.math.Vector2(self.rect.center)

        # Таймеры
        self._timers = {
            "shake": Timer(BATTLE_SHAKE_TIME),
            "attack": Timer(BATTLE_ATTACK_TIME)
        }

        # Параметры участника боя
        self._is_defeated = False
        self._max_health = max_health
        self._health = health
        self._max_damage = max_damage
        self._defence = defence
        self._heal = heal
        self._is_defencing = False

        self._health_bar = ui.ProgressBar(self.rect.topleft)

        self._start_pos = self.pos.copy()
        self._x_direction = 1

        self.sounds_punch = os.listdir('music_and_sound/sound/punch')
        self.sound_heal = pygame.mixer.Sound('music_and_sound/sound/heal/healing_spell_mend_02_16_441.mp3')
        self.sound_death = pygame.mixer.Sound('music_and_sound/sound/game/death.mp3')
        self.sound_win = pygame.mixer.Sound('music_and_sound/sound/game/win.mp3')

        self._wound_effect = effects.Effect(position, "./sprites/fight/fight_effect/wound", effect_group)
        self._heal_effect = effects.Effect(position, "./sprites/fight/fight_effect/heal", effect_group)

    def _shake(self, intensity: float, speed: float, dt):
        if self.pos.x >= self._start_pos.x + intensity:
            self._x_direction = -1
        elif self.pos.x <= self._start_pos.x - intensity:
            self._x_direction = 1
        self.pos.x += self._x_direction * speed * dt
        self.rect.centerx = round(self.pos.x)

    def attack(self):
        self._timers["shake"].activate()
        self._timers["attack"].activate()

    def _check_defence(self):
        return not self._is_defencing or not random.randint(0, 100) < self._defence

    def healing(self):
        self.sound_heal.play()
        if self._health + self._heal <= self._max_health:
            self._health += self._heal
        else:
            self._health = self._max_health
        self._health_bar.value = self._health / self._max_health
        self._heal_effect.start()
        self._is_defencing = False

    def take_damage(self, damage):
        if self._check_defence():
            if self._health - damage > 0:
                self._health -= damage
                self._timers['shake'].activate()
                self.s_punch = pygame.mixer.Sound("music_and_sound/sound/punch/" + random.choice(self.sounds_punch))
                self.s_punch.play()
            else:
                self.sound_death.play()
                self._health = 0.0
                self._die()
            self._wound_effect.start()
            self._health_bar.value = self._health / self._max_health
            self._is_defencing = False

    def _die(self):
        self._timers['shake'].activate()
        self._is_defeated = True
        self._wound_effect.kill()
        self._heal_effect.kill()

    def update(self, dt):
        self._wound_effect.update(dt)
        self._heal_effect.update(dt)
        if self._timers['shake'].active:
            self._timers['shake'].update()
            self._shake(BATTLE_SHAKE_INTENSITY, BATTLE_SHAKE_SPEED, dt)
        if self._attack_image:
            if self._timers['attack'].active:
                self._timers['attack'].update()
                self.image = self._attack_image
            else:
                self.image = self._stay_image

    def set_pos(self, new_pos):
        self.pos.x = new_pos[0]
        self.pos.y = new_pos[1]
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)
        self._health_bar = ui.ProgressBar(self.rect.topleft)
        self._start_pos = self.pos.copy()
        self._wound_effect.rect = self.rect.center
        self._heal_effect.rect = self.rect.center

    @property
    def max_damage(self):
        return self._max_damage

    @property
    def health(self):
        return self._health

    @property
    def health_bar(self):
        return self._health_bar

    @property
    def is_defeated(self):
        return self._is_defeated


class BattleEnemy(BattleObject):
    def __init__(self, position, data, battle_group, effect_group, battle_player,
                 new_phase_enemies_data: tuple = ()):
        super().__init__(position=position,
                         battle_group=battle_group,
                         effect_group=effect_group,
                         image_path=data["image_path"],
                         max_health=data["max_health"],
                         max_damage=data["max_damage"],
                         defence=data["defence"],
                         health=data["max_health"],
                         heal=data["heal"])
        self._battle_player = battle_player
        self._new_phase_enemies_data = new_phase_enemies_data
        self._exp_from_me = data['exp']

    def make_move(self):
        if self._health > self._max_health / 2:
            self._battle_player.take_damage(self._max_damage)
        elif self._health > self._max_health / 4:
            self._is_defencing = True
        else:
            self.healing()

    @property
    def new_phase_enemies_data(self):
        return self._new_phase_enemies_data

    @property
    def exp_from_me(self):
        return self._exp_from_me


class BattlePlayer(BattleObject):
    def __init__(self, battle_group, effect_group, game_player: pl.Player,
                 attack_image_path: str = "sprites/main_character/fighting/fighting_hit.png"):
        super().__init__(
            position=BATTLE_PLAYER_POS,
            battle_group=battle_group,
            effect_group=effect_group,
            image_path=DEFAULT_PLAYER_BATTLE_SPRITE,
            max_health=LEVELS_PROPERTIES[game_player.level]['max_health'],
            max_damage=LEVELS_PROPERTIES[game_player.level]['max_damage'],
            defence=LEVELS_PROPERTIES[game_player.level]['defence'],
            health=game_player.health,
            heal=LEVELS_PROPERTIES[game_player.level]['heal'],
            attack_image_path=attack_image_path
        )


class BattleGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.progress_bars = []

    def add_progress_bar(self, prog_bar):
        self.progress_bars.append(prog_bar)

    def custom_draw(self):
        for sprite in self.sprites():
            if (type(sprite) == BattleEnemy or type(sprite) == BattlePlayer) and not sprite.is_defeated:
                self.display_surf.blit(sprite.image, sprite.rect)
                pygame.draw.rect(self.display_surf, sprite.health_bar.color[0], sprite.health_bar.rect[0])
                pygame.draw.rect(self.display_surf, sprite.health_bar.color[1], sprite.health_bar.rect[1])


class Battle:
    def __init__(self, game_player, enemies_data, level_music_path,
                 battle_music_path: str = "music_and_sound/music/fighting/Frau Holle - Sand Cave.mp3",
                 bg_image_path: str = "./sprites/fight/fight_background/desert.png",
                 select_sprite_path: str = "./sprites/fight/UI/select_sprite.png"):
        self._is_battle = False
        self._is_finished_battle = False
        self._display_surf = pygame.display.get_surface()
        self._game_player = game_player

        self.__event_list = []
        self._timers = {"make_move": Timer(BATTLE_MOVE_TIME)}

        self._participants = []
        self._turn = 0

        self._selected_enemy = 0
        self._state_of_battle = BATTLE_STATES.choose_move

        self._bg_image = pygame.image.load(bg_image_path)
        self._bg_rect = self._bg_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self._battle_menu = None
        self._battle_group = BattleGroup()
        self._effect_group = effects.EffectGroup()
        self.set_battle_menu()
        self._battle_scale = ui.PowerScale()
        self._battle_player = BattlePlayer(battle_group=self._battle_group,
                                           effect_group=self._effect_group,
                                           game_player=game_player,
                                           attack_image_path="sprites/main_character/fighting/fighting_hit.png")

        self._participants.append(self._battle_player)

        self._enemies = []

        for index, enemy_data in enumerate(enemies_data):
            self._add_enemy(enemy_data, index)

        self._set_enemies_positions()

        self._select_sprite = pygame.image.load(select_sprite_path)
        self._select_rect = self._select_sprite.get_rect(center=self._enemies[self._selected_enemy].pos)

        self.level_music_path = level_music_path
        self.battle_music_path = battle_music_path

    def set_battle_menu(self):
        attack_btn = ui.Button(func=self._make_move, args=BATTLE_MOVES.attack, pos=BATTLE_BUTTONS_POS[0],
                               text="attack")
        heal_btn = ui.Button(func=self._make_move, args=BATTLE_MOVES.heal, pos=BATTLE_BUTTONS_POS[1],
                             text="heal")
        block_btn = ui.Button(func=self._make_move, args=BATTLE_MOVES.block, pos=BATTLE_BUTTONS_POS[2],
                              text="block")
        run_btn = ui.Button(func=self._make_move, args=BATTLE_MOVES.run, pos=BATTLE_BUTTONS_POS[3],
                            text="run")
        self._battle_menu = ui.Menu((attack_btn, heal_btn, block_btn, run_btn))

    def _remove_enemy(self, index):
        if self._game_player.take_exp(self._enemies[index].exp_from_me):
            self._battle_player.healing()
        for enemy_data in self._enemies[index].new_phase_enemies_data:
            self._add_enemy(enemy_data, len(self._enemies))
        if len(self._enemies) != 1:
            self._selected_enemy = 0
            self._enemies.pop(index)
            self._set_enemies_positions()
        else:
            self._end(True)

    def _add_enemy(self, new_enemy_data, enemy_index):
        self._enemies.append(BattleEnemy(
            position=(0, 0),
            battle_group=self._battle_group,
            effect_group=self._effect_group,
            data=new_enemy_data,
            battle_player=self._battle_player,
            new_phase_enemies_data=new_enemy_data["new_phase_enemies"]
        ))

        self._participants.append(self._enemies[enemy_index])
        self._battle_group.add_progress_bar(self._enemies[enemy_index].health_bar)

    def _set_enemies_positions(self):
        for index, enemy in enumerate(self._enemies):
            pos = (BATTLE_ENEMY_POS_X, (index + 1) * (SCREEN_HEIGHT / (len(self._enemies) + 1)))
            enemy.set_pos(pos)

    def _make_move(self, move):
        if move == BATTLE_MOVES.attack:
            self._timers["make_move"].activate()
            self._state_of_battle = BATTLE_STATES.selecting_enemy
        elif move == BATTLE_MOVES.heal:
            self._battle_player.healing()
            self._timers["make_move"].activate()
            self._state_of_battle = BATTLE_STATES.waiting
        elif move == BATTLE_MOVES.block:
            self._battle_player.is_defencing = True
            self._timers["make_move"].activate()
            self._state_of_battle = BATTLE_STATES.waiting
        elif move == BATTLE_MOVES.run:
            if random.randint(0, 100) < BATTLE_RUN_CHANCE:
                self._end(False)
            else:
                self._timers["make_move"].activate()
                self._state_of_battle = BATTLE_STATES.waiting

    def _selecting_enemy(self):
        for event in self.__event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if self._selected_enemy + 1 < len(self._enemies):
                        self._selected_enemy += 1
                    else:
                        self._selected_enemy = 0
                elif event.key == pygame.K_w:
                    if self._selected_enemy - 1 >= 0:
                        self._selected_enemy -= 1
                    else:
                        self._selected_enemy = len(self._enemies) - 1
                elif event.key == pygame.K_e:
                    self._state_of_battle = BATTLE_STATES.stash_damage

    def _waiting(self):
        if self._timers["make_move"].active:
            pass
        else:
            if self._turn < len(self._enemies):
                self._timers["make_move"].activate()
                self._enemies[self._turn].make_move()
                self._turn += 1
            else:
                self._state_of_battle = BATTLE_STATES.choose_move
                self._turn = 0

    def _stashing_damage(self):
        for event in self.__event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self._enemies[self._selected_enemy].take_damage(
                        self._battle_player.max_damage * self._battle_scale.get_value())
                    self._timers["make_move"].activate()
                    self._state_of_battle = BATTLE_STATES.waiting
                    self._battle_player.attack()

    def _update_states_of_battle(self, dt):
        if self._state_of_battle == BATTLE_STATES.selecting_enemy:
            self._selecting_enemy()
        elif self._state_of_battle == BATTLE_STATES.waiting:
            self._waiting()
        elif self._state_of_battle == BATTLE_STATES.choose_move:
            self._battle_menu.input()
            self._battle_menu.update()
        elif self._state_of_battle == BATTLE_STATES.stash_damage:
            self._battle_scale.update(dt)
            self._stashing_damage()

    def _end(self, is_finished):
        if self._is_battle:
            self._is_finished_battle = is_finished
            self._game_player.set_health(self._battle_player.health)
            self._is_battle = False
            pygame.mixer.music.load(self.level_music_path)
            pygame.mixer.music.play(-1)

    def set_events_list(self, event_list):
        self.__event_list = event_list
        self._battle_menu.set_events_list(event_list)

    def update(self, dt):
        # Игрок
        if self._battle_player.is_defeated:
            self._end(False)
        self._battle_player.update(dt)

        # Таймеры
        self._timers["make_move"].update()

        # Враги
        for index, enemy in enumerate(self._enemies):
            if enemy.is_defeated:
                self._remove_enemy(index)
            enemy.update(dt)

        self._update_states_of_battle(dt)

    def draw(self):
        self._display_surf.blit(self._bg_image, self._bg_rect)
        if self._state_of_battle == BATTLE_STATES.selecting_enemy:
            self._select_rect.centerx = self._enemies[self._selected_enemy].rect.centerx
            self._select_rect.centery = self._enemies[self._selected_enemy].rect.bottom
            self._display_surf.blit(self._select_sprite, self._select_rect)
        self._battle_group.custom_draw()
        self._battle_menu.draw_menu()
        self._effect_group.custom_draw()
        if self._state_of_battle == BATTLE_STATES.stash_damage:
            self._battle_scale.draw()

    def start(self):
        if not self._is_battle and not self._is_finished_battle:
            self._is_battle = True
            pygame.mixer.music.load(self.battle_music_path)
            pygame.mixer.music.play(-1)

    @property
    def is_battle(self):
        return self._is_battle

    @property
    def effect_group(self):
        return self._effect_group


class BattleManager:
    def __init__(self, battles_data, player, level_music_path):
        self._enemies = None
        self._battles = []
        self._player = player
        for keys in battles_data.keys():
            self._add_battle(battles_data[keys], level_music_path)
        self._current_battle_index = 0
        self._is_battle = False

    def _add_battle(self, battle_data: dict, level_music_path):
        enemies = []
        for enemy_name in battle_data["enemies"]:
            enemies.append(BATTLE_ENEMIES[enemy_name])
        self._enemies = enemies
        self._battles.append(Battle(self._player, enemies, level_music_path,
                                    battle_music_path=battle_data["music_path"]))

    def set_events_list(self, event_list):
        self._battles[self._current_battle_index].set_events_list(event_list)

    def update(self, dt):
        current_battle = self._battles[self._current_battle_index]
        if current_battle.is_battle:
            current_battle.update(dt)
            current_battle.draw()
        else:
            self._is_battle = False

    def start(self, index: int):
        self._current_battle_index = int(index)
        self._battles[self._current_battle_index].start()
        self._is_battle = self._battles[self._current_battle_index].is_battle

    @property
    def is_battle(self) -> bool:
        return self._is_battle
