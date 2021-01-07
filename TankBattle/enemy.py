import numpy
import pygame
import random
from pygame.sprite import Sprite

import tank_map
from bullet import Bullet
from enumClass import Direction, MapType


class Enemy(Sprite):
    """表示单个敌人的类"""
    def __init__(self, ai_settings, screen):
        super(Enemy, self).__init__()
        # 初期化
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载坦克图像并获取其外接矩形
        self.moving_image = pygame.image.load('images/tank_enemy.jpg')
        self.image = pygame.image.load('images/tank_enemy.jpg')
        self.rect = self.moving_image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将每艘新坦克放在屏幕底部中央
        self.rect.x = 0  # self.rect.width
        self.rect.y = 0  # self.rect.height
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = True
        # 在坦克的属性center中存储小数值
        self.x = 0
        self.y = 0
        # 坦克运行的方向
        self.direction = Direction.down
        # 坦克发出子弹数
        self.bullet_count = 0

    def blit_me(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.moving_image, self.rect)

    # def upadte(self, bullets):
    def update(self, enemy_bullets):
        """持续运动"""
        if self.need_transform():
            self.transform()
        if self.moving_right:
            self.x += self.ai_settings.tank_speed_factor
        if self.moving_left:
            self.x -= self.ai_settings.tank_speed_factor
        if self.moving_up:
            self.y -= self.ai_settings.tank_speed_factor
        if self.moving_down:
            self.y += self.ai_settings.tank_speed_factor

        # 根据self.center更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y

        if self.bullet_count < self.ai_settings.bullets_allowed:
            can_add = True
            for bullet in enemy_bullets.copy():
                if bullet.owner == self:
                    # 子弹发出70后在继续发下一个
                    rand_int = random.randint(0, 500)
                    # print(rand_int)
                    if self.direction == Direction.down or self.direction == Direction.up:
                        # print(abs(bullet.rect.centery - self.rect.centery))
                        if abs(bullet.rect.centery - self.rect.centery) < 70:
                            can_add = False
                            # 随机判断要不要发出下一发子弹
                        elif rand_int < 499:
                            can_add = False
                    if self.direction == Direction.right or self.direction == Direction.left:
                        if abs(bullet.rect.centerx - self.rect.centerx) < 70:
                            can_add = False
                            # 随机判断要不要发出下一发子弹
                        elif rand_int < 499:
                            can_add = False
            if can_add:
                new_bullet = Bullet(self.ai_settings, self.screen, self)
                new_bullet.owner = self
                enemy_bullets.add(new_bullet)
                self.bullet_count += 1

    def transform(self):
        # 随机转向
        array = [Direction.right, Direction.left, Direction.up, Direction.down]
        while True:
            numpy.random.shuffle(array)
            if self.direction != array[0]:
                direction = array[0]
                break
        if direction == Direction.right:
            if self.direction != Direction.right:
                self.direction = Direction.right
                self.moving_image = pygame.transform.rotate(self.image, 90)
            self.moving_right = True
            self.moving_left = False
            self.moving_up = False
            self.moving_down = False
        elif direction == Direction.left:
            if self.direction != Direction.left:
                self.direction = Direction.left
                self.moving_image = pygame.transform.rotate(self.image, 270)
            self.moving_right = False
            self.moving_left = True
            self.moving_up = False
            self.moving_down = False
        elif direction == Direction.up:
            if self.direction != Direction.up:
                self.direction = Direction.up
                self.moving_image = pygame.transform.rotate(self.image, 180)
            self.moving_right = False
            self.moving_left = False
            self.moving_up = True
            self.moving_down = False
        elif direction == Direction.down:
            if self.direction != Direction.down:
                self.direction = Direction.down
                self.moving_image = pygame.transform.rotate(self.image, 0)
            self.moving_right = False
            self.moving_left = False
            self.moving_up = False
            self.moving_down = True

    def need_transform(self):
        if self.moving_right and self.rect.right >= self.screen_rect.right:
            return True
        if self.moving_left and self.rect.left <= 0:
            return True
        if self.moving_up and self.rect.top <= 0:
            return True
        if self.moving_down and self.rect.bottom >= self.screen_rect.bottom:
            return True
        # 随机改变行走方向
        rand_int = random.randint(0, 500)
        if rand_int > 480:
            self.ai_settings.enemy_transform += 1
            if self.ai_settings.enemy_transform > 10:
                # 转向太过频繁，再次均衡
                self.ai_settings.enemy_transform = 0
                return True
        collisions = pygame.sprite.spritecollide(self, tank_map.get_map(MapType.brick.name), False)
        if len(collisions) > 0:
            self.back_for_collide()
            return True
        collisions = pygame.sprite.spritecollide(self, tank_map.get_map(MapType.steel.name), False)
        if len(collisions) > 0:
            self.back_for_collide()
            return True
        collisions = pygame.sprite.spritecollide(self, tank_map.get_map(MapType.seawater.name), False)
        if len(collisions) > 0:
            self.back_for_collide()
            return True
        return False

    def back_for_collide(self):
        if self.moving_right:
            self.x -= self.ai_settings.tank_speed_factor
        if self.moving_left:
            self.x += self.ai_settings.tank_speed_factor
        if self.moving_up:
            self.y += self.ai_settings.tank_speed_factor
        if self.moving_down:
            self.y -= self.ai_settings.tank_speed_factor