# Содержит логику уровня, управление волнами врагов, их спавн,
# а также расстановку башен и обработку коллизий.

import pygame
from enemy import Enemy
from settings import tower_classes


class Level:
    """ Управляет уровнем игры, волнами врагов и расстановкой башен. """

    def __init__(self, game):
        """ Инициализирует уровень игры. """
        self.game = game
        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.waves = [
            [{'path': self.game.settings.enemy_path, 'speed': 1, 'health': 100, 'image_path': 'assets/enemies/basic_enemy.png'}] * 5,
            [{'path': self.game.settings.enemy_path, 'speed': 1.5, 'health': 150, 'image_path': 'assets/enemies/fast_enemy.png'}] * 7,
            [{'path': self.game.settings.enemy_path, 'speed': 0.75, 'health': 200, 'image_path': 'assets/enemies/strong_enemy.png'}] * 4,
        ]
        self.current_wave = 0
        self.spawned_enemies = 0
        self.spawn_delay = 1000
        self.last_spawn_time = pygame.time.get_ticks()
        self.all_waves_complete = False
        self.start_next_wave()
        self.font = pygame.font.SysFont("Arial", 24)

    def start_next_wave(self):
        """ Запускает следующую волну врагов. """
        if self.current_wave < len(self.waves):
            self.spawned_enemies = 0
            self.spawn_next_enemy()

    def spawn_next_enemy(self):
        """ Генерирует следующего врага текущей волны. """
        if self.spawned_enemies < len(self.waves[self.current_wave]):
            enemy_info = self.waves[self.current_wave][self.spawned_enemies]
            new_enemy = Enemy(**enemy_info, game=self.game)
            self.enemies.add(new_enemy)
            self.spawned_enemies += 1

    def attempt_place_tower(self, mouse_pos, tower_type):
        """ Пытается разместить башню выбранного типа в позиции курсора. """
        if tower_type in tower_classes and self.game.settings.starting_money >= self.game.settings.tower_cost:
            grid_pos = self.game.grid.get_grid_position(mouse_pos)
            if self.game.grid.is_spot_available(grid_pos):
                self.game.settings.starting_money -= self.game.settings.tower_cost
                new_tower = tower_classes[tower_type](grid_pos, self.game)
                self.towers.add(new_tower)
                self.game.last_event_text = 'Tower placed.'
                print(self.game.last_event_text)
            else:
                self.game.last_event_text = 'Invalid position for tower.'
                print(self.game.last_event_text)
        else:
            self.game.last_event_text = 'Not enough money or unknown tower type.'
            print(self.game.last_event_text)

    def update(self):
        """ Обновляет состояние уровня, врагов, башен и пуль. """
        current_time = pygame.time.get_ticks()

        if self.current_wave < len(self.waves) and self.spawned_enemies < len(self.waves[self.current_wave]):
            if current_time - self.last_spawn_time > self.spawn_delay:
                enemy_info = self.waves[self.current_wave][self.spawned_enemies].copy()
                enemy_info['game'] = self.game
                new_enemy = Enemy(**enemy_info)
                self.enemies.add(new_enemy)
                self.spawned_enemies += 1
                self.last_spawn_time = current_time

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet in collisions:
            for enemy in collisions[bullet]:
                enemy.take_damage(bullet.damage)

        self.enemies.update()
        for tower in self.towers:
            tower.update(self.enemies, current_time, self.bullets)
        self.bullets.update()

        if len(self.enemies) == 0 and self.current_wave < len(self.waves) - 1:
            self.current_wave += 1
            self.start_next_wave()
        elif len(self.enemies) == 0 and self.current_wave == len(self.waves) - 1:
            self.all_waves_complete = True

    def draw_path(self, screen):
        """ Отображает путь врагов. """
        if self.game.show_grid:
            pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path, 5)
        if self.game.show_grid in [3, 4]:
            for pos in self.game.settings.tower_positions:
                pygame.draw.circle(screen, (128, 0, 0), pos, 10)

    def draw(self, screen):
        """ Отрисовывает уровень, включая врагов, башни и пули. """
        self.draw_path(screen)
        self.enemies.draw(screen)
        self.towers.draw(screen)
        self.bullets.draw(screen)
        mouse_pos = pygame.mouse.get_pos()
        for tower in self.towers:
            tower.draw(screen)
            if tower.is_hovered(mouse_pos):
                tower_stats_text = self.font.render(f"Damage: {tower.damage}, Range: {tower.tower_range}", True,
                                                    (255, 255, 255))
                screen.blit(tower_stats_text, (tower.rect.x, tower.rect.y - 20))
