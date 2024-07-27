import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

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
class Player(pygame.sprite.Sprite):w
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

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    all_sprites.update(keys)

    # Draw everything
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()