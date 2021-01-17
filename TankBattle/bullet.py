import pygame
from pygame.sprite import Sprite

from enumClass import Direction


class Bullet(Sprite):
    """一个对坦克发射的子弹进行管理的类"""
    def __init__(self, ai_settings, screen, tank):
        """在坦克所处的位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.moving_image = pygame.image.load('images/bullet.png')
        self.image = pygame.image.load('images/bullet.png')

        if tank.direction == Direction.up:
            self.rect = self.moving_image.get_rect()
            # # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
            # self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_h, ai_settings.bullet_height_h)
            self.rect.centerx = tank.rect.centerx
            self.rect.top = tank.rect.top
            # # 存储用小数表示的子弹位置
            # 子弹上下移动的时候移动计算用
            self.y = float(self.rect.y)

            self.transform(Direction.up)

        elif tank.direction == Direction.right:
            # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_v, ai_settings.bullet_height_v)
            self.rect.centery = tank.rect.centery
            self.rect.left = tank.rect.right
            # 子弹作于移动的时候移动计算用
            self.x = float(self.rect.x)
        elif tank.direction == Direction.left:
            # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_v, ai_settings.bullet_height_v)
            self.rect.centery = tank.rect.centery
            self.rect.right = tank.rect.left
            # 子弹作于移动的时候移动计算用
            self.x = float(self.rect.x)
        elif tank.direction == Direction.down:
            # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_h, ai_settings.bullet_height_h)
            self.rect.centerx = tank.rect.centerx
            self.rect.top = tank.rect.bottom
            # 存储用小数表示的子弹位置
            # 子弹上下移动的时候移动计算用
            self.y = float(self.rect.y)

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        # 子弹发射的方向
        self.direction = tank.direction
        self.owner = None

    def update(self):
        if self.direction == Direction.up:
            """向上移动子弹"""
            # 更新表示子弹位置的小数值
            self.y -= self.speed_factor
            # 更新表示子弹的rect的位置
            self.rect.y = self.y
        elif self.direction == Direction.right:
            """向右移动子弹"""
            # 更新表示子弹位置的小数值
            self.x += self.speed_factor
            # 更新表示子弹的rect的位置
            self.rect.x = self.x
        elif self.direction == Direction.left:
            """向左移动子弹"""
            # 更新表示子弹位置的小数值
            self.x -= self.speed_factor
            # 更新表示子弹的rect的位置
            self.rect.x = self.x
        elif self.direction == Direction.down:
            """向下移动子弹"""
            # 更新表示子弹位置的小数值
            self.y += self.speed_factor
            # 更新表示子弹的rect的位置
            self.rect.y = self.y

    def transform(self, direction):
        if direction == Direction.right:
            self.moving_image = pygame.transform.rotate(self.image, 270)
        elif direction == Direction.left:
            self.moving_image = pygame.transform.rotate(self.image, 90)
        elif direction == Direction.up:
            self.moving_image = pygame.transform.rotate(self.image, 0)
        elif direction == Direction.down:
            self.moving_image = pygame.transform.rotate(self.image, 180)

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
