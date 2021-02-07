import sys

import numpy
import pygame

import random

import coonDB
import tank_map
from boom import Boom
from coonDB import update
from enumClass import Direction, MapType, GameStep
from bullet import Bullet
from enemy import Enemy
from register import register
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if stats.game_step == GameStep.login:
                if 150 < pos[0] < 360 and 300 < pos[1] < 430:
                    user_id = tank_map.get_map("user_id")
                    if len(user_id) == 0:
                        user_id = "defaultUser"
                        tank_map.set_map("user_id", user_id)
                    register(user_id)
                    if stats.game_step == GameStep.login:
                        stats.game_step = GameStep.init
            elif stats.game_step == GameStep.total:
                if 40 < pos[0] < 220 and 440 < pos[1] < 490:
                    stats.game_step = GameStep.init
                    stats.level = 1
                    score = tank_map.get_map("score")
                    score = 0
                    tank_map.set_map("score", score)

                    init_tank(tank, 0, screen)
                    tank.x = 120
                    tank.y = 280
                    if tank2 is not None:
                        init_tank(tank2, 1, screen)
                elif 300 < pos[0] < 480 and 440 < pos[1] < 490:
                    stats.game_active = False


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

    # 积分维护
    font = pygame.font.SysFont("arial", 20)
    area_y = screen.get_rect().bottom - 20

    rect = pygame.Rect(0, area_y, screen.get_rect().width, 20)
    pygame.draw.rect(screen, (60, 60, 60), rect)

    text_user_id_lbl = font.render("User :", False, (255, 255, 255))
    text_rect_lbl = text_user_id_lbl.get_rect()
    text_rect_lbl.x = 20
    text_rect_lbl.y = area_y

    user_id = tank_map.get_map("user_id")
    text_user_id = font.render(user_id, False, (255, 255, 255))
    text_rect = text_user_id.get_rect()
    text_rect.x = 80
    text_rect.y = area_y

    text_score_lbl = font.render("Score :", False, (255, 255, 255))
    score_rect_lbl = text_score_lbl.get_rect()
    score_rect_lbl.x = 220
    score_rect_lbl.y = area_y

    score = tank_map.get_map("score")
    text_score = font.render(str(score), False, (255, 255, 255))
    score_rect = text_score.get_rect()
    score_rect.x = 300
    score_rect.y = area_y

    screen.blit(text_user_id_lbl, text_rect_lbl)
    screen.blit(text_user_id, text_rect)
    screen.blit(text_score_lbl, score_rect_lbl)
    screen.blit(text_score, score_rect)

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def check_keydown_events(event, ai_settings, screen, tank, tank2, bullets, stats):
    if stats.game_step == GameStep.login:
        key = event.key
        unicode = event.unicode
        # print(key)
        # 只有
        if pygame.K_0 <= key <= pygame.K_9 or pygame.K_a <= key <= pygame.K_z:
            if unicode != "":
                char = unicode
            else:
                char = chr(key)
            input_text(char)
        elif key == pygame.K_BACKSPACE:
            user_id = tank_map.get_map("user_id")
            print(user_id)
            print(type(user_id))
            print(user_id[0: -1])
            user_id = user_id[0: -1]
            tank_map.set_map("user_id", user_id)
    elif stats.game_step == GameStep.init:
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
            else:
                ai_settings.has_tank2 = False
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
            if Direction.right in tank.direction_priority:
                tank.direction_priority.remove(Direction.right)
        elif event.key == pygame.K_LEFT:
            tank.moving_left = False
            if Direction.left in tank.direction_priority:
                tank.direction_priority.remove(Direction.left)
        if event.key == pygame.K_UP:
            tank.moving_up = False
            if Direction.up in tank.direction_priority:
                tank.direction_priority.remove(Direction.up)
        elif event.key == pygame.K_DOWN:
            tank.moving_down = False
            if Direction.down in tank.direction_priority:
                tank.direction_priority.remove(Direction.down)
        if tank2 is not None:
            if event.key == pygame.K_d:
                tank2.moving_right = False
                if Direction.right in tank2.direction_priority:
                    tank2.direction_priority.remove(Direction.right)
            elif event.key == pygame.K_a:
                tank2.moving_left = False
                if Direction.left in tank2.direction_priority:
                    tank2.direction_priority.remove(Direction.left)
            elif event.key == pygame.K_w:
                tank2.moving_up = False
                if Direction.up in tank2.direction_priority:
                    tank2.direction_priority.remove(Direction.up)
            elif event.key == pygame.K_s:
                tank2.moving_down = False
                if Direction.down in tank2.direction_priority:
                    tank2.direction_priority.remove(Direction.down)


def update_bullets(ai_settings, enemies, tank, tank2, bullets, enemy_bullets, screen, stats, booms):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update(stats, False)
    enemy_bullets.update(stats, True)

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
        score = tank_map.get_map("score")
        score += 100 * stats.level
        tank_map.set_map("score", score)
        bullet.owner.bullet_count -= 1
        # 显示爆炸
        show_boom(ai_settings, screen, booms, bullet.x, bullet.y)
        for enemy in kill_enemies:
            enemies.remove(enemy)
            ai_settings.enemies_allowed -= 1
        if ai_settings.enemies_allowed == 0:
            bullets.empty()
            enemy_bullets.empty()
            booms.empty()
            stats.game_step = GameStep.levelChange

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
        for bullet in collisions:
            bullet.owner.bullet_count -= 1
            # 显示爆炸
            show_boom(ai_settings, screen, booms, bullet.x, bullet.y)
        score = tank_map.get_map("score")
        score -= 200
        tank_map.set_map("score", score)
        init_tank(tank, 0, screen)
        # tank.is_invincible = True

    if tank2 is not None:
        collisions = pygame.sprite.spritecollide(tank2, enemy_bullets, True)
        if len(collisions) > 0 and not tank2.is_invincible:
            score = tank_map.get_map("score")
            score -= 200
            tank_map.set_map("score", score)
            init_tank(tank2, 1, screen)

    # 老家被打到
    home = tank_map.get_map(MapType.home.name)
    collisions = pygame.sprite.spritecollide(home, enemy_bullets, True)
    if len(collisions) > 0:
        WallHome.break_home(home)
        update_score()
        stats.game_step = GameStep.total
        bullets.empty()
        enemy_bullets.empty()
        booms.empty()
    collisions = pygame.sprite.spritecollide(home, bullets, True)
    if len(collisions) > 0:
        WallHome.break_home(home)
        update_score()
        stats.game_step = GameStep.total
        bullets.empty()
        enemy_bullets.empty()
        booms.empty()



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


def update_enemies(enemies, enemy_bullets, stats):
    enemies.update(enemy_bullets, stats)


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
    start_image = pygame.image.load('images/start_image.jpg')
    start_rect = start_image.get_rect()
    start_rect.x = 0
    start_rect.y = 0
    screen.blit(start_image, start_rect)

    tank.moving_image = pygame.transform.rotate(tank.image, 270)
    tank.update()
    tank.blit_me()
    pygame.display.flip()


def over_image_update(screen):
    over_image = pygame.image.load('images/game_over.png').convert()
    over_image.set_alpha(10)
    over_image = pygame.transform.scale(over_image, (screen.get_rect().width, screen.get_rect().height))
    over_rect = over_image.get_rect()
    over_rect.x = 0
    over_rect.y = 0
    screen.blit(over_image, over_rect)

    pygame.display.flip()


def login(screen, count, user_id):
    # 创建一个Font对象
    font = pygame.font.SysFont("arial", 20)
    index = 0

    for i in range(15):
        rect = pygame.Rect(100 + 20 * i, 100, 20, 20)
        pygame.draw.rect(screen, (0, 0, 0), rect)
    for index_str in user_id:
        text_user_id = font.render(index_str, False, (255, 255, 255))
        text_rect = text_user_id.get_rect()
        text_rect.x = 100 + 20 * index
        text_rect.y = 100
        index += 1

        screen.blit(text_user_id, text_rect)

    rect = pygame.Rect(100 + 20 * index, 100, 20, 20)
    if (count % 100) > 50:
        pygame.draw.rect(screen, (60, 60, 60), rect)
    else:
        pygame.draw.rect(screen, (0, 0, 0), rect)

    font = pygame.font.SysFont("arial", 36)
    text_surface = font.render(u'Please enter your user ', False, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery
    screen.blit(text_surface, text_rect)

    # 图片周围显示白边
    start_button = pygame.image.load('images/start_button.png').convert()
    # start_button.set_alpha(10)
    button_rect = start_button.get_rect()
    button_rect.centerx = screen.get_rect().centerx
    button_rect.centery = screen.get_rect().centery + 100

    rect = pygame.Rect(0, 0, button_rect.width + 4, button_rect.height + 4)
    rect.centerx = button_rect.centerx
    rect.centery = button_rect.centery
    pygame.draw.rect(screen, (255, 255, 255), rect)
    screen.blit(start_button, button_rect)
    pygame.display.flip()


def input_text(value):
    user_id = tank_map.get_map("user_id")
    if len(user_id) <= 15:
        user_id = user_id + str(value)
        tank_map.set_map("user_id", user_id)


def update_score():
    sql = "select * from  user_info WHERE user_id = %s and double_flg = %s"
    args = (tank_map.get_map("user_id"), tank_map.get_map("double_flg"))
    results = coonDB.query(sql, args)
    score = 0
    for row in results:
        score = row[1]

    if score < tank_map.get_map("score"):
        sql = "update user_info set score = %s where user_id = %s and double_flg = %s"
        args = (tank_map.get_map("score"), tank_map.get_map("user_id"), tank_map.get_map("double_flg"))
        update(sql, args)


def show_ranking_list(screen):
    # 创建一个Font对象
    font = pygame.font.SysFont("arial", 36)
    font.set_bold(True)
    rect = pygame.Rect(0, 0, screen.get_rect().width, screen.get_rect().height)
    pygame.draw.rect(screen, (0, 0, 0), rect)

    text_surface = font.render(u'RANKING LIST', False, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 20
    screen.blit(text_surface, text_rect)

    font = pygame.font.SysFont("arial", 20)
    font.set_bold(False)
    text_surface = font.render(u'SOLO', False, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = screen.get_rect().width / 4
    text_rect.y = 80
    screen.blit(text_surface, text_rect)

    sql = "select * from  user_info WHERE score <> 0 and double_flg = 0 order by score desc limit 10"
    results = coonDB.query_no_args(sql)
    index = 0
    for row in results:
        index += 1
        print(row)
        user_id = row[0]
        score = row[1]
        text_surface = font.render(user_id + "    :", False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.right = screen.get_rect().width / 4
        text_rect.y = 90 + 20 * index
        screen.blit(text_surface, text_rect)

        text_surface = font.render(str(score), False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.left = screen.get_rect().width / 4 + 20
        text_rect.y = 90 + 20 * index
        screen.blit(text_surface, text_rect)

    text_surface = font.render(u'DOUBLE', False, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = screen.get_rect().width / 4 * 3
    text_rect.y = 80
    screen.blit(text_surface, text_rect)

    sql = "select * from  user_info WHERE score <> 0 and double_flg = 1 order by score desc limit 10"
    results = coonDB.query_no_args(sql)
    index = 0
    for row in results:
        index += 1
        print(row)
        user_id = row[0]
        score = row[1]
        text_surface = font.render(user_id + "    :", False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.right = screen.get_rect().width / 4 * 3
        text_rect.y = 90 + 20 * index
        screen.blit(text_surface, text_rect)

        text_surface = font.render(str(score), False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.left = screen.get_rect().width / 4 * 3 + 20
        text_rect.y = 90 + 20 * index
        screen.blit(text_surface, text_rect)
    # 按钮图片加载
    try_again_button = pygame.image.load('images/btn_try_again.png').convert()
    try_again_button = pygame.transform.scale(try_again_button, (180, 50))
    button_rect = try_again_button.get_rect()
    button_rect.x = 40
    button_rect.y = screen.get_rect().bottom - 100
    screen.blit(try_again_button, button_rect)

    end_button = pygame.image.load('images/btn_game_over.png').convert()
    end_button = pygame.transform.scale(end_button, (180, 50))
    button_rect = end_button.get_rect()
    button_rect.right = screen.get_rect().width - 40
    button_rect.y = screen.get_rect().bottom - 100
    screen.blit(end_button, button_rect)
    pygame.display.flip()


def init_tank(tank, tank_flg, screen):
    # 移动标志
    tank.moving_right = False
    tank.moving_left = False
    tank.moving_up = False
    tank.moving_down = False
    # 坦克运行的方向
    tank.direction = Direction.up
    # 坦克移动方向优先度
    tank.direction_priority = []
    # 是不是无敌
    tank.is_invincible = True
    tank.bullet_count = 0
    tank.rect.bottom = screen.get_rect().bottom - 20
    tank.y = tank.rect.y
    tank.moving_image = tank.image

    if tank_flg == 0:
        tank.x = 180
    else:
        tank.x = 300
        tank_map.set_map("double_flg", 1)


def init_home(ai_settings, screen):
    # 创建一个砖墙编组
    create_map(ai_settings, screen)

    home = tank_map.get_map(MapType.home.name)
    WallHome.normal_home(home)