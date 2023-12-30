from Player import *
from Rocket import *
from Missile import *
from PowerUp import *
from Button import *

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (105, 55, 55)
FLOOR_HEIGHT = 600
OFFSET = 10
game_active = False


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

    def check_collisions(self):
        # Check if the player has collected any powerups
        if pygame.sprite.spritecollide(self.player, self.powerup_group, True):
            self.player.circle_uses_left += 1  # Increase the circle uses

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

        # Ensure missiles are being updated
        self.missile_group.update()

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
