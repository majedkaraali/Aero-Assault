import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define a custom sprite class
class MySprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Create a surface for the sprite
        self.image.fill((255, 0, 0))  # Fill the surface with a color (e.g., red)
        self.rect = self.image.get_rect()  # Get the rectangle of the surface
        self.rect.center = (x, y)  # Set the initial position of the sprite
        self.rotation = 0  # Initial rotation angle

    def update(self):

        self.rotation += 1  # Increment the rotation angle

        # Rotate the sprite's image
        self.image = pygame.transform.rotate(self.image, self.rotation)

# Create a sprite group
all_sprites = pygame.sprite.Group()

# Create multiple instances of the custom sprite class
for _ in range(1):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    sprite = MySprite(x, y)
    all_sprites.add(sprite)

# Set the desired FPS
fps = 60

# Create a Clock object
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw all sprites on the screen
    all_sprites.draw(screen)

    # Update the screen
    pygame.display.flip()

    # Limit the FPS
    clock.tick(fps)

# Quit Pygame
pygame.quit()
