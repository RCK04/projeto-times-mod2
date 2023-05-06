import pygame.time
from src.component.obstacle.bird import Bird
from src.component.obstacle.metal import Metal
from src.component.obstacle.wood import Wood
from random import randint


class ObstacleManager:

    def __init__(self):
        self.obstacles = []
        self.death_sound = pygame.mixer.Sound('src/assets/sound/die.wav')

    def update(self, game):
        obstacle_type = [
            Metal(),
            Wood(),
            Bird()
        ]
        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[randint(0, len(obstacle_type) - 1)])
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            offset = (obstacle.rect.x - game.player.rect.x), (obstacle.rect.y - game.player.rect.y)
            if game.player.adventurer_mask.overlap(obstacle.obstacle_mask, offset) and game.player.attack and type(obstacle) != Metal:
                self.obstacles.remove(obstacle)
            elif game.player.adventurer_mask.overlap(obstacle.obstacle_mask, offset) and (not game.player.attack or (type(obstacle) == Metal)):
                self.death_sound.play()
                self.death_sound.set_volume(0.2)
                pygame.time.delay(500)
                game.player.reset_adventurer()
                game.running = False
                game.death_count += 1
                break

    def reset_obstacles(self):
        self.obstacles = []

    def draw(self, display):
        for obstacle in self.obstacles:
            obstacle.draw(display)
