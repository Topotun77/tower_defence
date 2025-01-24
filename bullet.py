# Класс пули, управляет движением пули, проверкой попаданий во врагов и нанесением урона.

import pygame
from pygame.math import Vector2


class Bullet(pygame.sprite.Sprite):
    """ Класс пули, управляет движением пули, проверкой попаданий во врагов и нанесением урона. """
    def __init__(self, start_pos, target_pos, damage, game, image):
        super().__init__()
        self.game = game
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.position = Vector2(start_pos)
        self.target = Vector2(target_pos)
        self.speed = 5
        self.damage = damage
        self.velocity = self.calculate_velocity()

        # Проиграть звук пули
        self.game.shoot_sound.play()

    def calculate_velocity(self):
        direction = (self.target - self.position).normalize()
        velocity = direction * self.speed
        return velocity

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position
        if self.position.distance_to(self.target) < 10 or not self.game.is_position_inside(self.position):
            self.kill()

    def is_position_inside(self, pos):
        return 0 <= pos.x <= self.game.settings.screen_width and 0 <= pos.y <= self.game.settings.screen_height
