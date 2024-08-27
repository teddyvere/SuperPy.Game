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
og_background_image = pygame.image.load('images/background.png')
background_image = pygame.transform.scale(og_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonts
font = pygame.font.SysFont(None, 55)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load movement images
        self.jump_images = [pygame.transform.scale(pygame.image.load(f'animation/player/mario_jump{i}.png'),(40,64)) for i in range(1) ]
        self.images = [pygame.transform.scale(pygame.image.load(f'animation/player/mario_run{i}.png'),(40,64)) for i in range(4)]
        self.index = 0
        self.jump_index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # Player movement properties
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 2
        self.jump_speed = -15
        self.gravity = 1
        self.jump_gravity = 1
        self.fall_gravity = 0.25
        self.on_ground = True
        self.jump_pressed = False  # Flag to avoid holding jump
        # Animation properties
        self.animation_timer = 0  # Timer for frame updating
        self.animation_speed = 150  # Milliseconds for each frame
        self.last_update = pygame.time.get_ticks()  # Last update time

    def update(self, keys):
        # Handle horizontal movement
        if keys[pygame.K_a]:  # Moving left
            self.velocity.x = -self.speed
        elif keys[pygame.K_d]:  # Moving right
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
        
        # Update animation
        self.animate()

    def animate(self):
        current_time = pygame.time.get_ticks()
        # Check if it's time to update the frame
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            
            # Update the frame index based on velocity and state
            if self.on_ground == False:  # If jumping up
                self.index = (self.index + 1) % len(self.jump_images)  # Loop through jump images
                self.image = self.jump_images[self.index]
            elif self.velocity.x != 0:  # If moving horizontally
                self.index = (self.index + 1) % len(self.images)  # Loop through run images
                self.image = self.images[self.index]
            else:  # If not moving horizontally and on the ground
                self.index = 0
                self.image = self.images[self.index]

            # Flip the image based on the direction of movement
            if self.velocity.x < 0:  # Moving left
                self.image = pygame.transform.flip(self.images[self.index], True, False)  # Flip horizontally
            elif self.velocity.x > 0:  # Moving right
                self.image = self.images[self.index]  # Original image

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(f'animation/zombie/zombie_walk{i}.png'),(64,64)) for i in range(2)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = 2.5  # Speed of the zombie
        self.move_direction = 1
        self.boundary_left = x - 250  # Left boundary
        self.boundary_right = x + 50  # Right boundary
        # Animation properties
        self.animation_timer = 0  # Timer for frame updating
        self.animation_speed = 150  # Milliseconds for each frame
        self.last_update = pygame.time.get_ticks()  # Last update time
    
    def update(self):
        # Move back and forth
        self.rect.x += self.velocity * self.move_direction

        # Reverse direction if hitting boundaries
        if self.rect.x <= self.boundary_left:  # Check left boundary
            self.rect.x = self.boundary_left  # Snap to boundary
            self.move_direction = 1  # Move right after hitting left boundary
        elif self.rect.x >= self.boundary_right:  # Check right boundary
            self.rect.x = self.boundary_right  # Snap to boundary
            self.move_direction = -1  # Move left after hitting right boundary
            
        # Flip the image based on the direction of movement
        if self.move_direction >= 0:  # Moving left
            self.image = pygame.transform.flip(self.image, True, False)  # Flip horizontally
        else:  # Moving right
            self.image = self.image  # Use the original image
            
        self.animate()
        
    def animate(self):
        current_time = pygame.time.get_ticks()
        # Check if it's time to update the frame
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            
        # Update the frame index regardless of velocity to constantly animate zombie walk
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]    
        
        # Flip the image based on the direction of movement
        if self.move_direction == -1:  # Moving left
            self.image = pygame.transform.flip(self.images[self.index], True, False)  # Flip horizontally
        else:  # Moving right
            self.image = self.images[self.index]  # Use the original image
                            
            
            

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

        # Group for all sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        # Add all zombies to the sprite group
        for zombie in self.zombies:
            self.all_sprites.add(zombie)
        # Add all platforms to the sprite group
        for platform in self.platforms:
            self.all_sprites.add(platform)

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
                    self.player.velocity.y = self.player.jump_speed  # Bounce the player up
                else:
                    # Player collided with the side of the zombie
                    player_died = True

        # Remove zombies that have been marked for removal
        for zombie in zombies_to_remove:
            self.all_sprites.remove(zombie)
            self.zombies.remove(zombie)
            zombie.kill()

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

        pygame.time.wait(5000)  # Display the message for 2 seconds

if __name__ == "__main__":
    game = Game()
    game.run()
