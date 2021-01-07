import pygame
from pygame.sprite import Sprite

from enumClass import Direction


class WallBrick(Sprite):
    """地图的类"""
    def __init__(self, ai_settings, screen):
        super(WallBrick, self).__init__()
        # 初期化
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/map_brick.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x = 0
        self.rect.y = 0
