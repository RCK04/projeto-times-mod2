from random import randint
import pygame
from src.util.constants import METAL
from src.component.obstacle.obstacle import Obstacle


class Metal(Obstacle):

    def __init__(self):
        images = METAL[randint(0, len(METAL)-1)]
        index = randint(0, len(images)-1)
        super().__init__(images, index)
        self.rect.y = 330
        self.sprite_index = 0

    def draw(self, display):
        self.image = self.images[self.sprite_index % len(self.images)].convert_alpha()
        self.obstacle_mask = pygame.mask.from_surface(self.image)
        self.mask = self.obstacle_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        display.blit(self.image, self.rect)
        self.sprite_index += 1
