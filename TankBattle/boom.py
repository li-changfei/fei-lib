import pygame
from pygame.draw_py import Point
from pygame.sprite import Sprite


class Boom(Sprite):
    """一个对坦克发射的子弹进行管理的类"""
    def __init__(self, ai_settings, screen, tank):
        """在坦克所处的位置创建一个子弹对象"""
        super(Boom, self).__init__()
        self.screen = screen
        # 加载爆炸图像并获取其外接矩形
        self.master_image = [pygame.image.load('images/boom0.jpg'), pygame.image.load('images/boom1.jpg'), pygame.image.load('images/boom2.jpg')]
        self.image = pygame.image.load('images/boom2.jpg')
        self.rect = self.image.get_rect()
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0, 0.0)


def update(self, current_time, rate=0):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time
        screen.blit(self.image, self.rect)
