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


class WallSteel(Sprite):
    """地图的类"""
    def __init__(self, ai_settings, screen):
        super(WallSteel, self).__init__()
        # 初期化
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/map_steel.JPG')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class WallSeawater(Sprite):
    """地图的类"""
    def __init__(self, ai_settings, screen):
        super(WallSeawater, self).__init__()
        # 初期化
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/map_seawater.JPG')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class WallGrassland(Sprite):
    """地图的类"""
    def __init__(self, ai_settings, screen):
        super(WallGrassland, self).__init__()
        # 初期化
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/map_grassland.JPG')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class WallHome(Sprite):
    """地图的类"""
    def __init__(self, ai_settings, screen):
        super(WallHome, self).__init__()
        # 初期化
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/home.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def break_home(self):
        self.image = pygame.image.load('images/break_home.jpg')

    def normal_home(self):
        self.image = pygame.image.load('images/home.jpg')

    def blit_me(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
