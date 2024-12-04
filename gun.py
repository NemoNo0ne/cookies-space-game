import pygame
from pygame.sprite import Sprite
class Gun(Sprite):

    def __init__(self, screen):
        """Инициализация пушки"""

        super(Gun, self).__init__()

        self.screen = screen
        self.image = pygame.image.load('img/pixil-frame-0.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.mright = False
        self.mleft = False
        self.shooting = False

    def output(self):
        """Рисунок корабля"""
        self.screen.blit(self.image, self.rect)

    def update_gun(self):
        """Обновление позиции корабля"""
        if self.mright and self.rect.right < self.screen_rect.right:
            self.center += 1
        if self.mleft and self.rect.left > 0:
            self.center -= 1

        self.rect.centerx = self.center

    def creat_gun(self):
        """Размешает пушку по центру внизу"""
        self.center = self.screen_rect.centerx
