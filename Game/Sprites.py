import pygame

from . import SCREEN_HEIGHT, WHITE, BLACK


class Score(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.score = 0
        self.font = pygame.font.SysFont(None, 55)  # Moved the font initialization here
        self.image = self.font.render(f"Score: {self.score}", True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def increase_score(self, amount):
        self.score += amount
        self.image = self.font.render(f"Score: {self.score}", True, WHITE)
        
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load movement images
        self.jump_images = [pygame.transform.scale(pygame.image.load(f'Game/static/animation/player/mario_jump{i}.png'),(40,64)) for i in range(1) ]
        self.images = [pygame.transform.scale(pygame.image.load(f'Game/static/animation/player/mario_run{i}.png'),(40,64)) for i in range(4)]
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
        self.images = [pygame.transform.scale(pygame.image.load(f'Game/static/animation/zombie/zombie_walk{i}.png'),(64,64)) for i in range(2)]
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
        
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(f'Game/static/animation/goldCoin/goldCoin{i}.png'),(32,32)) for i in range(8)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collected = False  # Flag to check if the coin has been collected
         # Animation properties
        self.animation_timer = 0  # Timer for frame updating
        self.animation_speed = 150  # Milliseconds for each frame
        self.last_update = pygame.time.get_ticks()  # Last update time
        
    def animate(self):
        current_time = pygame.time.get_ticks()
        # Check if it's time to update the frame
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            
        # Update the frame index regardless of velocity to constantly animate zombie walk
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]    
        
                            
        

