import pygame
import sys
from Sprite import Sprite
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spritesheet Example")

# Create a sprite instance
spritesheet_path = "src\img\weapons\smoke.png"  
sprite = Sprite(200,200,spritesheet_path, width=300, height=76, frame_width=25, frame_height=76)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sprite.update()

    screen.fill('black')
    sprite.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
