import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
BACKGROUND_WIDTH = SCREEN_WIDTH

# Colors
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Clone")

# Load assets
# (You'll need to provide your own Mario image or use Pygame's built-in shapes temporarily)
mario_image = pygame.image.load('images/mario.png')
og_background_image = pygame.image.load('images/background.png')
background_image = pygame.transform.scale(og_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(mario_image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_speed = -15
        self.gravity = 1

    def update(self, keys):
        # Handle horizontal movement
        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
        elif keys[pygame.K_d]:
            self.velocity.x = self.speed
        elif keys[pygame.K_s]:
            self.velocity.y = -self.jump_speed
            if self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += 1
        elif keys[pygame.K_w]:
            self.velocity.y = self.jump_speed
            if self.rect.top > 0:
                self.rect.y -= 1
        else:
            self.velocity.x = 0

        # Handle jump
        if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity.y = self.jump_speed

        # Apply gravity
        self.velocity.y += self.gravity
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Prevent falling through the bottom
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity.y = 0

# Create a player instance
player = Player(100, SCREEN_HEIGHT - 70)

# Group for all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variables for the background scrolling
backgrounds = [background_image.copy(), background_image.copy()]
background_x = [0, SCREEN_WIDTH + 200]  # Positions of the two backgrounds

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Scrolling offset
background_offset = 0


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    # Update background offset if the player is in the middle of the screen
    if player.rect.right > 600 and keys[pygame.K_d]:
        background_offset -= player.speed
        player.rect.right = 600
    elif player.rect.left < 200 and keys[pygame.K_a]:
        background_offset += player.speed
        player.rect.left = 200

    # Prevent scrolling beyond the background image
    background_offset = max(-SCREEN_WIDTH, min(0, background_offset))
    all_sprites.update(keys)
     
   # Update background positions based on player movement
    for i in range(len(background_x)):
        background_x[i] -= player.velocity.x  # Move background opposite to player

        # Reset the background position when it goes off screen
        if background_x[i] <- BACKGROUND_WIDTH:
            background_x[i] += BACKGROUND_WIDTH * 2  # Move it to the right end
        elif background_x[i] > BACKGROUND_WIDTH:
            background_x[i] -= BACKGROUND_WIDTH * 2  # Move it to the left end

 

    # Draw everything
    screen.fill(WHITE)
    for i in range(len(background_x)):  # Draw both backgrounds at the same time
        screen.blit(background_image, (background_x[i], 0))
    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()