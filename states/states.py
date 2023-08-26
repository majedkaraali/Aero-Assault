
class State():
    def __init__(self):
        self.state=None
        self.running=True



    def get_state(self):
        return self.state
    

    def survival_state(self):
        from survival_state import Survival
     
        n_state=Survival(state)

        self.state=(n_state)

    def level_state(self,level):
        from states.level_play_state import Level_Play
        n_state=Level_Play(state,level)
        self.state=(n_state)

    
    def survival_state(self):
        from states.survival_state import Survival
        n_state=Survival(state)
        self.state=(n_state)    

    def menu_state(self):
        from states.menu_state import MenuState
        n_state=MenuState(state)
        self.state=(n_state)


    def handle_events(self, events):
        self.state.handle_events(events)


    def draw(self,screen):
        self.state.draw(screen)




    
state=State()