import random
import pygame
from Animate_Sprites import SpriteSheet, Animation2

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (105, 55, 55)
FLOOR_HEIGHT = 600
OFFSET = 10
game_active = False


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_image):  # Accept the sprite sheet image as an argument
        super().__init__()
        # Load the sprite sheet for the Blue Crystal power-up
        self.sprite_sheet = SpriteSheet(sprite_sheet_image)

        # The Blue Crystal has 8 frames in its animation
        powerup_animation_frame_count = [8]

        # Initialize the animation
        self.powerup_animation = Animation2(self.sprite_sheet, powerup_animation_frame_count)

        # Set the initial image and rect
        self.image = self.powerup_animation.animation_list[0][0]

        # Assuming the power-up should appear above the floor, adjust the y-coordinate
        powerup_height = self.image.get_height()
        floor_y_position = FLOOR_HEIGHT - powerup_height  # Adjust so the bottom of the power-up is on the floor

        # Set the rect with random x position and y position at the floor
        self.rect = self.image.get_rect(midbottom=(random.randint(0, SCREEN_WIDTH), floor_y_position))

    def update(self):
        # Update the animation - the attribute name should match the initialization
        self.powerup_animation.update()
        self.image = self.powerup_animation.animation_list[self.powerup_animation.action][
            self.powerup_animation.animation_frame]
