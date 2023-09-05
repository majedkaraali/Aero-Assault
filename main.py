import pygame

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
pygame.mixer.set_num_channels(64)

screen_width = 1100
screen_height = 660

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Aero Assault")


intro_image = pygame.image.load("src/img/meta/intro_image.png")
intro_rect = intro_image.get_rect()



intro_duration = 5000  

from states import states
state=states.state
state.menu_state()
background_color=('black')

def main():
    intro_timer = 0
    alpha = 255  

    while state.running:
        current_state=state
        screen.fill(background_color)  
        clock.tick(60)
        events = pygame.event.get()
        
        
        for event in events:
            if event.type == pygame.QUIT:
                state.running = False

        

        if intro_timer < intro_duration:
            screen.blit(intro_image, intro_rect)
            alpha -= 1
            intro_image.set_alpha(alpha)
            pygame.display.update()
            intro_timer += clock.get_time()

        else:
            current_state.handle_events(events)
            current_state.draw(screen)


        pygame.display.flip()

    pygame.quit()
    
if __name__=='__main__':
    main()
