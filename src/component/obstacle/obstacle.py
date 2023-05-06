import pygame
from pygame.sprite import Sprite
from src.util.constants import SCREEN_WIDTH


class Obstacle(Sprite):

    def __init__(self, images, index):
        self.images = images
        self.index = index
        self.image = self.images[self.index].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.obstacle_mask = pygame.mask.from_surface(self.image)
        self.mask = self.obstacle_mask.to_surface()

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, display):
        self.image = self.images[self.index].convert_alpha()
        self.obstacle_mask = pygame.mask.from_surface(self.image)
        self.mask = self.obstacle_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        display.blit(self.image, (self.rect.x, self.rect.y))
