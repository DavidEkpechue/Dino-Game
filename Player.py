import pygame
from sys import exit
from Animate_Sprites import SpriteSheet, Animation, Animation2
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (105, 55, 55)
FLOOR_HEIGHT = 600
OFFSET = 10
class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_image):
        super().__init__()
        # Load the sprite sheet
        self.sprite_sheet = SpriteSheet(sprite_sheet_image)

        # Define the number of frames in each animation action
        animation_frame_counts = [4, 6, 3, 4, 7]

        # Initialize the animation with the provided sprite sheet
        self.animation = Animation(self.sprite_sheet, animation_frame_counts, 24, 24)

        # Set the initial image
        self.image = self.animation.animation_list[0][0]

        # Player's initial setup
        self.offset = OFFSET
        self.rect = self.image.get_rect(midbottom=(80, FLOOR_HEIGHT + self.offset))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)
        self.facing_right = True
        self.lives = 3
        self.invulnerable = False
        self.invulnerability_duration = 360
        self.invulnerability_timer = 0
        self.hurt_animation = False
        self.circle_active = False
        self.circle_radius = 0
        self.circle_duration = 300  # seconds in milliseconds
        self.circle_start_time = 0
        self.circle_uses_left = 3
        self.game_active = False

        self.game_start_time = pygame.time.get_ticks()

        # Add any additional initialization as needed

    def player_input(self):
        if self.game_active:  # Only process input if the game is active
            if not self.invulnerable:  # Only handle input if not in hurt animation
                keys = pygame.key.get_pressed()
                mods = pygame.key.get_mods()  # Get the current state of all modifier keys
                mouse_buttons = pygame.mouse.get_pressed()

                if keys[pygame.K_SPACE] and self.rect.bottom >= FLOOR_HEIGHT + self.offset:
                    self.gravity = -17
                    self.animation.change_action(2)  # Change to the jump animation

                # Check for running (Shift + A/D)
                elif keys[pygame.K_d] and mods & pygame.KMOD_SHIFT:
                    self.rect.x += 7
                    self.animation.change_action(4)  # Change to the run animation
                    self.facing_right = True
                elif keys[pygame.K_a] and mods & pygame.KMOD_SHIFT:
                    self.rect.x -= 7
                    self.animation.change_action(4)  # Change to the run animation
                    self.facing_right = False

                # Check for walking (A/D without Shift)
                elif keys[pygame.K_d]:
                    self.rect.x += 4
                    self.animation.change_action(1)  # Change to the walk animation
                    self.facing_right = True
                elif keys[pygame.K_a]:
                    self.rect.x -= 4
                    self.animation.change_action(1)  # Change to the walk animation
                    self.facing_right = False

                elif keys[pygame.K_p]:
                    self.animation.change_action(3)

                # Reset to idle animation if no movement
                else:
                    self.animation.change_action(0)  # Change to the idle animation

                if mouse_buttons[0] and not self.circle_active:  # Left mouse button is index 0
                    self.activate_circle()

                if self.rect.x > SCREEN_WIDTH:
                    self.rect.x = 0
                if self.rect.x < 0:
                    self.rect.x = SCREEN_WIDTH

    def take_damage(self):
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerability_timer = pygame.time.get_ticks()
            self.animation.change_action(3)  # Switch to the hurt animation

    def activate_circle(self):
        current_time = pygame.time.get_ticks()
        if self.circle_active is False and self.circle_uses_left > 0 and (current_time - self.game_start_time) > 1000:
            self.circle_active = True
            self.circle_radius = 0
            self.circle_start_time = current_time
            self.circle_uses_left -= 1

    def update_circle(self):
        if self.circle_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.circle_start_time < self.circle_duration:
                self.circle_radius += 22  # Increase the radius over time
            else:
                self.circle_active = False  # Deactivate the circle after 3 seconds

    def update_invulnerability(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerability_timer > self.invulnerability_duration:
                self.invulnerable = False
                self.animation.change_action(0)  # Switch back to idle or another appropriate animation

    def play_hurt_animation(self):
        while self.hurt_animation:
            self.animation.change_action(3)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= FLOOR_HEIGHT + self.offset:
            self.rect.bottom = FLOOR_HEIGHT + self.offset

    def flip(self):
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False).convert_alpha()  # Flip horizontally

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation.update()
        self.update_invulnerability()
        self.image = self.animation.animation_list[self.animation.action][self.animation.animation_frame]
        self.update_circle()
        if self.invulnerable:
            self.animation.change_action(3)  # Ensure the hurt animation is played if invulnerable

        self.flip()
