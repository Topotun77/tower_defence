# Главный файл, содержащий основной игровой цикл, обработку событий,
# обновление состояний игры и отрисовку элементов игры.

import sys

import pygame

from grid import Grid
from level import Level
from settings import Settings, help_text


class TowerDefenseGame:
    """
    Главный класс игры, управляющий основным циклом игры, событиями, обновлениями состояний и отрисовкой.
    """
    def __init__(self):
        """
        Конструктор, инициализирует основные параметры игры, загружает ресурсы и создаёт объекты уровня и сетки.
        """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load(self.settings.background_image).convert()
        self.background = pygame.transform.scale(self.background,
                                                 (self.settings.screen_width, self.settings.screen_height))

        self.font = pygame.font.SysFont("Arial", 24)

        self.background_music = pygame.mixer.Sound(self.settings.background_music)
        self.shoot_sound = pygame.mixer.Sound(self.settings.shoot_sound)
        self.enemy_hit_sound = pygame.mixer.Sound(self.settings.enemy_hit_sound)
        self.put_sound = pygame.mixer.Sound(self.settings.put_sound)
        self.oreshnik_sound = pygame.mixer.Sound(self.settings.oreshnik_sound)
        self.money_sound = pygame.mixer.Sound(self.settings.money_sound)

        self.background_music.set_volume(0.15)
        self.background_music.play(loops=-1)

        self.level = Level(self)
        self.grid = Grid(self)
        self.show_grid = 2

        self.selected_tower_type = 'basic'
        self.is_game_over = False
        self.show_help = True

        self.last_event_text = ''

    def game_over(self):
        """ Обрабатывает условия окончания игры. """
        self.is_game_over = True

    def is_position_inside(self, pos):
        """ Проверяет, находится ли позиция в пределах игрового поля. """
        return 0 <= pos.x <= self.settings.screen_width and 0 <= pos.y <= self.settings.screen_height

    def _check_events(self):
        """ Обрабатывает игровые события, такие как нажатие клавиш и клики мыши. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.show_help:
                if (event.type == pygame.KEYDOWN and
                        event.key in [pygame.K_KP_ENTER, pygame.K_n, pygame.K_g, pygame.K_SPACE, pygame.K_F2, pygame.K_p]):
                    # Начать игру, если нажата кнопка начала игры
                    print('start')
                    self.show_help = False
            elif event.type == pygame.KEYDOWN:
                # Если игра закончена - начать новую игру по нажатию кнопки
                if ((self.is_game_over or self.level.all_waves_complete)
                        and event.key in [pygame.K_KP_ENTER, pygame.K_n, pygame.K_g, pygame.K_SPACE, pygame.K_F2, pygame.K_p]):
                    self.show_help = True
                elif event.key == pygame.K_p:               # нажата клавиша "P"
                    # Пауза в игре
                    self.show_help = True
                elif event.key == pygame.K_F2:              # нажата клавиша "F2"
                    # Начать новую игру
                    self.is_game_over = True
                elif event.key == pygame.K_SPACE:           # нажата клавиша "пробел"
                    self.show_grid = (self.show_grid + 1) % 5
                    self.last_event_text = "Show/Hide grid"
                    print(self.last_event_text)
                elif event.key == pygame.K_1:               # нажата клавиша "1"
                    self.selected_tower_type = 'basic'
                    self.last_event_text = "Selected basic tower."
                    print(self.last_event_text)
                elif event.key == pygame.K_2:               # нажата клавиша "2"
                    self.selected_tower_type = 'sniper'
                    self.last_event_text = "Selected sniper tower."
                    print(self.last_event_text)
                elif event.key == pygame.K_3:               # нажата клавиша "3"
                    self.selected_tower_type = 'money'
                    self.last_event_text = "Selected money tower."
                    print(self.last_event_text)
                elif event.key == pygame.K_0:               # нажата клавиша "0"
                    # Апгрейд башни
                    self.selected_tower_type = 'upgrade'
                    self.last_event_text = "Selected upgrade tower."
                    print(self.last_event_text)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.is_game_over:
                # Не выбран никакой тип башни
                if not self.selected_tower_type:
                    self.last_event_text = "No tower type selected."
                    print(self.last_event_text)
                    return
                mouse_pos = pygame.mouse.get_pos()
                for tower in self.level.towers:
                    if tower.rect.collidepoint(mouse_pos):
                       # Позиция занята
                        if self.selected_tower_type != 'upgrade':
                            self.last_event_text = "The position is occupied."
                            print(self.last_event_text)
                            return
                        else:
                            # Апгрейд башни если нашли башню
                            tower.upgrade()
                else:
                    if self.selected_tower_type != 'upgrade':
                        # Установить башню
                        self.level.attempt_place_tower(mouse_pos, self.selected_tower_type)
                    else:
                        # Нет башни для апгрейда
                        self.last_event_text = "There is no tower to upgrade."
                        print(self.last_event_text)


    def _update_game(self):
        """ Обновляет состояние игры, вызывая обновления уровня и сетки. """
        self.level.update()
        self.grid.update()


    def _draw_win_screen(self):
        """ Отображает экран победы. """
        win_text = "You Win!"
        win_render = self.font.render(win_text, True, (255, 215, 0))
        win_rect = win_render.get_rect(center=(self.settings.screen_width/2, self.settings.screen_height/2))
        self.screen.blit(win_render, win_rect)

    def _draw_game_over_screen(self):
        """ Отображает экран проигрыша. """
        self.screen.fill((0, 0, 0))

        game_over_text = "Game Over!"
        game_over_render = self.font.render(game_over_text, True, (255, 0, 0))
        game_over_rect = game_over_render.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2))

        self.screen.blit(game_over_render, game_over_rect)

    def _draw(self):
        """ Управляет отрисовкой всех элементов игры. """
        if self.is_game_over:
            self._draw_game_over_screen()
        elif self.show_help:
            self.screen.blit(self.background, (0, 0))
            help_list = list(help_text.split('\n'))
            for i in range(len(help_list)):
                help_text_label = self.font.render(help_list[i], True, (255, 255, 255))
                self.screen.blit(help_text_label, (10, 30*(i+1)))
        else:
            self.screen.blit(self.background, (0, 0))
            self.level.draw(self.screen)
            if self.show_grid in [2, 4]:
                self.grid.draw()

            money_text = self.font.render(f"Money: ${int(self.settings.starting_money)}", True, (255, 255, 255))
            tower_text = self.font.render(
                f"Selected Tower: {self.selected_tower_type if self.selected_tower_type else 'None'}", True,
                (255, 255, 255))
            waves_text = self.font.render(f"Waves Left: {len(self.level.waves) - self.level.current_wave}", True,
                                          (255, 255, 255))
            enemies_text = self.font.render(f"Enemies Left: {len(self.level.enemies)}", True, (255, 255, 255))
            last_event_text = self.font.render(f"Last Event: {self.last_event_text}", True, (255, 255, 255))

            self.screen.blit(money_text, (10, 10))
            self.screen.blit(tower_text, (10, 40))
            self.screen.blit(waves_text, (10, 70))
            self.screen.blit(enemies_text, (10, 100))
            self.screen.blit(last_event_text, (250, 10))

            if self.level.all_waves_complete:
                self._draw_win_screen()

        pygame.display.flip()

    def run_game(self):
        """ Запускает основной игровой цикл. """
        while True:
            self._check_events()
            if not self.show_help and not self.is_game_over:
                self._update_game()

                if len(self.level.enemies) == 0 and not self.level.all_waves_complete:
                    self.level.start_next_wave()
            self._draw()
            self.clock.tick(60)
            if self.is_game_over and self.show_help:
                return



if __name__ == '__main__':
    while True:
        td_game = TowerDefenseGame()
        td_game.run_game()
