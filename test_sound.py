import pygame
pygame.init()

# Initialize Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")

# Load the firing sound effect
firing_sound = pygame.mixer.Sound("shoot.wav")
pygame.mixer.set_num_channels(64)
# Initialize variables
firing = False
fire_delay = 0  # Introduce a delay
fire_delay_threshold = 10  # Adjust this threshold for your desired delay

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire trigger is pressed
                firing = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                # Fire trigger is released
                firing = False
                fire_delay = 0  # Reset the delay when releasing the trigger

    # Play the firing sound while the fire trigger is held down with a delay
    if firing and fire_delay <= 0:
        firing_sound.play()
        fire_delay = fire_delay_threshold  # Reset the delay

    # Decrement the fire delay
    if fire_delay > 0:
        fire_delay -= 1

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
