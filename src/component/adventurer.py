import pygame
from pygame.sprite import Sprite
from src.util.constants import ADVENTURER_IDLE, ADVENTURER_RUN, ADVENTURER_JUMP, ADVENTURER_FALL, ADVENTURER_SLIDE, ADVENTURER_ATTACK, ADVENTURER_AIR_ATTACK


ADVENTURER_X = 130
ADVENTURER_Y = 275
JUMP_VEL = 8.5
SLIDE_VEL = 8.5
ATTACK_VEL = 8.5
AIR_ATTACK_VEL = 8.5


class Adventurer(Sprite):

    def __init__(self):
        self.image = ADVENTURER_IDLE[0].convert_alpha()
        self.rect = self.image.get_rect()
        self.adventurer_mask = pygame.mask.from_surface(self.image)
        self.mask = self.adventurer_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        self.rect.x = ADVENTURER_X
        self.rect.y = ADVENTURER_Y
        self.jump_vel = JUMP_VEL
        self.slide_vel = SLIDE_VEL
        self.attack_vel = ATTACK_VEL
        self.air_attack_vel = AIR_ATTACK_VEL
        self.sprite_index = 0
        self.run = False
        self.jump = False
        self.slide = False
        self.attack = False
        pygame.mixer.init() # inicializa o mixer
        self.jump_sound = pygame.mixer.Sound('src/assets/sound/jump.ogg') # carrega o arquivo de som para pular
        self.sword_sound = pygame.mixer.Sound('src/assets/sound/sword_hit.wav') # carrega o arquivo de som para pular
        self.setup_state()

    def setup_state(self):
        self.has_power_up = False
        self.show_text = False
        self.shield_time_up = 0

    def update(self, user_input):
        if self.run:
            self.adventurer_run()
        elif self.jump and not self.attack:
            self.adventurer_jump()
        elif self.jump and self.attack:
            self.air_attack()
        elif self.slide:
            self.adventurer_slide()
        elif self.attack and self.has_power_up:
            self.adventurer_attack()

        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE] or user_input[pygame.K_w]) and not self.jump:
            self.run = False
            self.jump = True
            self.slide = False
            self.attack = False 
            self.jump_sound.play()  # toca o som de pular
            self.jump_sound.set_volume(0.3)       
        elif user_input[pygame.K_DOWN] or user_input[pygame.K_LCTRL] or user_input[pygame.K_s]:
            self.run = False
            self.jump = False
            self.slide = True
            self.attack = False
        elif (user_input[pygame.K_RIGHT] or user_input[pygame.K_d]) and self.jump and self.has_power_up:
            self.run = False
            self.slide = False
            self.attack = True
            self.sword_sound.play()# toca o som de ataque
            self.sword_sound.set_volume(0.06)
        elif (user_input[pygame.K_RIGHT] or user_input[pygame.K_d]) and not self.jump and self.has_power_up:
            self.run = False
            self.jump = False
            self.slide = False
            self.attack = True
            self.sword_sound.play()# toca o som de ataque
            self.sword_sound.set_volume(0.06)
        elif not self.jump and not self.slide and not self.attack:
            self.run = True

    def adventurer_run(self):
        self.image = ADVENTURER_RUN[int(self.sprite_index) % len(ADVENTURER_RUN)].convert_alpha()
        self.rect = self.image.get_rect()
        self.adventurer_mask = pygame.mask.from_surface(self.image)
        self.mask = self.adventurer_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        self.rect.x = ADVENTURER_X
        self.rect.y = ADVENTURER_Y
        self.sprite_index += 0.3

    def adventurer_jump(self):
        self.image = ADVENTURER_JUMP[int(self.sprite_index) % len(ADVENTURER_JUMP)].convert_alpha()
        self.adventurer_mask = pygame.mask.from_surface(self.image)
        self.mask = self.adventurer_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        if self.jump:
            self.rect.y -= self.jump_vel * 2
            self.jump_vel -= 0.8
            self.sprite_index += 0.3
        if self.jump_vel < -JUMP_VEL:
            self.rect.y = ADVENTURER_Y
            self.jump_vel = JUMP_VEL
            self.jump = False
            self.sprite_index = 0

    def adventurer_slide(self):
        if self.rect.y < ADVENTURER_Y:
            self.image = ADVENTURER_FALL[int(self.sprite_index) % len(ADVENTURER_FALL)].convert_alpha()
            self.adventurer_mask = pygame.mask.from_surface(self.image)
            self.mask = self.adventurer_mask.to_surface(unsetcolor=(0, 0, 0, 0))
            self.rect.y -= self.jump_vel
            self.jump_vel -= 2
            self.sprite_index += 0.3
        else:
            self.rect.y = ADVENTURER_Y
            self.jump_vel = JUMP_VEL
            self.image = ADVENTURER_SLIDE[int(self.sprite_index) % len(ADVENTURER_SLIDE)].convert_alpha()
            self.adventurer_mask = pygame.mask.from_surface(self.image)
            self.mask = self.adventurer_mask.to_surface(unsetcolor=(0, 0, 0, 0))
            if self.slide:
                self.slide_vel -= 0.8
                self.sprite_index += 0.3
            if self.slide_vel < -SLIDE_VEL:
                self.slide = False
                self.slide_vel = SLIDE_VEL
                self.sprite_index = 0

    def adventurer_attack(self):
        self.image = ADVENTURER_ATTACK[int(self.sprite_index) % len(ADVENTURER_ATTACK)].convert_alpha()
        self.adventurer_mask = pygame.mask.from_surface(self.image)
        self.mask = self.adventurer_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        self.rect.x = ADVENTURER_X
        self.rect.y = ADVENTURER_Y
        if self.attack:
            self.sprite_index += 0.3
            self.attack_vel -= 0.8
        if self.attack_vel < -ATTACK_VEL:
            self.attack = False
            self.attack_vel = ATTACK_VEL
            self.sprite_index = 0

    def air_attack(self):
        if self.rect.y < ADVENTURER_Y:
            self.image = ADVENTURER_AIR_ATTACK[int(self.sprite_index) % len(ADVENTURER_AIR_ATTACK)]
            self.adventurer_mask = pygame.mask.from_surface(self.image)
            self.mask = self.adventurer_mask.to_surface(unsetcolor=(0, 0, 0, 0))
            self.rect.y -= self.jump_vel
            self.jump_vel -= 2
            self.sprite_index += 0.3
        else:
            self.jump_vel = JUMP_VEL
            self.rect.y = ADVENTURER_Y
            self.jump = False
            self.attack = False
            self.air_attack_vel = AIR_ATTACK_VEL
            self.sprite_index = 0

    def reset_adventurer(self):
        self.image = ADVENTURER_IDLE[0].convert_alpha()
        self.rect = self.image.get_rect()
        self.adventurer_mask = pygame.mask.from_surface(self.image)
        self.mask = self.adventurer_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        self.rect.x = ADVENTURER_X
        self.rect.y = ADVENTURER_Y
        self.jump_vel = JUMP_VEL
        self.slide_vel = SLIDE_VEL
        self.attack_vel = ATTACK_VEL
        self.air_attack_vel = AIR_ATTACK_VEL
        self.sprite_index = 0
        self.run = False
        self.jump = False
        self.slide = False
        self.attack = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
