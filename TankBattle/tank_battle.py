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
    tank2 = None

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
    # 创建一个炸弹的编组
    booms = Group()
    # bg_color = (230, 230, 230)

    stats = GameStats(ai_settings)
    # 创建一个Font对象
    font = pygame.font.SysFont("arial", 36)
    font.set_bold(True)

    clock = pygame.time.Clock()

    wait_count = 0
    invincible_count = 0
    # 开启游戏主循环
    while True:
        clock.tick(100)
        # 监视键盘鼠标
        gf.check_events(ai_settings, screen, tank, tank2, bullets, stats)

        if stats.game_active:
            if stats.game_step == GameStep.init:
                gf.start_image_update(tank, screen)
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
                if ai_settings.has_tank2 and tank2 is None:
                    tank2 = Tank(ai_settings, screen, 2)
                    tank2.x = 300
                    tank2.rect.bottom = screen.get_rect().bottom + 20
                    tank2.y = tank2.rect.y
                    tank2.moving_image = tank2.image

                wait_count += 1
                if wait_count == 500:
                    wait_count = 0
                    if len(enemies) < ai_settings.enemies_allowed:
                        gf.create_fleet(ai_settings, screen, enemies)
                if tank.is_invincible:
                    invincible_count += 1
                if invincible_count == 400:
                    tank.is_invincible = False
                    if tank2 is not None:
                        tank2.is_invincible = False
                tank.update()
                if tank2 is not None:
                    tank2.update()
                # enemy.upadte(bullets)
                gf.update_bullets(ai_settings, enemies, tank, tank2, bullets, enemy_bullets, screen, stats, booms)
                gf.update_enemies(enemies, enemy_bullets)
                gf.update_booms(booms)
                gf.update_screen(ai_settings, screen, tank, tank2, enemies, bullets, enemy_bullets, booms)
                # print(len(enemy_bullets))
        else:
            gf.over_image_update(screen)


run_game()
