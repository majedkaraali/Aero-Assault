import pygame

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()


screen_width = 1100
screen_height = 660

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SPAA Game")


from states import states
state=states.state
state.menu_state()



def main():
    while state.running:
        current_state=state

        clock.tick(60)
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                state.running = False


        current_state.handle_events(events)
        current_state.draw(screen)


        pygame.display.flip()

    pygame.quit()
if __name__=='__main__':
    main()
