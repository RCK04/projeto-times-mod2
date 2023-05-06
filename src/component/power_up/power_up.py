import random
import pygame
from pygame.sprite import Sprite
from src.util.constants import SCREEN_WIDTH


class PowerUp(Sprite):

    def __init__(self, images, index):
        self.images = images
        self.index = index
        self.image = self.images[self.index].convert_alpha()
        self.rect = self.image.get_rect()
        self.obstacle_mask = pygame.mask.from_surface(self.image)
        self.mask = self.obstacle_mask.to_surface()
        self.rect.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.rect.y = random.randint(190, 250)
        self.start_time = 0
        self.duration = random.randint(5, 10)

    def update(self, game_speed, power_ups):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            power_ups.pop()

    def draw(self, display):
        self.image = self.images[self.index].convert_alpha()
        self.obstacle_mask = pygame.mask.from_surface(self.image)
        self.mask = self.obstacle_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        display.blit(self.image, (self.rect.x, self.rect.y))
                