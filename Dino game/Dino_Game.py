import pygame
from sys import exit
from Animate_Sprites import SpriteSheet, Animation, Animation2
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (105, 55, 55)
FLOOR_HEIGHT = 600
OFFSET = 10
game_active = False


def test_function():
    print("Button clicked!")


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


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BACKGROUND_COLOR = BACKGROUND_COLOR
        self.FLOOR_HEIGHT = FLOOR_HEIGHT
        self.game_active = game_active
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Dino Rocket Drop")
        self.score = 0
        self.obstacle_time = 1200
        self.missile_spawn_rate = 10000
        self.last_multiple_of_5 = 0
        self.last_score_checkpoint = 0
        self.load_assets()
        self.setup()
        self.main_loop()

    def start_game(self):
        self.player.game_start_time = pygame.time.get_ticks()
        self.game_active = True
        self.player.game_active = True
        self.start_time = pygame.time.get_ticks() // 1000
        self.player.rect.midbottom = (80, self.FLOOR_HEIGHT)
        self.obstacle_group.empty()
        self.missile_group.empty()
        self.player.lives = 3
        self.player.invulnerable = False
        # Reset the game as needed
        self.reset_game()

    def load_assets(self):
        self.image_list = [pygame.image.load('sheets/DinoSprites - mort.png').convert_alpha(),
                           pygame.image.load('sheets/DinoSprites - doux.png').convert_alpha(),
                           pygame.image.load('sheets/DinoSprites - tard.png').convert_alpha(),
                           pygame.image.load('sheets/DinoSprites - vita.png').convert_alpha()]
        self.image_choice = random.choice(self.image_list)
        self.sheet_image = self.image_choice
        self.bg_music = pygame.mixer.Sound('audio/david deals with devils.wav')
        self.bg_music.set_volume(0.1)
        self.bg_music.play(loops=-1)
        self.test_font = pygame.font.Font('font/gomarice_no_continue.ttf', 50)
        self.background_image = pygame.image.load('graphics/Space Background.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.floor = pygame.image.load('graphics/game_floor.png')
        self.floor = pygame.transform.scale(self.floor, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT - self.FLOOR_HEIGHT))
        self.powerup_sheet_image = pygame.image.load('sheets/BlueCrystal.png').convert_alpha()

    def setup(self):
        # Choose a random sprite sheet for the player
        self.image_choice = random.choice(self.image_list)
        # Initialize the player with the selected sprite sheet
        self.player = Player(self.image_choice)
        self.player_sprites = pygame.sprite.GroupSingle(self.player)

        # Initialize other game components like obstacle group, missile group, etc.
        self.obstacle_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        # Setup timers and other initial game settings
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, self.obstacle_time)
        self.powerup_spawn_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.powerup_spawn_timer, 5000)  # 5 seconds
        self.missile_timer = pygame.USEREVENT + 3
        self.missiles_started = False

        # Load the button sprite sheet
        self.button_sprite_sheet = pygame.image.load('sheets/Silver.png')

        # Inside Game class setup method
        self.start_button = Button(self.SCREEN_WIDTH / 2, (self.SCREEN_HEIGHT / 2) + 100, self.button_sprite_sheet,
                                   self.start_game, 'Start', 2, 6,
                                   'font/gomarice_no_continue.ttf', 20, (0, 0, 0))

    def display_powerups(self):
        # Display the current number of powerups under the score
        powerup_text = self.test_font.render(f'Powerups: {self.player.circle_uses_left}', False, (255, 255, 255))
        powerup_rect = powerup_text.get_rect(topleft=(20, 80))
        self.screen.blit(powerup_text, powerup_rect)

    def display_score(self):
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        score_surf = self.test_font.render(f'Score: {current_time}', False, (56, 1, 1))
        score_rect = score_surf.get_rect(topleft=(20, 20))
        self.screen.blit(score_surf, score_rect)
        return current_time

    def display_menu(self):
        menu_text = self.test_font.render('Click Start to Play', True, (BACKGROUND_COLOR))
        menu_rect = menu_text.get_rect(center=(self.SCREEN_WIDTH / 2, (self.SCREEN_HEIGHT / 2)))

        highscore = self.get_highscore()
        highscore_text = self.test_font.render(f'High Score: {highscore}', True, (BACKGROUND_COLOR))
        highscore_rect = highscore_text.get_rect(center=(self.SCREEN_WIDTH / 2, (self.SCREEN_HEIGHT / 2) + 300))

        self.screen.fill((26, 15, 28))  # Fill the screen with the menu color
        self.screen.blit(menu_text, menu_rect)  # Draw the menu text
        self.screen.blit(highscore_text, highscore_rect)  # Draw the high score text
        # Update and draw the start button
        self.start_button.update()
        self.screen.blit(self.start_button.image, self.start_button.rect.topleft)

    def display_lives(self):
        lives_text = self.test_font.render(f'Lives: {self.player.lives}', False, (255, 255, 255))
        lives_rect = lives_text.get_rect(topright=(self.SCREEN_WIDTH - 20, 20))
        self.screen.blit(lives_text, lives_rect)

    def reset_game(self):
        # Resetting the obstacle time and score
        self.obstacle_time = 1200
        self.missile_spawn_rate = 10000
        pygame.time.set_timer(self.obstacle_timer, self.obstacle_time)
        self.last_multiple_of_5 = 0
        self.last_score_checkpoint = 0
        self.score = 0
        self.game_active = True

        # Choose a new random sprite sheet for the player
        self.image_choice = random.choice(self.image_list)
        # Reinitialize the player with the new sprite sheet
        self.player = Player(self.image_choice)
        self.player_sprites = pygame.sprite.GroupSingle(self.player)

        # Resetting the player's state
        self.player.game_active = True
        self.player.circle_uses_left = 3
        self.player.lives = 3
        self.player.invulnerable = False

        # Emptying existing groups and resetting timers as needed
        self.obstacle_group.empty()
        self.missile_group.empty()
        self.powerup_group.empty()
        self.missiles_started = False

        # Any additional resetting needed for the game...

    def check_collisions(self):
        # Check for collision with rockets
        if pygame.sprite.spritecollide(self.player, self.obstacle_group, True) and not self.player.invulnerable:
            self.player.take_damage()
            # Additional logic if needed when rockets collide with player

        # Check for collision with missiles
        if pygame.sprite.spritecollide(self.player, self.missile_group, True) and not self.player.invulnerable:
            self.player.take_damage()
            # Additional logic if needed when missiles collide with player

        if self.player.lives <= 0:
            final_score = int(pygame.time.get_ticks() / 1000) - self.start_time  # Calculate final score
            new_highscore = self.highscore(final_score)  # Update high score
            print(f"Final Score: {final_score}, New High Score: {new_highscore}")  # Debug print
            self.game_active = False

    def spawn_powerup(self):
        new_powerup = PowerUp(self.powerup_sheet_image)
        self.powerup_group.add(new_powerup)

    def check_powerup_collisions(self):
        # Check if the player has collected any powerups
        if pygame.sprite.spritecollide(self.player, self.powerup_group, True):
            self.player.circle_uses_left += 1  # Increase the circle uses

    def check_circle_collisions(self):
        if self.player.circle_active:
            # Check for collision with rockets
            for rocket in self.obstacle_group.sprites():
                distance = pygame.math.Vector2(rocket.rect.center) - pygame.math.Vector2(self.player.rect.center)
                if distance.length() < self.player.circle_radius:
                    rocket.kill()  # Remove the rocket if it touches the circle

            # Check for collision with missiles
            for missile in self.missile_group.sprites():
                distance = pygame.math.Vector2(missile.rect.center) - pygame.math.Vector2(self.player.rect.center)
                if distance.length() < self.player.circle_radius:
                    missile.kill()  # Remove the missile if it touches the circle

    def highscore(self, current_score):
        highscore_file = 'highscore.txt'

        try:
            with open(highscore_file, 'r') as file:
                highscore = int(file.read())
                print(f"Read High Score: {highscore}")  # Debug print
        except FileNotFoundError:
            highscore = 0
            print("High Score File Not Found. Setting High Score to 0")  # Debug print
        except ValueError:
            highscore = 0
            print("Value Error. Setting High Score to 0")  # Debug print

        if current_score > highscore:
            with open(highscore_file, 'w') as file:
                file.write(str(current_score))
                print(f"New High Score Written: {current_score}")  # Debug print
            return current_score
        return highscore

    def get_highscore(self):
        highscore_file = 'highscore.txt'
        try:
            with open(highscore_file, 'r') as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

                # Handle button click in the menu
            if not self.game_active:
                self.start_button.update()

            if event.type == self.obstacle_timer and self.game_active:
                self.obstacle_group.add(Rocket())

            if event.type == self.missile_timer and self.game_active:
                self.missile_group.add(Missile())

            if event.type == self.powerup_spawn_timer and self.game_active:
                self.spawn_powerup()  # Spawn a new powerup

            if event.type == pygame.KEYDOWN and not self.game_active:
                if event.key == pygame.K_RETURN:  # Check if the Enter key is pressed
                    self.game_active = True
                    self.player.game_active = True  # Ensure this is updated as well
                    self.start_time = pygame.time.get_ticks() // 1000
                    self.player.rect.midbottom = (80, self.FLOOR_HEIGHT)
                    self.obstacle_group.empty()
                    self.missile_group.empty()
                    self.player.lives = 3
                    self.player.invulnerable = False
                    self.reset_game()  # Reset the game here

    def update_game(self):
        self.player_sprites.update()
        self.obstacle_group.update()
        self.score = self.display_score()
        self.display_lives()
        self.display_powerups()

        # Check if the score has reached the next multiple of 5 since the last adjustment
        if self.score // 5 > self.last_score_checkpoint:
            self.last_score_checkpoint = self.score // 5
            self.obstacle_time = max(self.obstacle_time - 100, 10)  # Decrease timer, but set a minimum limit
            pygame.time.set_timer(self.obstacle_timer, self.obstacle_time)  # Reset the timer with the new interval

        # Check if the obstacle time has reached its minimum limit
        if self.obstacle_time == 10:
            self.obstacle_time = 1200  # Reset to initial value or another value as per game design
            pygame.time.set_timer(self.obstacle_timer, self.obstacle_time)  # Reset the timer with the new interval

        # Check for rocket-circle collisions
        self.check_circle_collisions()

        # Ensure missiles are being updated
        self.missile_group.update()

        self.check_powerup_collisions()
        self.powerup_group.update()  # Update the power-ups

        # Start spawning missiles after the score reaches 60
        if int(self.score) >= 55 and not self.missiles_started:
            pygame.time.set_timer(self.missile_timer, self.missile_spawn_rate)
            self.missiles_started = True

    def draw_game(self):
        self.player_sprites.draw(self.screen)
        self.obstacle_group.draw(self.screen)
        pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect, 1)  # Draw player collision box
        if self.player.circle_active:
            pygame.draw.circle(self.screen, (255, 255, 255), self.player.rect.center, self.player.circle_radius, 1)
        self.powerup_group.draw(self.screen)
        # Draw missiles
        self.missile_group.draw(self.screen)

    def main_loop(self):
        while True:
            self.handle_events()  # Process input and events

            # Always fill the screen with the background color to avoid any artifacts
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.floor, (0, self.SCREEN_HEIGHT - self.floor.get_height()))

            if self.game_active:
                self.update_game()  # Update game objects and UI
                self.check_collisions()  # Check for collisions between player and obstacles
                self.draw_game()  # Draw the game objects

                # Ensure the score and lives are drawn on top of the game scene
                self.display_score()
                self.display_lives()

            else:
                self.display_menu()  # Display the main menu when the game is not active
            # The display should be updated once after all drawing operations

            pygame.display.update()
            self.clock.tick(60)  # Maintain the game's frame rate


if __name__ == "__main__":
    print("Starting the game")  # This should print when the game is about to start
    Game()
