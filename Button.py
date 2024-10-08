import pygame
from Animate_Sprites import SpriteSheet, Animation

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (105, 55, 55)
FLOOR_HEIGHT = 600
OFFSET = 10


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet_image, function, text, text_scale, button_scale, base_font_path,
                 base_font_size, text_color=(0, 0, 0)):
        super().__init__()
        self.text_offset_y = 5
        self.sprite_sheet = SpriteSheet(sprite_sheet_image)
        self.function = function
        self.text = text
        self.text_color = text_color
        self.is_clicked = False
        self.button_scale = button_scale
        self.delay = None
        self.last_click_time = 0

        # Three states: normal, clicked, hovered
        animation_frame_counts = [1, 1, 1]

        # Initialize the animation with the provided sprite sheet
        self.animation = Animation(self.sprite_sheet, animation_frame_counts, 48, 16)
        self.current_state = 0

        # Scale the button image
        self.image_original = self.animation.animation_list[self.current_state][0]
        self.image_original = pygame.transform.scale(self.image_original,
                                                     (int(48 * self.button_scale), int(16 * self.button_scale)))
        self.image = self.image_original.copy()

        self.rect = self.image.get_rect(center=(x, y))

        # Text rendering with scaling
        scaled_font_size = int(base_font_size * text_scale)
        self.font = pygame.font.Font(base_font_path, scaled_font_size)
        self.render_text()

    def render_text(self):
        # Render the text onto a separate surface
        text_surface = self.font.render(self.text, True, self.text_color)

        # Calculate the position to center the text on the button
        text_x = (self.image.get_width() - text_surface.get_width()) // 2
        text_y = ((self.image.get_height() - text_surface.get_height()) // 2) - self.text_offset_y

        # Clear the button image and then blit the text onto it
        self.image = self.image_original.copy()
        self.image.blit(text_surface, (text_x, text_y))

    def update_button_state(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Change state based on mouse position and click status
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:  # Mouse is pressed over the button
                self.current_state = 1  # Clicked state
            else:
                self.current_state = 2  # Hover state
        else:
            self.current_state = 0  # Normal state

        # Update the button image based on the current state
        self.image_original = pygame.transform.scale(self.animation.animation_list[self.current_state][0],
                                                     (int(48 * self.button_scale), int(16 * self.button_scale)))
        self.render_text()  # Re-render the text onto the updated button image

    def check_for_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            self.is_clicked = True
        else:
            self.is_clicked = False

        if self.is_clicked:
            self.function()

    def update(self):
        self.update_button_state()
        self.check_for_click()
