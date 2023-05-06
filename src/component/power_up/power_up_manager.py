import random
import pygame
from src.component.power_up.sword import SWORD, Sword


class PowerUpManager:

    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300)
            self.power_ups.append(Sword())

    def update(self, score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            offset = (power_up.rect.x - player.rect.x), (power_up.rect.y - player.rect.y)
            if player.adventurer_mask.overlap(power_up.obstacle_mask, offset):
                power_up.start_time = pygame.time.get_ticks()
                player.has_power_up = True
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)
