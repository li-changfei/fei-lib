import pygame
from pygame.draw_py import Point
from pygame.sprite import Sprite


class Boom(Sprite):
    """一个对坦克发射的子弹进行管理的类"""

    def __init__(self, ai_settings, screen):
        """在坦克所处的位置创建一个子弹对象"""
        super(Boom, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        # 加载爆炸图像并获取其外接矩形
        self.image00 = pygame.image.load('images/boom0.png').convert()
        self.image00.set_colorkey((0, 0, 0))
        self.image01 = pygame.image.load('images/boom1.png').convert()
        self.image01.set_colorkey((0, 0, 0))
        self.image02 = pygame.image.load('images/boom2.png').convert()
        self.image02.set_colorkey((0, 0, 0))
        self.master_image = [self.image00,
                             self.image01,
                             self.image02]
        self.image = pygame.image.load('images/boom2.png').convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 2
        self.columns = 0
        self.last_time = 10
        self.direction = 0
        self.velocity = Point(0.0, 0.0)
        self.centerx = 0
        self.centery = 0

    def update(self, booms):
        # 根据self.center更新rect对象
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        # 循环显示动画效果
        if self.frame <= self.last_frame:
            if self.columns < self.last_time:
                self.columns += 1
            else:
                self.columns = 0
                self.image = self.master_image[self.frame]
                self.frame += 1
        else:
            booms.remove(self)

    def blit_me(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
