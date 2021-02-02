import sys

import numpy
import pygame

import random
import tank_map
from boom import Boom
from enumClass import Direction, MapType, GameStep
from bullet import Bullet
from enemy import Enemy
from wall import WallBrick, WallSteel, WallSeawater, WallGrassland, WallHome
from pygame.sprite import Group


def check_events(ai_settings, screen, tank, tank2, bullets, stats):
    """相应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, tank, tank2, bullets, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, tank, tank2, stats)
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if stats.game_step == GameStep.init:
        #         stats.game_step = GameStep.ready


def update_screen(ai_settings, screen, tank, tank2, enemies, bullets, enemy_bullets, booms):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 后面重绘所有子弹
    for bullet in enemy_bullets.sprites():
        bullet.draw_bullet()
    # 重绘所有敌人
    for enemy in enemies.sprites():
        enemy.blit_me()
    tank.blit_me()
    tank.blit_invincible()
    if tank2 is not None:
        tank2.blit_me()
        tank2.blit_invincible()
    # enemy.blitme()
    # enemies.draw(screen)

    # 重绘所有炸弹
    for boom in booms.sprites():
        boom.blit_me()

    # 重绘地图
    bricks = tank_map.get_map(MapType.brick.name)
    bricks.draw(screen)
    steels = tank_map.get_map(MapType.steel.name)
    steels.draw(screen)
    seawater = tank_map.get_map(MapType.seawater.name)
    seawater.draw(screen)
    grassland = tank_map.get_map(MapType.grassland.name)
    grassland.draw(screen)
    home = tank_map.get_map(MapType.home.name)
    home.blit_me()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def check_keydown_events(event, ai_settings, screen, tank, tank2, bullets, stats):
    if stats.game_step == GameStep.init:
        if event.key == pygame.K_UP:
            if tank.y == 280:
                tank.y = 385
            tank.y -= 35
        elif event.key == pygame.K_DOWN:
            if tank.y == 350:
                tank.y = 245
            tank.y += 35
        elif event.key == pygame.K_SPACE:
            if tank.y > 280:
                ai_settings.has_tank2 = True
            tank.x = 180
            tank.rect.bottom = screen.get_rect().bottom - 20
            tank.y = tank.rect.y
            tank.moving_image = tank.image
            stats.game_step = GameStep.ready
    elif stats.game_step == GameStep.start:
        if event.key == pygame.K_RIGHT:
            # 坦克右移
            tank.moving_right = True
            tank.direction_priority.append(Direction.right)
        elif event.key == pygame.K_LEFT:
            tank.moving_left = True
            tank.direction_priority.append(Direction.left)
        elif event.key == pygame.K_UP:
            tank.moving_up = True
            tank.direction_priority.append(Direction.up)
        elif event.key == pygame.K_DOWN:
            tank.moving_down = True
            tank.direction_priority.append(Direction.down)
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, tank, bullets)

        if tank2 is not None:
            if event.key == pygame.K_d:
                # 坦克右移
                tank2.moving_right = True
                tank2.direction_priority.append(Direction.right)
            elif event.key == pygame.K_a:
                tank2.moving_left = True
                tank2.direction_priority.append(Direction.left)
            elif event.key == pygame.K_w:
                tank2.moving_up = True
                tank2.direction_priority.append(Direction.up)
            elif event.key == pygame.K_s:
                tank2.moving_down = True
                tank2.direction_priority.append(Direction.down)
            elif event.key == pygame.K_j:
                fire_bullet(ai_settings, screen, tank2, bullets)


def check_keyup_events(event, tank, tank2, stats):
    if stats.game_step == GameStep.start:
        if event.key == pygame.K_RIGHT:
            tank.moving_right = False
            tank.direction_priority.remove(Direction.right)
        elif event.key == pygame.K_LEFT:
            tank.moving_left = False
            tank.direction_priority.remove(Direction.left)
        if event.key == pygame.K_UP:
            tank.moving_up = False
            tank.direction_priority.remove(Direction.up)
        elif event.key == pygame.K_DOWN:
            tank.moving_down = False
            tank.direction_priority.remove(Direction.down)
        if tank2 is not None:
            if event.key == pygame.K_d:
                tank2.moving_right = False
                tank2.direction_priority.remove(Direction.right)
            elif event.key == pygame.K_a:
                tank2.moving_left = False
                tank2.direction_priority.remove(Direction.left)
            elif event.key == pygame.K_w:
                tank2.moving_up = False
                tank2.direction_priority.remove(Direction.up)
            elif event.key == pygame.K_s:
                tank2.moving_down = False
                tank2.direction_priority.remove(Direction.down)


def update_bullets(ai_settings, enemies, tank, tank2, bullets, enemy_bullets, screen, stats, booms):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()
    enemy_bullets.update()

    # 删除子弹
    delete_bullets(ai_settings, enemies, tank, tank2, bullets, enemy_bullets, screen, stats, booms)


def delete_bullets(ai_settings, enemies, tank, tank2, bullets, enemy_bullets, screen, stats, booms):
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # 显示爆炸
            show_boom(ai_settings, screen, booms, bullet.x, bullet.y)
            # print(len(bullets))
        if bullet.rect.right >= screen.get_rect().right:
            bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # 显示爆炸
            show_boom(ai_settings, screen, booms, bullet.x, bullet.y)
            # print(len(bullets))
        if bullet.rect.left <= 0:
            bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # 显示爆炸
            show_boom(ai_settings, screen, booms, bullet.x, bullet.y)
            # print(len(bullets))
        if bullet.rect.bottom >= screen.get_rect().bottom:
            bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # 显示爆炸
            show_boom(ai_settings, screen, booms, bullet.x, bullet.y)
            # print(len(bullets))
    # 删除已消失的子弹
    for bullet in enemy_bullets.copy():
        if bullet.rect.top <= 0:
            enemy_bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
        if bullet.rect.right >= screen.get_rect().right:
            enemy_bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
        if bullet.rect.left <= 0:
            enemy_bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
        if bullet.rect.bottom >= screen.get_rect().bottom:
            enemy_bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
    # 碰撞检测，如果有碰撞，删掉碰撞的精灵
    # 子弹碰到后抵消
    collisions = pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)
    for collide_bullet, collide_enemy_bullets in collisions.items():
        collide_bullet.owner.bullet_count -= 1
        for enemy_bullet in collide_enemy_bullets:
            enemy_bullet.owner.bullet_count -= 1
    # 子弹攻击到敌人后，一起消失
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
    # if len(collisions) > 0:
    #     print(collisions)
    for bullet, kill_enemies in collisions.items():
        bullet.owner.bullet_count -= 1
        # 显示爆炸
        show_boom(ai_settings, screen, booms, bullet.x, bullet.y)
        for enemy in kill_enemies:
            enemies.remove(enemy)
            ai_settings.enemies_allowed -= 1
        if  ai_settings.enemies_allowed == 0:
            stats.game_active = False

    # 子弹打到砖墙时动作
    bricks = tank_map.get_map(MapType.brick.name)
    collisions = pygame.sprite.groupcollide(bullets, bricks, True, True)
    for bullet in collisions.keys():
        bullet.owner.bullet_count -= 1
        # 显示爆炸
        show_boom(ai_settings, screen, booms, bullet.x, bullet.y)
    collisions = pygame.sprite.groupcollide(enemy_bullets, bricks, True, True)
    for bullet in collisions.keys():
        bullet.owner.bullet_count -= 1
    # 子弹打到钢铁墙时动作
    steels = tank_map.get_map(MapType.steel.name)
    collisions = pygame.sprite.groupcollide(bullets, steels, True, False)
    for bullet in collisions.keys():
        bullet.owner.bullet_count -= 1
        # 显示爆炸
        show_boom(ai_settings, screen, booms, bullet.x, bullet.y)
    collisions = pygame.sprite.groupcollide(enemy_bullets, steels, True, False)
    for bullet in collisions.keys():
        bullet.owner.bullet_count -= 1
    # 被敌人子弹攻击后触发
    collisions = pygame.sprite.spritecollide(tank, enemy_bullets, True)
    if len(collisions) > 0 and not tank.is_invincible:
        stats.game_active = False
    if tank2 is not None:
        collisions = pygame.sprite.spritecollide(tank2, enemy_bullets, True)
        if len(collisions) > 0 and not tank2.is_invincible:
            stats.game_active = False
    # 老家被打到
    home = tank_map.get_map(MapType.home.name)
    collisions = pygame.sprite.spritecollide(home, enemy_bullets, True)
    if len(collisions) > 0:
        WallHome.break_home(home)
        stats.game_active = False
    collisions = pygame.sprite.spritecollide(home, bullets, True)
    if len(collisions) > 0:
        WallHome.break_home(home)
        stats.game_active = False


def show_boom(ai_settings, screen, booms, x, y):
    new_boom = Boom(ai_settings, screen)
    new_boom.centerx = x
    new_boom.centery = y
    booms.add(new_boom)


def fire_bullet(ai_settings, screen, tank, bullets):
    # 创建一颗子弹，并将其加入到编组bullets中
    if tank.bullet_count < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, tank)
        new_bullet.owner = tank
        bullets.add(new_bullet)
        tank.bullet_count += 1


def create_fleet(ai_settings, screen, enemies):
    enemy_x = [0, 240, 480]
    numpy.random.shuffle(enemy_x)
    rand_int = random.randint(1, 3)
    if len(enemies) + rand_int > ai_settings.enemies_allowed:
        count = ai_settings.enemies_allowed - len(enemies)
    else:
        count = rand_int
    for x in enemy_x[0:count]:
        enemy = Enemy(ai_settings, screen)
        enemy.x = x
        enemy.rect.x = enemy.x
        enemies.add(enemy)


def update_enemies(enemies, enemy_bullets):
    enemies.update(enemy_bullets)


def update_booms(booms):
    booms.update(booms)


def create_map(ai_settings, screen):
    bricks = Group()
    steels = Group()
    seawater = Group()
    grassland = Group()
    row_index = 0
    for row in ai_settings.map:
        row_index += 1
        for i, item in enumerate(row):
            if item == MapType.brick.value:
                wall_brick = WallBrick(ai_settings, screen)
                wall_brick.x = i * 20
                wall_brick.y = (row_index - 1) * 20
                wall_brick.rect.x = wall_brick.x
                wall_brick.rect.y = wall_brick.y
                bricks.add(wall_brick)
            if item == MapType.steel.value:
                wall_steel = WallSteel(ai_settings, screen)
                wall_steel.x = i * 20
                wall_steel.y = (row_index - 1) * 20
                wall_steel.rect.x = wall_steel.x
                wall_steel.rect.y = wall_steel.y
                steels.add(wall_steel)
            if item == MapType.seawater.value:
                wall_seawater = WallSeawater(ai_settings, screen)
                wall_seawater.x = i * 20
                wall_seawater.y = (row_index - 1) * 20
                wall_seawater.rect.x = wall_seawater.x
                wall_seawater.rect.y = wall_seawater.y
                seawater.add(wall_seawater)
            if item == MapType.grassland.value:
                wall_grassland = WallGrassland(ai_settings, screen)
                wall_grassland.x = i * 20
                wall_grassland.y = (row_index - 1) * 20
                wall_grassland.rect.x = wall_grassland.x
                wall_grassland.rect.y = wall_grassland.y
                grassland.add(wall_grassland)
    tank_map.set_map(MapType.brick.name, bricks)
    tank_map.set_map(MapType.steel.name, steels)
    tank_map.set_map(MapType.seawater.name, seawater)
    tank_map.set_map(MapType.grassland.name, grassland)
    # 创建老家
    my_home = WallHome(ai_settings, screen)
    my_home.rect.x = 240
    my_home.rect.bottom = screen.get_rect().bottom - 20
    tank_map.set_map(MapType.home.name, my_home)


def start_image_update(tank, screen):
    button_image = pygame.image.load('images/start_image.jpg')
    button_rect = button_image.get_rect()
    button_rect.x = 0
    button_rect.y = 0
    screen.blit(button_image, button_rect)

    tank.moving_image = pygame.transform.rotate(tank.image, 270)
    tank.update()
    tank.blit_me()
    pygame.display.flip()


def over_image_update(screen):
    button_image = pygame.image.load('images/game_over.png').convert()
    button_image.set_alpha(10)
    button_image = pygame.transform.scale(button_image, (screen.get_rect().width, screen.get_rect().height))
    button_rect = button_image.get_rect()
    button_rect.x = 0
    button_rect.y = 0
    screen.blit(button_image, button_rect)

    pygame.display.flip()


def login(screen, count, index):

    rect = pygame.Rect(0, 0, 20, 20)
    rect.x = 100
    rect.y = 100
    if (count % 100) > 50:
        pygame.draw.rect(screen, (60, 60, 60), rect)
    else:
        pygame.draw.rect(screen, (0, 0, 0), rect)
    # 创建一个Font对象
    font = pygame.font.SysFont("arial", 36)
    font.set_bold(True)
    text_surface = font.render(u'Please enter your user ', False, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
