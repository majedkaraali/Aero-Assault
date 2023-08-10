import pygame


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((500, 500))  # Set your desired screen dimensions
pygame.display.set_caption("Animated GIF in Pygame")
clock = pygame.time.Clock()

# Load the GIF and extract frames
gif_path = "src/img/aaa.gif"  # Replace with the actual path to your GIF

frames = [pygame.image.fromstring(frame.tostring(), frame.size, "RGB") for frame in clip.iter_frames(fps=clip.fps)]

# Main loop for displaying frames
running = True
frame_index = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(frames[frame_index], (0, 0))
    pygame.display.flip()
    clock.tick(clip.fps)

    frame_index = (frame_index + 1) % len(frames)

# Clean up resources
clip.reader.close()
clip.audio.reader.close_proc()
pygame.quit()
