import pygame

import tank_map
from enumClass import GameStep
from game_stats import GameStats
from settings import Settings
from tank import Tank
import game_functions as gf
from pygame.sprite import Group

from wall import WallHome


def run_game():
    # 初期化一个
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Tank Battle")

    # 创建一个坦克
    tank = Tank(ai_settings, screen)
    # 创建一个子弹分组
    bullets = Group()
    # 创建一个敌人子弹分组
    enemy_bullets = Group()
    # 创建一个敌人编组
    enemies = Group()
    # 创建一个敌人
    # enemy = Enemy(ai_settings, screen)
    # 创建外敌人群
    gf.create_fleet(ai_settings, screen, enemies)

    # 创建一个砖墙编组
    gf.create_map(ai_settings, screen)

    # bg_color = (230, 230, 230)

    stats = GameStats(ai_settings)
    # 创建一个Font对象
    font = pygame.font.SysFont("arial", 36)
    font.set_bold(True)

    clock = pygame.time.Clock()

    wait_count = 0
    # 开启游戏主循环
    while True:
        clock.tick(100)
        # 监视键盘鼠标
        gf.check_events(ai_settings, screen, tank, bullets, stats)

        if stats.game_active:
            if stats.game_step == GameStep.init:
                button_image = pygame.image.load('images/start_image.jpg')
                button_rect = button_image.get_rect()
                button_rect.x = 0
                button_rect.y = 0
                screen.blit(button_image, button_rect)
                pygame.display.flip()
            elif stats.game_step == GameStep.ready:
                wait_count += 1
                text_surface = font.render(u'level {0}'.format(stats.level), False, ai_settings.failed_color)
                text_rect = text_surface.get_rect()
                text_rect.centerx = screen.get_rect().centerx
                text_rect.centery = screen.get_rect().centery
                screen.fill(ai_settings.bg_color)
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
                if wait_count == 100:
                    wait_count = 0
                    stats.game_step = GameStep.start
            elif stats.game_step == GameStep.start:
                tank.update()
                # enemy.upadte(bullets)
                gf.update_bullets(enemies, tank, bullets, enemy_bullets, screen, stats)
                gf.update_enemies(enemies, enemy_bullets)
                gf.update_screen(ai_settings, screen, tank, enemies, bullets, enemy_bullets)
                # print(len(enemy_bullets))
        else:
            text_surface = font.render(u'Game Over', False, ai_settings.failed_color)
            text_rect = text_surface.get_rect()
            text_rect.centerx = screen.get_rect().centerx
            text_rect.centery = screen.get_rect().centery

            screen.blit(text_surface, text_rect)
            pygame.display.flip()


run_game()
