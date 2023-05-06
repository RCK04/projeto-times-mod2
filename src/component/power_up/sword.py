import pygame
from src.util.constants import SWORD
from src.component.power_up.power_up import PowerUp


class Sword(PowerUp):

    def __init__(self):
        self.sprite_index = 0
        super().__init__(SWORD, self.sprite_index)

    def draw(self, display):
        self.image = self.images[self.sprite_index % len(self.images)].convert_alpha()
        self.obstacle_mask = pygame.mask.from_surface(self.image)
        self.mask = self.obstacle_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        display.blit(self.image, self.rect)
        self.sprite_index += 1
