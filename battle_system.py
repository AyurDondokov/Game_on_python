import random

import pygame.sprite

import player as pl
import UI as ui
from timer import Timer
from properties import *


class BattleObject(pygame.sprite.Sprite):
    def __init__(self, position, battle_group, image_path,
                 max_health, max_damage, defence, health, heal, on_die_func, args,
                 attack_image_path: str = ''):
        super().__init__(battle_group)

        # General settings
        self.stay_image = pygame.image.load(image_path)
        if attack_image_path != '':
            self.attack_image = pygame.image.load(attack_image_path)
        else:
            self.attack_image = None
        self.image = self.stay_image
        self.rect = self.image.get_rect(center=position)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.args = args

        # Timers
        self._timers = {
            "shake": Timer(BATTLE_SHAKE_TIME),
            "attack": Timer(BATTLE_ATTACK_TIME)
        }

        # Battle prams
        self.is_defeated = False

        self.max_health = max_health
        self.health = health
        self.max_damage = max_damage
        self.defence = defence
        self.heal = heal

        self.is_defencing = False
        self.on_die_func = on_die_func
        self.health_bar = ui.ProgressBar(self.rect.topleft)
        self.start_pos = self.pos.copy()
        self.x_direction = 1

    def _shake(self, intensity, speed, dt):
        if self.pos.x >= self.start_pos.x + intensity:
            self.x_direction = -1
        elif self.pos.x <= self.start_pos.x - intensity:
            self.x_direction = 1
        self.pos.x += self.x_direction * speed * dt
        self.rect.centerx = round(self.pos.x)

    def attack(self):
        self._timers["shake"].activate()
        self._timers["attack"].activate()

    def check_defence(self):
        return not self.is_defencing or not random.randint(0, 100) < self.defence

    def healing(self):
        if self.health + self.heal <= self.max_health:
            self.health += self.heal
        else:
            self.health = self.max_health
        self.health_bar.value = self.health / self.max_health
        self.is_defencing = False

    def take_damage(self, damage):
        if self.check_defence():
            if self.health - damage > 0:
                self.health -= damage
                self._timers['shake'].activate()
            else:
                self.health = 0.0
                self.die()
            self.health_bar.value = self.health / self.max_health
            self.is_defencing = False

    def die(self):
        self._timers['shake'].activate()
        self.is_defeated = True
        self.on_die_func(self.args)

    def update(self, dt):
        if self._timers['shake'].active:
            self._timers['shake'].update()
            self._shake(BATTLE_SHAKE_INTENSITY, BATTLE_SHAKE_SPEED, dt)
        if self.attack_image:
            if self._timers['attack'].active:
                self._timers['attack'].update()
                self.image = self.attack_image
            else:
                self.image = self.stay_image

    def make_move(self):
        pass

    def set_pos(self, new_pos):
        self.pos.x = new_pos[0]
        self.pos.y = new_pos[1]
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)
        self.health_bar = ui.ProgressBar(self.rect.topleft)
        self.start_pos = self.pos.copy()


class BattleEnemy(BattleObject):
    def __init__(self, position, data, battle_group, on_die_func, args, battle_player,
                 new_phase_enemies_data: tuple = ()):
        super().__init__(position=position,
                         battle_group=battle_group,
                         image_path=data["image_path"],
                         max_health=data["max_health"],
                         max_damage=data["max_damage"],
                         defence=data["defence"],
                         health=data["max_health"],
                         heal=data["heal"],
                         on_die_func=on_die_func,
                         args=args)
        self.battle_player = battle_player
        self.new_phase_enemies_data = new_phase_enemies_data
        print(self.new_phase_enemies_data)

    def make_move(self):
        if self.health > self.max_health/2:
            self.battle_player.take_damage(self.max_damage)
        elif self.health > self.max_health/4:
            self.is_defencing = True
        else:
            self.healing()


class BattlePlayer(BattleObject):
    def __init__(self, battle_group, game_player: pl.Player, on_die_func,
                 attack_image_path: str = "sprites/main_character/fighting/fighting_hit.png"):
        super().__init__(
            position=BATTLE_PLAYER_POS,
            battle_group=battle_group,
            image_path=DEFAULT_PLAYER_BATTLE_SPRITE,
            max_health=LEVELS_PROPERTIES[game_player.level]['max_health'],
            max_damage=LEVELS_PROPERTIES[game_player.level]['max_damage'],
            defence=LEVELS_PROPERTIES[game_player.level]['defence'],
            health=game_player.health,
            heal=LEVELS_PROPERTIES[game_player.level]['heal'],
            on_die_func=on_die_func,
            args=False,
            attack_image_path=attack_image_path
        )


class BattleMenu:
    def __init__(self, buttons,
                 action_bar_path: str = "./sprites/fight/UI/action_bar.png"):
        self.action_bar = pygame.sprite.Sprite()
        self.action_bar.image = pygame.image.load(action_bar_path)
        self.action_bar.rect = self.action_bar.image.get_rect(center=BATTLE_ACTIONS_BAR_POS)
        self.target_index = 0

        self.buttons = buttons
        self.buttons_count = len(self.buttons)
        self.buttons[self.target_index].is_targeted = True

        self.display_surf = pygame.display.get_surface()
        self.__event_list = []

    def change_target_on_n(self, n):
        self.buttons[self.target_index].is_targeted = False
        self.target_index = n
        self.buttons[self.target_index].is_targeted = True

    def draw_menu(self):
        self.display_surf.blit(self.action_bar.image, self.action_bar.rect)
        for button in self.buttons:
            button.draw()

    def set_events_list(self, event_list):
        self.__event_list = event_list
        for button in self.buttons:
            button.set_events_list(event_list)

    def input(self):
        for event in self.__event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if self.target_index - 1 >= 0:
                        self.change_target_on_n(self.target_index - 1)
                    else:
                        self.change_target_on_n(self.buttons_count - 1)
                elif event.key == pygame.K_d:
                    if self.target_index + 1 < self.buttons_count:
                        self.change_target_on_n(self.target_index + 1)
                    else:
                        self.change_target_on_n(0)

    def update(self):
        for button in self.buttons:
            button.update()


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
    def __init__(self, game_player, enemies_data,
                 bg_image_path: str = "./sprites/fight/fight_background/desert.png",
                 select_sprite_path: str = "./sprites/fight/UI/select_sprite.png"):
        self.is_battle = False
        self.is_finished_battle = False
        self.display_surf = pygame.display.get_surface()

        self.__event_list = []
        self.timers = {"make_move": Timer(BATTLE_MOVE_TIME)}

        self.participants = []
        self.turn = 0

        self.selected_enemy = 0
        self.state_of_battle = BATTLE_STATES.choose_move

        self.bg_image = pygame.image.load(bg_image_path)
        self.bg_rect = self.bg_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.battle_menu = None
        self.battle_group = BattleGroup()
        self.set_battle_menu()
        self.battle_scale = ui.PowerScale()
        self.battle_player = BattlePlayer(battle_group=self.battle_group,
                                          game_player=game_player,
                                          on_die_func=self.end,
                                          attack_image_path="sprites/main_character/fighting/fighting_hit.png")

        self.participants.append(self.battle_player)

        self.enemies = []

        for index, enemy_data in enumerate(enemies_data):
            self.add_enemy(enemy_data, index)

        self.set_enemies_positions()

        self.select_sprite = pygame.image.load(select_sprite_path)
        self.select_rect = self.select_sprite.get_rect(center=self.enemies[0].pos)

    def set_battle_menu(self):
        attack_btn = ui.Button(func=self.make_move, args=BATTLE_MOVES.attack, pos=BATTLE_BUTTONS_POS[0],
                               text="attack")
        heal_btn = ui.Button(func=self.make_move, args=BATTLE_MOVES.heal, pos=BATTLE_BUTTONS_POS[1],
                             text="heal")
        block_btn = ui.Button(func=self.make_move, args=BATTLE_MOVES.block, pos=BATTLE_BUTTONS_POS[2],
                              text="block")
        run_btn = ui.Button(func=self.make_move, args=BATTLE_MOVES.run, pos=BATTLE_BUTTONS_POS[3],
                            text="run")
        self.battle_menu = BattleMenu((attack_btn, heal_btn, block_btn, run_btn))

    def remove_enemy(self, index):
        for enemy_data in self.enemies[index].new_phase_enemies_data:
            self.add_enemy(enemy_data, len(self.enemies))
        if len(self.enemies) != 1:
            self.selected_enemy = 0
            self.enemies.pop(index)
            self.set_enemies_positions()
        else:
            self.end(True)

    def add_enemy(self, new_enemy_data, enemy_index):
        self.enemies.append(BattleEnemy(
            position=(0, 0),
            battle_group=self.battle_group,
            data=new_enemy_data,
            on_die_func=self.remove_enemy,
            args=enemy_index,
            battle_player=self.battle_player,
            new_phase_enemies_data=new_enemy_data["new_phase_enemies"]
        ))

        self.participants.append(self.enemies[enemy_index])
        self.battle_group.add_progress_bar(self.enemies[enemy_index].health_bar)

    def set_enemies_positions(self):
        for index, enemy in enumerate(self.enemies):
            pos = (BATTLE_ENEMY_POS_X, (index + 1) * (SCREEN_HEIGHT / (len(self.enemies) + 1)))
            enemy.set_pos(pos)
            enemy.args = index

    def set_events_list(self, event_list):
        self.__event_list = event_list
        self.battle_menu.set_events_list(event_list)

    def make_move(self, move):
        if move == BATTLE_MOVES.attack:
            self.state_of_battle = BATTLE_STATES.selecting_enemy
        elif move == BATTLE_MOVES.heal:
            self.battle_player.healing()
            self.state_of_battle = BATTLE_STATES.waiting
        elif move == BATTLE_MOVES.block:
            self.battle_player.is_defencing = True
            self.state_of_battle = BATTLE_STATES.waiting
        elif move == BATTLE_MOVES.run:
            if random.randint(0, 100) < BATTLE_RUN_CHANCE:
                self.end(False)
            else:
                self.state_of_battle = BATTLE_STATES.waiting

    def selecting_enemy(self):
        for event in self.__event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if self.selected_enemy + 1 < len(self.enemies):
                        self.selected_enemy += 1
                    else:
                        self.selected_enemy = 0
                elif event.key == pygame.K_w:
                    if self.selected_enemy - 1 >= 0:
                        self.selected_enemy -= 1
                    else:
                        self.selected_enemy = len(self.enemies) - 1
                elif event.key == pygame.K_e:
                    self.state_of_battle = BATTLE_STATES.stash_damage
                    self.timers["make_move"].activate()

    def stashing_damage(self):
        for event in self.__event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.enemies[self.selected_enemy].take_damage(
                        self.battle_player.max_damage*self.battle_scale.get_value())
                    self.state_of_battle = BATTLE_STATES.waiting
                    self.battle_player.attack()

    def update(self, dt):
        self.battle_player.update(dt)
        self.timers["make_move"].update()
        for enemy in self.enemies:
            enemy.update(dt)

        if self.state_of_battle == BATTLE_STATES.selecting_enemy:
            self.selecting_enemy()
        elif self.state_of_battle == BATTLE_STATES.waiting:
            if self.timers["make_move"].active:
                pass
            else:
                if self.turn < len(self.enemies):
                    self.timers["make_move"].activate()
                    self.enemies[self.turn].make_move()
                    self.turn += 1
                else:
                    self.state_of_battle = BATTLE_STATES.choose_move
                    self.turn = 0
        elif self.state_of_battle == BATTLE_STATES.choose_move:
            self.battle_menu.input()
            self.battle_menu.update()
        elif self.state_of_battle == BATTLE_STATES.stash_damage:
            self.battle_scale.update(dt)
            self.stashing_damage()

    def draw(self):
        self.display_surf.blit(self.bg_image, self.bg_rect)
        if self.state_of_battle == BATTLE_STATES.selecting_enemy:
            self.select_rect.center = self.enemies[self.selected_enemy].rect.center
            self.display_surf.blit(self.select_sprite, self.select_rect)
        self.battle_group.custom_draw()
        self.battle_menu.draw_menu()
        if self.state_of_battle == BATTLE_STATES.stash_damage:
            self.battle_scale.draw()

    def start(self):
        if not self.is_battle and not self.is_finished_battle:
            self.is_battle = True
            # print(f"Начался бой с \n {self.enemies}")

    def end(self, is_finished):
        if self.is_battle:
            self.is_finished_battle = is_finished
            self.is_battle = False
            # print(f"Бой закончен\n Победа: {self.is_finished_battle}")

