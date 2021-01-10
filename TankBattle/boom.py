import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """一个对坦克发射的子弹进行管理的类"""
    def __init__(self, ai_settings, screen, tank):
        """在坦克所处的位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen