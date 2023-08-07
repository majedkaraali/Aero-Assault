import pygame

# Initialize Pygame
pygame.init()

# Load an image
image = pygame.image.load("src/img/spaa-gepard3.png")

# Create a flipped version of the image (horizontally)
flipped_image = pygame.transform.flip(image, True, False)

# Set up the display
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))  # Fill the screen with white

# Blit the original and flipped images onto the screen
screen.blit(image, (100, 100))
screen.blit(flipped_image, (300, 100))

# Update the display
pygame.display.update()

# Event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()