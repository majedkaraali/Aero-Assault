

class State():
    def __init__(self):
        self.state=None
        self.running=True


    def get_state(self):
        return self.state
    

    def survival_state(self):
        from survival_state import Survival
        self.state=Survival(state)

    def level_state(self,level):
        from level_play_state import Level_Play
        self.state=Level_Play(state,level)

    def menu_state(self):
        from menu_state import MenuState
        self.state=MenuState(state)

    def handle_events(self, events):
        self.state.handle_events(events)


    def draw(self,screen):
        self.state.draw(screen)



class GameState:

    def __init__(self):
        self.running = False

    def handle_events(self, events):
        pass

    def draw(self):
        pass



    

    
state=State()