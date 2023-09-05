import pygame
from pygame.locals import *
import sys

pygame.init()

# Set up your display with a black66 background
screen = pygame.display.set_mode((1100, 660))  # Adjust dimensions as needed
pygame.display.set_caption("Game Intro")
background_color = (0, 0, 0)  # Black background color

# Load the intro image
intro_image = pygame.image.load("src/img/meta/intro_image.png")
intro_rect = intro_image.get_rect()

# Set the initial alpha value for the image
alpha = 255  # Fully opaque

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Timer for controlling the intro duration
intro_timer = 0
intro_duration = 5000  # 5000 milliseconds (5 seconds)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(background_color)  # Fill with a black background

    if intro_timer < intro_duration:
        screen.blit(intro_image, intro_rect)

        # Gradually decrease alpha value to create a fade-in effect
        alpha -= 1
        intro_image.set_alpha(alpha)

        # Update the display
        pygame.display.update()

        # Increase the timer
        intro_timer += clock.get_time()
    else:
        running = False  # Exit the loop after the intro duration

    clock.tick(60)  

pygame.quit()
sys.exit()
