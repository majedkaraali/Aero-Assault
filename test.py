import pygame
import sys
from Sprite import Sprite
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spritesheet Example")

# Create a sprite instance
spritesheet_path = "spritesheet.png"  # Path to your spritesheet
sprite = Sprite(spritesheet_path, width=64, height=64, frame_width=32, frame_height=32, draw_limit=5)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sprite.update()

    screen.fill((0, 0, 0))
    sprite.draw(screen, screen_width // 2, screen_height // 2)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
