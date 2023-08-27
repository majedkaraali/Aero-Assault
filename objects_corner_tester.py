import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rotate Around Specific Point")

# Load the image
image = pygame.image.load('src/img/weapons/missile4.png')  # Replace with your image path
image_rect = image.get_rect()

image2=pygame.image.load('src/img/weapons/smoke.png').convert_alpha()
# Rotation point
rotation_point = (300, 200)
rotation_point2 = (600, 400)
# Initial rotation angle (in degrees)
rotation_angle = 0
angle=0
# Rotation increment (in degrees)
rotation_increment = 1
from Sprite import Sprite

# Initialize the clock
clock = pygame.time.Clock()

spritesheet_path=('src/img/weapons/smoke2.png')
sprite = Sprite(200,200,spritesheet_path, width=300, height=238, frame_width=25, frame_height=238)


mid_pos=(0,0)

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
    rotated_image = pygame.transform.rotate(image, angle)

    # Calculate the new position of the rotated image
    rotated_rect = rotated_image.get_rect(center=rotation_point)

    tpleft=rotated_rect.topleft
    topright=rotated_rect.topright
    bottomleft=rotated_rect.bottomleft
    bottomright=rotated_rect.bottomright
    midbottom=rotated_rect.midbottom
    midtop=rotated_rect.midtop
    midleft=rotated_rect.midleft
    midright=rotated_rect.midright

    rct1=pygame.Rect(tpleft[0],tpleft[1],10,10)
    rct2=pygame.Rect(topright[0],topright[1],10,10)
    rct3=pygame.Rect(bottomleft[0],bottomleft[1],10,10)
    rct4=pygame.Rect(bottomright[0],bottomright[1],10,10)
    rct5=pygame.Rect(midbottom[0],midbottom[1],10,10)
    rct6=pygame.Rect(midtop[0],midtop[1],10,10)
    rct7=pygame.Rect(midleft[0],midleft[1],10,10)
    rct8=pygame.Rect(midright[0],midright[1],10,10)

    rct1.center=(tpleft[0],tpleft[1])
    rct2.center=(topright[0],topright[1])
    rct3.center=(bottomleft[0],bottomleft[1])
    rct4.center=(bottomright[0],bottomright[1])
    
    rct5.center=(midbottom[0],midbottom[1])
    rct6.center=(midtop[0],midtop[1])
    rct7.center=(midleft[0],midleft[1])
    rct8.center=(midright[0],midright[1])



    pygame.draw.rect(screen,'black',rct5)
    pygame.draw.rect(screen,'orange',rct6)
    pygame.draw.rect(screen,'gray',rct7)
    pygame.draw.rect(screen,'lightblue',rct8)

    # Draw the rotated image





    # tpleft2=sprite.topleft
    # topright2=sprite.topright
    # bottomleft2=sprite.bottomleft
    # bottomright2=sprite.bottomright
    # midbottom2=sprite.midbottom
    # midtop2=sprite.midtop
    # midleft2=sprite.midleft
    # midright2=sprite.midright

    # rct11=pygame.Rect(tpleft2[0],tpleft2[1],5,5)
    # rct22=pygame.Rect(topright2[0],topright2[1],5,5)
    # rct33=pygame.Rect(bottomleft2[0],bottomleft2[1],5,5)
    # rct44=pygame.Rect(bottomright2[0],bottomright2[1],5,5)
    # rct55=pygame.Rect(midbottom2[0],midbottom2[1],5,5)
    # rct66=pygame.Rect(midtop2[0],midtop2[1],5,5)
    # rct77=pygame.Rect(midleft2[0],midleft2[1],5,5)
    # rct88=pygame.Rect(midright2[0],midright2[1],5,5)

    # rct11.center=(tpleft2[0],tpleft2[1])
    # rct22.center=(topright2[0],topright2[1])
    # rct33.center=(bottomleft2[0],bottomleft2[1])
    # rct44.center=(bottomright2[0],bottomright2[1])
    # rct55.center=(midbottom2[0],midbottom2[1])
    # rct66.center=(midtop2[0],midtop2[1])
    # rct77.center=(midleft2[0],midleft2[1])
    # rct88.center=(midright2[0],midright2[1])

    # pygame.draw.rect(screen,'red',rct11)
    # pygame.draw.rect(screen,'blue',rct22)
    # pygame.draw.rect(screen,'green',rct33)
    # pygame.draw.rect(screen,'yellow',rct44)
    # pygame.draw.rect(screen,'black',rct55)
    # pygame.draw.rect(screen,'orange',rct66)
    # pygame.draw.rect(screen,'gray',rct77)
    # pygame.draw.rect(screen,'lightblue',rct88)


    screen.blit(rotated_image, rotated_rect.topleft)


    if angle>=380:
          angle=0
    
    angle+=1

    custum_angel=angle

    corner_pos=rotated_rect.center
    screen.blit(rotated_image, rotated_rect.topleft)
    sprite.set_vars(corner_pos[0],corner_pos[1],custum_angel)
    sprite.update()
    sprite.draw(screen)
    
    rotated_rect2 = sprite.get_rect()

    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(30)

# Clean up
pygame.quit()
sys.exit()
