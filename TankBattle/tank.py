import pygame

import tank_map
from enumClass import Direction, MapType


class Tank:
    def __init__(self, ai_settings, screen):
        # 初期化
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载坦克图像并获取其外接矩形
        self.moving_image = pygame.image.load('images/tank_y.jpg')
        self.image = pygame.image.load('images/tank_y.jpg')
        self.rect = self.moving_image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将每艘新坦克放在屏幕底部中央
        self.x = 180
        self.rect.x = self.x
        self.rect.bottom = self.screen_rect.bottom
        self.y = self.rect.y
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        # 坦克运行的方向
        self.direction = Direction.up
        # 坦克唯一标识
        self.bullet_count = 0
        self.hasCollide = False

    def blit_me(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.moving_image, self.rect)

    def update(self):
        """持续运动"""
        # if self.moving_right and self.rect.right < self.screen_rect.right:
        #     if not self.must_stop():
        #         self.x += self.ai_settings.tank_speed_factor
        # if self.moving_left and self.rect.left > 0:
        #     if not self.must_stop():
        #         self.x -= self.ai_settings.tank_speed_factor
        # if self.moving_up and self.rect.top > 0:
        #     if not self.must_stop():
        #         self.y -= self.ai_settings.tank_speed_factor
        # if self.moving_down and self.rect.y < self.screen_rect.bottom:
        #     if not self.must_stop():
        #         self.y += self.ai_settings.tank_speed_factor
        if self.must_stop():
            if self.moving_right:
                self.moving_right = False
            if self.moving_left:
                self.moving_left = False
            if self.moving_up:
                self.moving_up = False
            if self.moving_down:
                self.moving_down = False
        if self.moving_right:
            self.x += self.ai_settings.tank_speed_factor
        if self.moving_left:
            self.x -= self.ai_settings.tank_speed_factor
        if self.moving_up:
            self.y -= self.ai_settings.tank_speed_factor
        if self.moving_down:
            self.y += self.ai_settings.tank_speed_factor

        # 根据self.x更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y

    def transform(self, direction):
        if direction == Direction.right:
            if self.direction != Direction.right:
                self.direction = Direction.right
                self.moving_image = pygame.transform.rotate(self.image, 270)
        elif direction == Direction.left:
            if self.direction != Direction.left:
                self.direction = Direction.left
                self.moving_image = pygame.transform.rotate(self.image, 90)
        elif direction == Direction.up:
            if self.direction != Direction.up:
                self.direction = Direction.up
                self.moving_image = pygame.transform.rotate(self.image, 0)
        elif direction == Direction.down:
            if self.direction != Direction.down:
                self.direction = Direction.down
                self.moving_image = pygame.transform.rotate(self.image, 180)

    def must_stop(self):
        if self.moving_right and self.rect.right >= self.screen_rect.right:
            return True
        if self.moving_left and self.rect.left <= 0:
            return True
        if self.moving_up and self.rect.top <= 0:
            return True
        if self.moving_down and self.rect.bottom >= self.screen_rect.bottom:
            return True

        if self.hasCollide:
            self.hasCollide = False
        else:
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
        self.hasCollide = True
        if self.moving_right:
            self.x -= self.ai_settings.tank_speed_factor
        if self.moving_left:
            self.x += self.ai_settings.tank_speed_factor
        if self.moving_up:
            self.y += self.ai_settings.tank_speed_factor
        if self.moving_down:
            self.y -= self.ai_settings.tank_speed_factor