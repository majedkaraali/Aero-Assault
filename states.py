

class State():
    def __init__(self):
        self.state=None
        self.running=True


    def get_state(self):
        return self.state
    

    def survival_state(self):
        from survival_state import Survival
        current_state=Survival(state)
        self.state=(current_state)

    def level_state(self,level):
        from level_play_state import Level_Play
        current_state=Level_Play(state,level)
        self.state=(current_state)

    def menu_state(self):
        
        from menu_state import MenuState
        current_state=MenuState(state)
        self.state=(current_state)


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