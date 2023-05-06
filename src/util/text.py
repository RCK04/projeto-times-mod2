import pygame
from src.util.constants import SCREEN_HEIGHT, SCREEN_WIDTH

FONT_COLOR = (255, 255, 255)
FONT_SIZE = 22
FONT_STYLE = 'freesansbold.ttf'


def draw_message_component(
        message,
        display,
        font_color=FONT_COLOR,
        font_size=FONT_SIZE,
        y_center=SCREEN_HEIGHT // 2,
        x_center=SCREEN_WIDTH // 2
):
    font = pygame.font.Font(FONT_STYLE, font_size)
    text = font.render(message, True, font_color)
    text_rect = text.get_rect()
    text_rect.center = (x_center, y_center)
    display.blit(text, text_rect)
