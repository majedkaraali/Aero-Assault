import pygame



pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()


screen_width = 1100
screen_height = 660
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SPAA Game")

import states
current_state = states.menu_state



def update_state():
    global current_state
    current_state = states.get_state()



def main():

    while current_state.running:
        update_state()
        clock.tick(60)
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                current_state.running = False

        current_state.handle_events(events)
        current_state.update()
        current_state.draw(screen)
        pygame.display.flip()
      #  print(clock.get_fps())

    pygame.quit()
if __name__=='__main__':
    main()
