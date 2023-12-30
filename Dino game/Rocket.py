import random
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (105, 55, 55)
FLOOR_HEIGHT = 600
OFFSET = 10


class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/Rockets/Rocket_001.png').convert_alpha()
        scale = 3
        self.image = pygame.transform.scale(self.image, (32 * scale, 16 * scale))
        self.image = pygame.transform.rotate(self.image, 90)
        # Start the rocket at a random x position at the top of the screen
        self.rect = self.image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH), -100))
        self.gravity = 0
        self.hit = False  # Add this line

    def apply_gravity(self):
        self.gravity += 0.5  # Adjust gravity for a more realistic fall
        self.rect.y += self.gravity
        if self.rect.y > FLOOR_HEIGHT - 85:
            self.kill()  # Remove the rocket if it goes off the bottom of the screen

    def update(self):
        self.apply_gravity()
