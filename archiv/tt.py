import pygame

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))

# Set the initial position
position = (100, 100)

# Create a rectangle surface
width = 20
height = 40
rect = pygame.Surface((width, height), pygame.SRCALPHA)


# Define the rotation angle in degrees
angle = 45

# Rotate the rectangle


# Blit the rotated rectangle onto the screen at the adjusted position

# Update the display
pygame.display.flip()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    angle+=1
    rotated_rect = pygame.transform.rotate(rect, angle)

# Calculate the position adjustment to center the rotated rectangle
    x_adjustment = (rotated_rect.get_width() - width) // 2
    y_adjustment = (rotated_rect.get_height() - height) // 2
    pygame.draw.rect(rect, pygame.Color('blue'), (0, 0, width, height))
    screen.blit(rotated_rect, (position[0] - x_adjustment, position[1] - y_adjustment))

