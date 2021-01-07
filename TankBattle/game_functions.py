import sys
import pygame

import tank_map
from enumClass import Direction, MapType, GameStep
from bullet import Bullet
from enemy import Enemy
from wall import WallBrick, WallSteel, WallSeawater, WallGrassland, WallHome
from pygame.sprite import Group


def check_events(ai_settings, screen, tank, bullets, stats):
    """相应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, tank, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, tank)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            stats.game_step = GameStep.ready


def update_screen(ai_settings, screen, tank, enemies, bullets, enemy_bullets):
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
    # enemy.blitme()
    # enemies.draw(screen)

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


def check_keydown_events(event, ai_settings, screen, tank, bullets):
    if event.key == pygame.K_RIGHT:
        # 坦克右移
        tank.moving_right = True
        tank.transform(Direction.right)
    elif event.key == pygame.K_LEFT:
        tank.moving_left = True
        tank.transform(Direction.left)
    elif event.key == pygame.K_UP:
        tank.moving_up = True
        tank.transform(Direction.up)
    elif event.key == pygame.K_DOWN:
        tank.moving_down = True
        tank.transform(Direction.down)
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, tank, bullets)


def check_keyup_events(event, tank):
    if event.key == pygame.K_RIGHT:
        tank.moving_right = False
    elif event.key == pygame.K_LEFT:
        tank.moving_left = False
    if event.key == pygame.K_UP:
        tank.moving_up = False
    elif event.key == pygame.K_DOWN:
        tank.moving_down = False


def update_bullets(enemies, tank, bullets, enemy_bullets, screen, stats):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()
    enemy_bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
        if bullet.rect.right >= screen.get_rect().right:
            bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
        if bullet.rect.right <= 0:
            bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
        if bullet.rect.bottom >= screen.get_rect().bottom:
            bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
    # 删除已消失的子弹
    for bullet in enemy_bullets.copy():
        if bullet.rect.bottom <= 0:
            enemy_bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
        if bullet.rect.right >= screen.get_rect().right:
            enemy_bullets.remove(bullet)
            bullet.owner.bullet_count -= 1
            # print(len(bullets))
        if bullet.rect.right <= 0:
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
    # 子弹攻击到敌人后，一起消失
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for bullet in collisions.keys():
        bullet.owner.bullet_count -= 1

    # 子弹打到砖墙时动作
    bricks = tank_map.get_map(MapType.brick.name)
    collisions = pygame.sprite.groupcollide(bullets, bricks, True, True)
    for bullet in collisions.keys():
        bullet.owner.bullet_count -= 1
    collisions = pygame.sprite.groupcollide(enemy_bullets, bricks, True, True)
    for bullet in collisions.keys():
        bullet.owner.bullet_count -= 1
    # 子弹打到钢铁墙时动作
    steels = tank_map.get_map(MapType.steel.name)
    collisions = pygame.sprite.groupcollide(bullets, steels, True, False)
    for bullet in collisions.keys():
        bullet.owner.bullet_count -= 1
    collisions = pygame.sprite.groupcollide(enemy_bullets, steels, True, False)
    for bullet in collisions.keys():
        bullet.owner.bullet_count -= 1
    # 被敌人子弹攻击后触发
    collisions = pygame.sprite.spritecollide(tank, enemy_bullets, True)
    if len(collisions) > 0:
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


def fire_bullet(ai_settings, screen, tank, bullets):
    # 创建一颗子弹，并将其加入到编组bullets中
    if tank.bullet_count < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, tank)
        new_bullet.owner = tank
        bullets.add(new_bullet)
        tank.bullet_count += 1


def create_fleet(ai_settings, screen, enemies):
    enemy = Enemy(ai_settings, screen)
    enemy.x = 0
    enemy.rect.x = enemy.x
    enemies.add(enemy)
    enemy = Enemy(ai_settings, screen)
    enemy.x = 240
    enemy.rect.x = enemy.x
    enemies.add(enemy)
    enemy = Enemy(ai_settings, screen)
    enemy.x = 480
    enemy.rect.x = enemy.x
    enemies.add(enemy)


def update_enemies(enemies, enemy_bullets):
    enemies.update(enemy_bullets)


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
    my_home.rect.bottom = screen.get_rect().bottom
    tank_map.set_map(MapType.home.name, my_home)


