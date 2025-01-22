# Определяет класс врага, его движение по карте, здоровье и получение урона.

import pygame
from pygame.math import Vector2
# from main import TowerDefenseGame


class Enemy(pygame.sprite.Sprite):
    """ Определяет класс врага, его движение по карте, здоровье и получение урона. """

    def __init__(self, path, speed=2, health=10, image_path=None, game=None, reward=50):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.game = game
        self.path = path
        self.path_index = 0
        self.speed = speed
        self.health = health
        self.reward = reward
        self.position = Vector2(path[0])
        self.rect.center = self.position
        # проиграть музыку появления врага
        self.game.enemy_hit_sound.play()

    def take_damage(self, amount):
        # проиграть музыку повреждения врага
        self.game.enemy_hit_sound.play()

        self.health -= amount
        if self.health <= 0:
            # Получить награду за уничтожение врага
            self.game.settings.starting_money += self.reward
            self.game.last_event_text = f'The enemy has been destroyed + ${self.reward}'
            print(self.game.last_event_text)
            self.kill()

    def update(self):
        if self.path_index < len(self.path) - 1:
            start_point = Vector2(self.path[self.path_index])
            end_point = Vector2(self.path[self.path_index + 1])
            direction = (end_point - start_point).normalize()

            self.position += direction * self.speed
            self.rect.center = self.position

            if self.position.distance_to(end_point) < self.speed:
                self.path_index += 1

            if self.path_index >= len(self.path) - 1:
                self.game.game_over()
                self.kill()
