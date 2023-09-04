import pygame

# Initialize Pygame
pygame.init()

# Load the reloading sound
reloading = pygame.mixer.Sound("src/sound/wopn/reloading2.wav")

# Play the sound on a specific channel (e.g., channel 0)
channel = reloading.play()

# Check if the "reloading" sound on channel 0 has finished playing
while channel.get_busy():
    pygame.time.delay(100)  # Delay for a short period (e.g., 100 milliseconds) before checking again

# Sound has finished playing on channel 0
print("Reloading sound has finished playing")

# Quit Pygame when done
pygame.quit()
