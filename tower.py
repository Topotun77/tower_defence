# Базовый класс башни и его наследники для разных типов башен,
# содержит логику стрельбы, поиска цели и улучшения.

import pygame
from bullet import Bullet
import math


class Tower(pygame.sprite.Sprite):
    """
    Базовый класс для всех башен, его методы включают инициализацию, отрисовку,
    обновление, стрельбу, поворот к цели и поиск цели.
    """
    def __init__(self, position, game):
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.game = game

        self.image = None
        self.rect = None
        # Радиус действия башни
        self.tower_range = 0
        # Наносимый урон
        self.damage = 0
        # Скорострельность в мс
        self.rate_of_fire = 0
        # Время последнего выстрела
        self.last_shot_time = pygame.time.get_ticks()
        # Уровень башни
        self.level = 1
        self.original_image = self.image

        # Проиграть звук при создании башни
        self.game.put_sound.play()

    def upgrade_cost(self):
        """
        Стоимость улучшения башни. Зависит от уровня башни.
        :return: Стоимость апгрейда башни
        """
        return 100 * self.level

    def draw(self, screen):
        """
        Отражение информации о башне на экране
        :param screen: Экран для отрисовки
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            level_text = self.game.font.render(f"Level: {self.level}", True, (255, 255, 255))
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()  }", True, (255, 255, 255))

            # Позиция текста
            level_text_pos = (self.position.x, self.position.y + 20)
            upgrade_cost_pos = (self.position.x, self.position.y + 40)

            # Вывод текста
            screen.blit(level_text, level_text_pos)
            screen.blit(upgrade_cost_text, upgrade_cost_pos)

    def update(self, enemies, current_time, bullets_group):
        """
        Обновляет состояние башни: поиск цели, стрельба и создание пуль.
        :param enemies: Список врагов.
        :param current_time: Текущее время.
        :param bullets_group: Список пуль.
        """
        if current_time - self.last_shot_time > self.rate_of_fire:
            target = self.find_target(enemies)
            if target:
                self.rotate_towards_target(target)
                self.shoot(target, bullets_group)
                self.last_shot_time = current_time

    def is_hovered(self, mouse_pos):
        """ Проверка: курсор мыши над башней? """
        return self.rect.collidepoint(mouse_pos)

    def shoot(self, target, bullets_group):
        """
        Стрельба по цели.
        :param target: Цель
        :param bullets_group: Список пуль
        """
        pass

    def rotate_towards_target(self, target):
        """
        Поворачивает башню в направлении цели
        :param target: Цель
        """
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        # Вычисляем угол в радианах
        angle_rad = math.atan2(dy, dx)
        # Преобразуем радианы в градусы
        angle_deg = math.degrees(angle_rad)
        angle_deg = -angle_deg - 90
        self.image = pygame.transform.rotate(self.original_image, angle_deg)
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        """
        Поиск ближайшей цели
        :param enemies: Список врагов
        :return: Ближайший враг или None, если врагов нет в радиусе действия башни
        """
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.position.distance_to(enemy.position)
            if distance < min_distance and distance <= self.tower_range:
                nearest_enemy = enemy
                min_distance = distance
        return nearest_enemy

    def upgrade(self):
        """ Апгрейд башни """
        self.level += 1


class BasicTower(Tower):
    """ Базовая башня """
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/basic_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 150
        self.damage = 20
        self.rate_of_fire = 1000

    def shoot(self, target, bullets_group):
        """
        Стрельба по цели.
        :param target: Цель
        :param bullets_group: Список пуль
        """
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class SniperTower(Tower):
    """ Снайперская башня """
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/sniper_tower.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 300
        self.damage = 40
        self.rate_of_fire = 2000

    def find_target(self, enemies):
        """
        Поиск ближайшей цели
        :param enemies: Список врагов
        :return: Ближайший враг или None, если врагов нет в радиусе действия башни
        """
        healthiest_enemy = None
        max_health = 0
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.tower_range and enemy.health > max_health:
                healthiest_enemy = enemy
                max_health = enemy.health
        return healthiest_enemy

    def shoot(self, target, bullets_group):
        """
        Стрельба по цели.
        :param target: Цель
        :param bullets_group: Список пуль
        """
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class MoneyTower(Tower):
    """ Денежная башня """
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/money_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)

        # Генерируемая сумма за 1 выстрел
        self.damage = 50
        # Интервал выстрелов (генерации денег)
        self.rate_of_fire = 10000

    def update(self, enemies, current_time, bullets_group):
        """
        Обновляет состояние башни: проверка необходимости генерации денег.
        :param enemies: Список врагов.
        :param current_time: Текущее время.
        :param bullets_group: Список пуль.
        """
        if current_time - self.last_shot_time > self.rate_of_fire:
            # Увеличиваем сумму денег на счету игрока
            self.game.settings.starting_money += self.damage
            # Проиграть звук монет
            self.game.money_sound.play()
            self.last_shot_time = current_time
