import random
import sys
import numpy as np
import pygame
import scipy
from . __init__ import BACKGROUND_WIDTH, FPS, GREEN, RED, WHITE, SCREEN_HEIGHT, SCREEN_WIDTH
from . Sprites import Score, Player, Zombie, Coin, Platform

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Py.Man")

og_background_image = pygame.image.load('Game/static/images/background.png')
background_image = pygame.transform.scale(og_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

        # Create player object
        self.player = Player(100, SCREEN_HEIGHT - 70)
        
        # Create a list of zombies
        self.zombies = [
            Zombie(400, SCREEN_HEIGHT - 70),
            Zombie(500, SCREEN_HEIGHT - 70),
            Zombie(550, SCREEN_HEIGHT - 70),
            Zombie(575, SCREEN_HEIGHT - 70),
            Zombie(600, SCREEN_HEIGHT - 70),
            Zombie(800, SCREEN_HEIGHT - 70),
            Zombie(1000, SCREEN_HEIGHT - 70),
            Zombie(1200, SCREEN_HEIGHT - 70),
            Zombie(1400, SCREEN_HEIGHT - 70),
            Zombie(1600, SCREEN_HEIGHT - 70),
            Zombie(1800, SCREEN_HEIGHT - 70)
        ]
        
        # Create a list of platforms
        self.platforms = [
            Platform(100, SCREEN_HEIGHT - 100, 150, 20),
            Platform(500, SCREEN_HEIGHT - 100, 150, 20),
            Platform(900, SCREEN_HEIGHT - 100, 150, 20),
            Platform(1300, SCREEN_HEIGHT - 100, 150, 20),
            Platform(1700, SCREEN_HEIGHT - 100, 150, 20),
            Platform(1900, SCREEN_HEIGHT - 150, 200, 20),
            Platform(2100, SCREEN_HEIGHT - 200, 150, 20),
            Platform(2300, SCREEN_HEIGHT - 250, 150, 20),
            Platform(2500, SCREEN_HEIGHT - 300, 150, 20),
        ]
        
        # Create a list of coins
        self.coins = [
            Coin(200, SCREEN_HEIGHT - 150),
            Coin(300, SCREEN_HEIGHT - 200),
            Coin(500, SCREEN_HEIGHT - 50),
            Coin(700, SCREEN_HEIGHT - 100),
            Coin(900, SCREEN_HEIGHT - 150),
            Coin(1100, SCREEN_HEIGHT - 200),
            Coin(1300, SCREEN_HEIGHT - 50),
            Coin(1500, SCREEN_HEIGHT - 100),
            Coin(1700, SCREEN_HEIGHT - 150),
            Coin(1900, SCREEN_HEIGHT - 200),
            Coin(2100, SCREEN_HEIGHT - 50),
            Coin(2300, SCREEN_HEIGHT - 100),
            Coin(2500, SCREEN_HEIGHT - 150),
        ]

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