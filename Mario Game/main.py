import pygame
import sys
import numpy as np
import scipy.ndimage

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
BACKGROUND_WIDTH = SCREEN_WIDTH

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Py.Man")

# Load assets
mario_image = pygame.image.load('images/mario.png')
zombie1_image = pygame.image.load('images/zombie1.png')
og_background_image = pygame.image.load('images/background.png')
background_image = pygame.transform.scale(og_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonts
font = pygame.font.SysFont(None, 55)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(mario_image, (32, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 2.5
        self.jump_speed = -15
        self.gravity = 1
        self.jump_gravity = 1
        self.fall_gravity = 0.25
        self.on_ground = True
        self.jump_pressed = False  # Flag to avoid holding jump

    def update(self, keys):
        # Handle horizontal movement
        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
        elif keys[pygame.K_d]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
        
        # Handle jump
        if self.on_ground and keys[pygame.K_w]:
            self.velocity.y = self.jump_speed
            self.on_ground = False  # Now in the air

        # Apply gravity
        if self.velocity.y < 0:
            self.velocity.y += self.jump_gravity
        else:
            self.velocity.y += self.fall_gravity

        # Update player position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        # Check for ground collision
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity.y = 0
            self.on_ground = True

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(zombie1_image, (32, 70))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = 2.5  # Speed of the zombie
        self.move_direction = 1
        self.boundary_left = x - 100  # Left boundary
        self.boundary_right = x + 100  # Right boundary
    
    def update(self):
        # Move back and forth
        self.rect.x += self.velocity * self.move_direction

        # Reverse direction if hitting boundaries
        if self.rect.x <= self.boundary_left or self.rect.x >= self.boundary_right:
            self.move_direction *= -1  # Reverse direction    

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((128, 128, 128))  # Fill with gray color
        # Draw black border
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 3)  # 3 pixels for the border width
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.background_offset = 0
        self.show_menu = True  # Flag to show the menu

        # Create game objects
        self.player = Player(100, SCREEN_HEIGHT - 70)
        self.zombie1 = Zombie(400, SCREEN_HEIGHT - 70)
        self.zombie2 = Zombie(800, SCREEN_HEIGHT - 70)
        self.zombie3 = Zombie(1200, SCREEN_HEIGHT - 70)
        
        # Create platforms
        self.platform1 = Platform(300, SCREEN_HEIGHT - 100, 150, 20)
        self.platform2 = Platform(1100, SCREEN_HEIGHT - 150, 200, 20)
        self.platform3 = Platform(1900, SCREEN_HEIGHT - 100, 150, 20)
        self.platform4 = Platform(2700, SCREEN_HEIGHT - 150, 200, 20)
        self.platform5 = Platform(3500, SCREEN_HEIGHT - 100, 150, 20)

        # Group for all sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.zombie1)
        self.all_sprites.add(self.zombie2)
        self.all_sprites.add(self.zombie3)
        self.all_sprites.add(self.platform1)
        self.all_sprites.add(self.platform2)
        self.all_sprites.add(self.platform3)
        self.all_sprites.add(self.platform4)
        self.all_sprites.add(self.platform5)

        self.backgrounds = [background_image.copy(), background_image.copy()]
        self.background_x = [0, SCREEN_WIDTH + 200]  # Positions of the two backgrounds

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
        title = title_font.render("GTA 6", True, WHITE)
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
        
        self.player.update(keys)
        self.zombie1.update()
        self.zombie2.update()
        self.zombie3.update()
        
        # Check for collisions
        player_died = False
        for zombie in [self.zombie1, self.zombie2, self.zombie3]:
            if pygame.sprite.collide_rect(self.player, zombie):
                if (self.player.rect.bottom <= zombie.rect.top + 10 and self.player.velocity.y > 0):
                    # Remove zombie if player lands on it
                    self.all_sprites.remove(zombie)
                    zombie.kill()
                    self.player.velocity.y = self.player.jump_speed  # Bounce the player up
                elif (self.player.rect.right >= zombie.rect.left + 5 and self.player.rect.left <= zombie.rect.right - 5):
                    player_died = True  # Player collided with the side of the zombie
        
        if player_died:
            self.display_death_message()
            self.running = False  # End the game when the player dies
                
        # Check for collision with platforms
        for platform in [self.platform1, self.platform2, self.platform3, self.platform4, self.platform5]:
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity.y > 0 and self.player.rect.bottom <= platform.rect.bottom:
                    self.player.velocity.y = 0
                    self.player.on_ground = True
                    self.player.rect.bottom = platform.rect.top
        
        # Update background offset if the player is in the middle of the screen
        if self.player.rect.right > 600 and keys[pygame.K_d]:
            self.background_offset -= self.player.speed
            self.player.rect.right = 600
        elif self.player.rect.left < 200 and keys[pygame.K_a]:
            self.background_offset += self.player.speed
            self.player.rect.left = 200

        # Prevent scrolling beyond the background image
        self.background_offset = max(-SCREEN_WIDTH, min(0, self.background_offset))

        # Update background positions based on player movement
        for i in range(len(self.background_x)):
            self.background_x[i] -= self.player.velocity.x  # Move background opposite to player

            # Move platforms and zombies with the background
            for platform in [self.platform1, self.platform2, self.platform3, self.platform4, self.platform5]:
                platform.rect.x -= self.player.velocity.x
            for zombie in [self.zombie1, self.zombie2, self.zombie3]:
                zombie.rect.x -= self.player.velocity.x 

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

        # Render death message
        death_message = font.render("WASTED", True, RED)
        death_rect = death_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(death_message, death_rect)
        pygame.display.flip()

        pygame.time.wait(10000)  # Display the message for 2 seconds

if __name__ == "__main__":
    game = Game()
    game.run()
