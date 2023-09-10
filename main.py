import pygame

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
pygame.mixer.set_num_channels(64)

screen_width = 1100
screen_height = 660

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Aero Assault")


intro_image = pygame.image.load("src/img/meta/intro_image.png").convert_alpha()
intro_rect = intro_image.get_rect()


intro_duration = 5000  
intro_running=True
intro_comblete=False
intro_timer = 0
alpha = 255  
background_color=('black')

while intro_running:
    screen.fill(background_color)  
    clock.tick(60)

    events = pygame.event.get()
        
        
    for event in events:
            if event.type == pygame.QUIT:
                intro_running = False

    if intro_timer < intro_duration:
            screen.blit(intro_image, intro_rect)
            alpha -= 1
            intro_image.set_alpha(alpha)
            pygame.display.update()
            intro_timer += clock.get_time()
            pygame.display.flip()

    else:
        intro_running=False
        intro_comblete=True
          

if  intro_comblete:
    from states import states
    from objects.objects import *
    from windows import *
    from states.survival_state import *
    state=states.state
    state.menu_state()
    

    while state.running:
        current_state=state
        clock.tick(60)
        events = pygame.event.get()
        
        
        for event in events:
            if event.type == pygame.QUIT:
                state.running = False

        

        
        current_state.handle_events(events)
        current_state.draw(screen)

        #  print(clock.get_fps())
        pygame.display.flip()

    pygame.quit()


