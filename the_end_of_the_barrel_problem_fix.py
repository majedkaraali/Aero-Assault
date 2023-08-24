import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rotate Around Specific Point")

# Load the image
image = pygame.image.load("src/img/vehicles/barrel2.png")  # Replace with your image path
image_rect = image.get_rect()

# Rotation point
rotation_point = (300, 200)

# Initial rotation angle (in degrees)
rotation_angle = 0

# Rotation increment (in degrees)
rotation_increment = 1

# Initialize the clock
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the rotation angle
    rotation_angle += rotation_increment

    # Clear the screen
    screen.fill((120, 120, 120))

    # Rotate the image
    rotated_image = pygame.transform.rotate(image, rotation_angle)

    # Calculate the new position of the rotated image
    rotated_rect = rotated_image.get_rect(center=rotation_point)
    tpleft1=rotated_rect.topleft
    tpleft2=rotated_rect.topright
    tpleft3=rotated_rect.bottomleft
    tpleft4=rotated_rect.bottomright
    tpleft5=rotated_rect.midbottom
    tpleft6=rotated_rect.midtop
    tpleft7=rotated_rect.midbottom
    tpleft8=rotated_rect.midtop

    rct1=pygame.Rect(tpleft1[0],tpleft1[1],15,15)
    rct2=pygame.Rect(tpleft2[0],tpleft2[1],15,15)
    rct3=pygame.Rect(tpleft3[0],tpleft3[1],15,15)
    rct4=pygame.Rect(tpleft4[0],tpleft4[1],15,15)
    rct5=pygame.Rect(tpleft5[0],tpleft5[1],15,15)
    rct6=pygame.Rect(tpleft6[0],tpleft6[1],15,15)
    rct7=pygame.Rect(tpleft7[0],tpleft7[1],15,15)
    rct8=pygame.Rect(tpleft8[0],tpleft8[1],15,15)

    rct1.center=(tpleft1[0],tpleft1[1])
    rct2.center=(tpleft2[0],tpleft2[1])
    rct3.center=(tpleft3[0],tpleft3[1])
    rct4.center=(tpleft4[0],tpleft4[1])
    
    rct5.center=(tpleft5[0],tpleft5[1])
    rct6.center=(tpleft6[0],tpleft6[1])
    rct7.center=(tpleft7[0],tpleft7[1])
    rct8.center=(tpleft8[0],tpleft8[1])


    pygame.draw.rect(screen,'red',rct1)
    pygame.draw.rect(screen,'blue',rct2)
    pygame.draw.rect(screen,'green',rct3)
    pygame.draw.rect(screen,'yellow',rct4)
    pygame.draw.rect(screen,'black',rct5)
    pygame.draw.rect(screen,'orange',rct6)
    pygame.draw.rect(screen,'gray',rct7)
    pygame.draw.rect(screen,'lightblue',rct8)

    # Draw the rotated image
    screen.blit(rotated_image, rotated_rect.topleft)

    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
