import random
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (105, 55, 55)
FLOOR_HEIGHT = 600
OFFSET = 10


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/Rockets/Rocket_005.png').convert_alpha()
        scale = 2.5
        self.image = pygame.transform.scale(self.image, (32 * scale, 16 * scale))
        # Start the rocket at a random x position at the top of the screen
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH, random.randint(FLOOR_HEIGHT - 100, FLOOR_HEIGHT)))
        self.hit = False  # Add this line

    def fly(self):
        self.rect.x -= 15
        if self.rect.x < 0:
            self.kill()  # Remove the rocket if it goes off the bottom of the screen

    def update(self):
        self.fly()
