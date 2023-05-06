import pygame
import pygame.mixer
import random
from src.component.adventurer import Adventurer
from src.component.obstacle.obstacle_manager import ObstacleManager
from src.component.power_up.power_up_manager import PowerUpManager
from src.util.constants import TITLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, BACKGROUND, FPS
from src.util.text import draw_message_component


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.high_score = 0
        self.current_score = 0
        self.death_count = 0
        self.game_speed = 0
        self.background_y = 0
        self.player = Adventurer()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.music_list = [
            r'src/assets/sound/Sound_1.mp3',
            r'src/assets/sound/Sound_2.mp3'
        ]
        pygame.mixer.music.load(random.choice(self.music_list))
        pygame.mixer.music.play(-1)

    def execute(self):
        self.playing = True
        while self.playing:
            if not self.running:
                self.show_initial_menu()
        pygame.display.quit()
        pygame.quit()        

    def show_initial_menu(self):      
        self.display.blit(BACKGROUND, (0, 0))
        if self.death_count == 0:
            self.draw_start_message()
        else:
            self.draw_restart_message()
        pygame.display.update()
        pygame.display.flip()
        self.handle_events_on_menu()

    def draw_start_message(self):
        draw_message_component(
            "THE ADVENTURER'S JOURNEY",
            self.display, font_size=54,
            y_center=(SCREEN_HEIGHT // 2) - 40
        )
        draw_message_component(
            "Press any key to start",
            self.display,
            y_center=(SCREEN_HEIGHT // 2) + 20
        )
        self.player.draw(self.display)

    def draw_restart_message(self):
        draw_message_component(
            "Press any key to restart the game",
            self.display,
            y_center=(SCREEN_HEIGHT // 2)
        )
        draw_message_component(
            f"HIGH SCORE: {int(self.high_score)}",
            self.display,
            y_center=(SCREEN_HEIGHT // 2) - 150
        )
        draw_message_component(
            f"LAST SCORE: {int(self.current_score)}",
            self.display,
            y_center=(SCREEN_HEIGHT // 2) - 100
        )
        draw_message_component(
            f"DEATHS: {int(self.death_count)}",
            self.display,
            y_center=(SCREEN_HEIGHT // 2) - 50
        )

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.player.run = False
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()
                
    def run(self):
        self.running = True
        self.player.run = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.game_speed = 15
        self.current_score = 0
        while self.running:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.player.run = False
                self.running = False
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_current_score()
        self.power_up_manager.update(self.current_score, self.game_speed, self.player)

    def update_current_score(self):
        self.current_score += 1
        if self.high_score == 0 or self.high_score < self.current_score:
            self.high_score = self.current_score
        if self.current_score % 100 == 0:
            self.game_speed += 0.5

    def draw(self):
        self.clock.tick(FPS)
        self.draw_background()
        self.player.draw(self.display)
        self.obstacle_manager.draw(self.display)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.display)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        rel_x = self.background_y % BACKGROUND.get_rect().width
        self.display.blit(BACKGROUND, (rel_x - BACKGROUND.get_rect().width, 0))
        if rel_x < SCREEN_WIDTH:
            self.display.blit(BACKGROUND, (rel_x, 0))
        self.background_y -= self.game_speed

    def draw_score(self):
        high_score_message = "HIGH SCORE: " + str(int(self.high_score))
        score_message = "SCORE: " + str(int(self.current_score))
        draw_message_component(
            f'{high_score_message}',
            self.display,
            x_center=750,
            y_center=50
        )
        draw_message_component(
            f'{score_message}',
            self.display,
            x_center=730,
            y_center=80
        )

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(
                    f"Sword enable for {time_to_show} seconds",
                    self.display,
                    font_size=18,
                    x_center=500,
                    y_center=40
                )
            else:
                self.player.has_power_up = False
