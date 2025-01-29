# файл настроек, содержит параметры конфигурации игры, такие как размеры экрана,
# стоимость и параметры башен, пути к ресурсам и т.д.
from tower import BasicTower, SniperTower, MoneyTower
from random import choice

# Башни
tower_classes = {
    'basic': BasicTower,
    'sniper': SniperTower,
    'money': MoneyTower,
}

# Список путей
enemy_path_list = [
    [(50, 400), (300, 400), (300, 200), (600, 200), (600, 600), (900, 600), (900, 300), (1150, 300)],
    [(30, 600), (250, 400), (350, 180), (600, 200), (500, 600), (900, 600), (800, 300), (1150, 500)],
    [(30, 300), (600, 500), (300, 300), (600, 200), (500, 600), (900, 600), (700, 300), (1150, 400)],
    [(30, 400), (300, 200), (600, 600), (900, 200), (1150, 600)],
]

# Список врагов
image_enemy_paths = [
    ['assets/enemies/basic_enemy.png', {'speed': 1, 'health': 100, 'reward': 10,}],
    ['assets/enemies/fast_enemy.png', {'speed': 1.5, 'health': 150, 'reward': 20}],
    ['assets/enemies/strong_enemy.png', {'speed': 0.75, 'health': 200, 'reward': 30}],
    ['assets/enemies/croco_enemy.png', {'speed': 0.5, 'health': 250, 'reward': 40}],
    ['assets/enemies/shark_enemy.png', {'speed': 1.2, 'health': 300, 'reward': 50}],
]

# Текст подсказки
help_text = """Это игра в жанре "Tower Defense", где игроку предстоит защищать базу от волн врагов, расставляя башни.

Управление игрой осуществляется с клавиатуры. Ниже перечислены доступные клавиши управления.

   Цифровыми клавишами можно выбрать тип башни:
        Клавиша <1> - базовая башня
        Клавиша <2> - снайперская винтовка
        Клавиша <3> - денежная башня (генерирует деньги)
        Клавиша <0> - апгрейд башни (улучшает все характеристики башни на 20%)
   После выбора типа башни, следует указать мышью куда ее установить. 
   Башни устанавливать можно только на свободные места.

   Клавиша <Пробел> - показать/убрать позиции расположения башен.
   
   Клавиши <Enter>, <Пробел>, <F2>, <N> и <G> - начать новую игру.
   Клавиша <F2> во время игры завершает текущую игру. Можно начать новую игру.
   Клавиша <P> во время игры - пауза в игре.
"""

class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (150, 150, 0)
        self.text_color = (250, 250, 250)

        self.rows = 10
        self.cols = 15
        self.grid_size = (64, 64)

        self.tower_cost = 100
        self.tower_upgrade_cost = 150
        self.tower_sell_percentage = 0.75

        self.enemy_path = choice(enemy_path_list)

        self.tower_sprites = {
            'basic': 'assets/towers/basic_tower.png',
            'sniper': 'assets/towers/sniper_tower.png',
        }
        self.enemy_sprite = 'assets/enemies/basic_enemy.png'
        self.background_image = 'assets/backgrounds/game_background.png'

        self.shoot_sound = 'assets/sounds/shoot.wav'
        self.upgrade_sound = 'assets/sounds/upgrade.wav'
        self.sell_sound = 'assets/sounds/sell.wav'
        self.put_sound = 'assets/sounds/put.mp3'
        self.enemy_hit_sound = 'assets/sounds/archivo.mp3'
        self.oreshnik_sound = 'assets/sounds/oreshnik.mp3'
        self.money_sound = 'assets/sounds/money.mp3'
        self.background_music = 'assets/sounds/background_music.mp3'

        self.starting_money = 500
        self.lives = 20

        self.tower_positions = [
            (x * self.grid_size[0] + self.grid_size[0] // 2, y * self.grid_size[1] + self.grid_size[1] // 2)
            for x in range(1, self.cols) for y in range(3, self.rows)]
