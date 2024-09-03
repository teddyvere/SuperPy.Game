import os
import random
import sys
import numpy as np
import pygame
import scipy
from . Config import BACKGROUND_WIDTH, FPS, GREEN, RED, WHITE, SCREEN_HEIGHT, SCREEN_WIDTH
from . Sprites import Score, Player, Zombie, Coin, Platform

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Py.Man")

og_background_image = pygame.image.load('Game/static/images/background.png')
background_image = pygame.transform.scale(og_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
highscore_file = "highscores.txt"  # File to store high scores


font = pygame.font.SysFont(None, 55)

class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.background_offset = 0
        self.show_menu = True  # Flag to show the menu
        self.score = Score(10,10)
        self.coins_collected = 0
        self.highscores = self.load_highscores()


        # Create player object
        self.player = Player(100, SCREEN_HEIGHT - 70)
        
        # Create a list of random zombies
        self.zombies = self.create_random_zombies()
        
        # Create a list of platforms
        self.platforms = self.create_random_platforms()
        
        # Create a list of coins
        self.coins = self.create_random_coins()

        # Group for all sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.score)
        self.all_sprites.add(self.player)
        # Add all zombies to the sprite group
        for zombie in self.zombies:
            self.all_sprites.add(zombie)
        # Add all platforms to the sprite group
        for platform in self.platforms:
            self.all_sprites.add(platform)
        # Add all coins to the sprite group
        for coin in self.coins:
            self.all_sprites.add(coin)

        self.backgrounds = [background_image.copy(), background_image.copy()]
        self.background_x = [0, SCREEN_WIDTH]  # Positions of the two backgrounds
    
    def create_random_zombies(self):
        num_zombies = random.randint(5, 15)  # Randomly decide the number of zombies between 5 and 15
        zombies = []
        for _ in range(num_zombies):
            x_pos = random.randint(400, SCREEN_WIDTH * 2)  # Random x position within a range
            zombie = Zombie(x_pos, SCREEN_HEIGHT - 70)
            zombies.append(zombie)
        return zombies
    
    def create_random_platforms(self):
        num_platforms = random.randint(5, 10)  # Randomly decide the number of platforms
        platforms = []
        for _ in range(num_platforms):
            x_pos = random.randint(100, SCREEN_WIDTH * 3)
            y_pos = random.randint(SCREEN_HEIGHT -300, SCREEN_HEIGHT -100)  # Random y position within a range
            width = random.randint(100, 200)  # Random platform width
            platform = Platform(x_pos, y_pos, width, 20)
            platforms.append(platform)
        return platforms
    
    def create_random_coins(self):
        num_coints = random.randint(10, 20)  # Randomly decide the number of
        coins = []
        for _ in range(num_coints):
            x_pos = random.randint(200, SCREEN_WIDTH * 3)  # Random x position within a range
            y_pos = random.randint(SCREEN_HEIGHT- 350, SCREEN_HEIGHT - 150)  # Random y position within a range
            coin = Coin(x_pos, y_pos)
            coins.append(coin)
        return coins
    
    def load_highscores(self):
        if os.path.exists(highscore_file):
            with open(highscore_file, "r") as f:
                highscores = [line.strip().split(",") for line in f.readlines()]
                highscores = [(name, int(score)) for name, score in highscores]
        else:
            highscores = []
        return highscores

    def save_highscores(self):
        with open(highscore_file, "w") as f:
            for name, score in self.highscores:
                f.write(f"{name},{score}\n")

    def check_for_highscore(self):
        if len(self.highscores) < 10 or self.score.score > self.highscores[-1][1]:
            return True
        return False

    def add_highscore(self):
        if self.check_for_highscore():
            self.display_highscore_input()

    def display_highscore_input(self):
        input_active = True
        player_name = ""
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    input_active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
            
            # Display the input prompt
            self.screen.fill(WHITE)
            prompt = font.render("Enter your name:", True, GREEN)
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(prompt, prompt_rect)
            
            name_surface = font.render(player_name, True, GREEN)
            name_rect = name_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(name_surface, name_rect)
            
            pygame.display.flip()

        # Add the new high score and sort the list
        self.highscores.append((player_name, self.score.score))
        self.highscores.sort(key=lambda x: x[1], reverse=True)
        self.highscores = self.highscores[:10]  # Keep only the top 10 scores
        self.save_highscores()
        

    def run(self):
        while self.running:
            if self.show_menu:
                self.display_menu()
            else:
                self.events()
                self.update()
                self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
        
    def display_menu(self):
        # Blur the background
        surface_array = pygame.surfarray.array3d(self.screen)

        # Apply a blur effect
        blurred_array = scipy.ndimage.gaussian_filter(surface_array, sigma=(5, 5, 0))

        # Convert back to pygame surface and draw
        blurred_surface = pygame.surfarray.make_surface(np.transpose(blurred_array, (1, 0, 2)))
        self.screen.blit(blurred_surface, (0, 0))

        # Render the game title
        title_font = pygame.font.Font(None, 74)  # You can adjust the size and font
        title = title_font.render("URBAN ZOMBIE WARRIOR", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))  # Adjust position as needed
        self.screen.blit(title, title_rect)

        # Render play button
        play_button = font.render("PRESS ENTER TO CONTINUE", True, WHITE)
        button_rect = play_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(play_button, button_rect)

        # Update the display
        pygame.display.flip()

        # Wait for user interaction
        self.wait_for_menu_input()
    
    def display_highscores(self):
        highscore_font = pygame.font.Font(None, 36)
        title = highscore_font.render("High Scores", True, WHITE)
        self.screen.blit(title, (50, 50))

        for i, (name, score) in enumerate(self.highscores):
            score_text = f"{i+1}. {name} - {score}"
            score_surface = highscore_font.render(score_text, True, WHITE)
            self.screen.blit(score_surface, (50, 100 + i * 30))

    def wait_for_menu_input(self):
        while self.show_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.show_menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Press Enter to start the game
                        self.show_menu = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Prepare a list to store zombies to remove
        zombies_to_remove = []

        # Update zombies and check for collisions
        player_died = False
        for zombie in self.zombies:
            zombie.update()  # Update each zombie's position

            # Check for collisions only with alive zombies
            if pygame.sprite.collide_rect(self.player, zombie):
                if (self.player.rect.bottom <= zombie.rect.top + 10 and self.player.velocity.y > 0):
                    # Mark zombie for removal if the player lands on it
                    zombies_to_remove.append(zombie)
                    self.score.increase_score(100)  # Increase the score by 100
                    self.player.velocity.y = self.player.jump_speed  # Bounce the player up
                else:
                    # Player collided with the side of the zombie
                    player_died = True

        # Remove zombies that have been marked for removal
        for zombie in zombies_to_remove:
            self.all_sprites.remove(zombie)
            self.zombies.remove(zombie)
            zombie.kill()
        
        

        #
            
        # Adds new zombies if score is high enough
        if self.coins_collected > 3:
            self.zombies.append(Zombie(random.randint(100, 500), 10))
            self.coins_collected -= 3  # Decrease the score by 100 when new zombies are added

        

        # Only update player position if they are still alive
        if not player_died:
            self.player.update(keys)

        if player_died:
            self.display_death_message()
            self.running = False  # End the game when the player dies
            
        # Check for collision with platforms   
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity.y > 0 and self.player.rect.bottom <= platform.rect.bottom:
                    self.player.velocity.y = 0
                    self.player.on_ground = True
                    self.player.rect.bottom = platform.rect.top
        
        # CHeck for collision with coins
        for coin in self.coins:
            coin.animate()
            if pygame.sprite.collide_rect(self.player, coin):
                coin.kill()  # Remove the coin when the player collects it
                self.coins.remove(coin) # Removes coins from listd
                self.coins_collected += 1  # Increase the coins collected
                self.score.increase_score(100)  # Increase the score by 10 when a coin is

        # Check if all coins have been collected
        if len(self.coins) == 0:
            self.display_win_message()
            self.running = False  # End the game when all coins have been collected
        
        

        # Determine if player needs to scroll
        # If the player has reached certain bounds near the edges of the screen
        scroll_speed = self.player.velocity.x  # Use the player's current speed for scrolling
        if self.player.rect.right > 600 and keys[pygame.K_d]:
            self.background_offset -= scroll_speed

            # Prevent player from scrolling past the edges
            self.player.rect.right = 600
        elif self.player.rect.left < 200 and keys[pygame.K_a]:
            self.background_offset += scroll_speed
            self.player.rect.left = 200

        # Update each sprite's position based on the background offset
        for zombie in self.zombies:
            if zombie.alive():
                zombie.rect.x -= scroll_speed  # Move zombies in the opposite direction of the player scroll

        # Prevent scrolling beyond the background image
        self.background_offset = max(-SCREEN_WIDTH, min(0, self.background_offset))

        # Update background positions based on player movement
        for i in range(len(self.background_x)):
            self.background_x[i] -= scroll_speed  # Move background opposite to player

            # Move platforms with the background
            for platform in self.platforms:
                platform.rect.x -= scroll_speed
                
            # Move coins with the background
            for coin in self.coins:
                coin.rect.x -= scroll_speed


            # Reset the background position when it goes off screen
            if self.background_x[i] < -BACKGROUND_WIDTH:
                self.background_x[i] += BACKGROUND_WIDTH * 2
            elif self.background_x[i] > BACKGROUND_WIDTH:
                self.background_x[i] -= BACKGROUND_WIDTH * 2
        



    def draw(self):
        self.screen.fill(WHITE)
        for bg in self.background_x:
            self.screen.blit(background_image, (bg, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        

    def display_death_message(self):
        # Capture the screen
        surface_array = pygame.surfarray.array3d(self.screen)
        surface_array = np.transpose(surface_array, (1, 0, 2))

        # Apply a blur effect
        blurred_array = scipy.ndimage.gaussian_filter(surface_array, sigma=(5, 5, 0))

        # Convert back to pygame surface and draw
        blurred_surface = pygame.surfarray.make_surface(np.transpose(blurred_array, (1, 0, 2)))
        self.screen.blit(blurred_surface, (0, 0))

        # Render death messaged
        death_message = font.render(f"WASTED Score:{self.score.score}", True, RED)
        death_rect = death_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(death_message, death_rect)
        pygame.display.flip()

        pygame.time.wait(5000)  # Display the message for 2 seconds
        
    def display_win_message(self):
        # Capture the screen
        surface_array = pygame.surfarray.array3d(self.screen)
        surface_array = np.transpose(surface_array, (1, 0, 2))

        # Apply a blur effect
        blurred_array = scipy.ndimage.gaussian_filter(surface_array, sigma=(5, 5, 0))

        # Convert back to pygame surface and draw
        blurred_surface = pygame.surfarray.make_surface(np.transpose(blurred_array, (1, 0, 2)))
        self.screen.blit(blurred_surface, (0, 0))

        # Render win message
        win_message = font.render(f"YOU WIN Score:{self.score.score}", True, GREEN)
        win_rect = win_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(win_message, win_rect)
        pygame.display.flip()
        
        pygame.time.wait(5000)  # Display the message for 2 seconds