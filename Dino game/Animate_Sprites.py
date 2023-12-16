import pygame


class SpriteSheet:
    # Initialization of the SpriteSheet class
    def __init__(self, sprite_sheet_image):
        self.sprite_sheet = sprite_sheet_image

    # Method to extract a specific image from the sprite sheet
    def get_image(self, frame, width, height, scale, colour):
        # Create a new surface for the image
        image = pygame.Surface((width, height)).convert_alpha()
        # Blit a portion of the sprite sheet onto this surface
        image.blit(self.sprite_sheet, (0, 0), ((frame * width), 0, width, height))
        # Scale the image if necessary
        image = pygame.transform.scale(image, (width * scale, height * scale))
        # Set a color key for transparency
        image.set_colorkey(colour)
        return image


class Animation:
    # Initialize the Animation class with parameters for animation steps and frame counts
    def __init__(self, sprite_sheet, animation_steps, sprite_x, sprite_y):
        self.sprite_sheet = sprite_sheet
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.animation_list = []  # List to store animation frames
        self.animation_steps = animation_steps  # Number of frames in each animation (passed as a parameter)
        self.action = 0  # Current action/animation index
        self.last_update = pygame.time.get_ticks()  # Time of the last update
        self.animation_cooldown = 120  # Cooldown time between frame updates
        self.animation_frame = 0  # Current frame of the animation
        self.load_animations()  # Load animations

    # Load the animations from the sprite sheet
    def load_animations(self):
        step_counter = 0
        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                # Extract each frame from the sprite sheet
                temp_img_list.append(self.sprite_sheet.get_image(step_counter, self.sprite_x, self.sprite_y, 3, 'BLACK'))
                step_counter += 1
            self.animation_list.append(temp_img_list)

    # Update the animation frames based on the cooldown
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.animation_frame += 1
            self.last_update = current_time
            if self.animation_frame >= len(self.animation_list[self.action]):
                self.animation_frame = 0

    # Draw the current frame of the animation
    def draw(self, surface):
        surface.blit(self.animation_list[self.action][self.animation_frame], (0, 0))

    # Change the current action/animation
    def change_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.animation_frame = 0

class Animation2:
    # Initialize the Animation class with parameters for animation steps and frame counts
    def __init__(self, sprite_sheet, animation_steps):
        self.sprite_sheet = sprite_sheet
        self.animation_list = []  # List to store animation frames
        self.animation_steps = animation_steps  # Number of frames in each animation (passed as a parameter)
        self.action = 0  # Current action/animation index
        self.last_update = pygame.time.get_ticks()  # Time of the last update
        self.animation_cooldown = 120  # Cooldown time between frame updates
        self.animation_frame = 0  # Current frame of the animation
        self.load_animations()  # Load animations

    # Load the animations from the sprite sheet
    def load_animations(self):
        step_counter = 0
        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                # Extract each frame from the sprite sheet
                temp_img_list.append(self.sprite_sheet.get_image(step_counter, 16, 16, 3, 'BLACK'))
                step_counter += 1
            self.animation_list.append(temp_img_list)

    # Update the animation frames based on the cooldown
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.animation_frame += 1
            self.last_update = current_time
            if self.animation_frame >= len(self.animation_list[self.action]):
                self.animation_frame = 0

    # Draw the current frame of the animation
    def draw(self, surface):
        surface.blit(self.animation_list[self.action][self.animation_frame], (0, 0))

    # Change the current action/animation
    def change_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.animation_frame = 0

