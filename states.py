import pygame

import objects
import os
from GUI import Button,Frame
from windows import Main_menu_screen,Game_modes_window
from levels import levels 

#from survival_state import Survival

pygame.init()

pygame.mixer.init()
width,height=1100,660

def _player():
        global player
        player=objects.Player(400,height-107,[],[],'Unnamed',[])
        return player

main_menu=Main_menu_screen()
game_mode_window=Game_modes_window()



font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
font_size = 19 
font = pygame.font.Font(font_path, font_size)


background=pygame.image.load('src/img/background1.png').convert_alpha()
statics_image=pygame.image.load('src/img/statics2.png').convert_alpha()

class GameState:

    def __init__(self):
        self.running = False

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass



    
class MenuState(GameState):

    def __init__(self):
        super().__init__()
        self.running=True
        self.screen=main_menu
        self.buttons=self.screen.get_buttons()
        
    

        
    def handle_events(self, events):
        global current_state,state
        for event in events:
            self.handle_buttons(event)
            if event.type == pygame.QUIT:
                self.running = False

            

                            

             
    def handle_buttons(self,event):
        global state
        holding_button=self.screen.holding_button
        if holding_button:
            button_head=holding_button.get_text()

            
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                # Menu buttons
                if button_head=="Play":
                    self.screen=game_mode_window

                # gammodes buttons
      

                if button_head=="Survival":
                    self.screen.survival_frame()

                elif button_head=="Apex Challenge":
                    self.screen.apex_frame()
                elif button_head =="Levels":
                    self.screen.levels_frame(levels)

                elif button_head=='Return':
                    self.screen.selected_frame=False
                    self.screen=main_menu

                if self.screen.apex_play_button:
                    if self.screen.apex_play_button.holding:
                        pass

                if self.screen.survival_play_button:
                    if self.screen.survival_play_button.holding:
                        _player()
                       # state=survival_play_state
                if self.screen.level_play_button:
                    if self.screen.level_play_button.holding:
                        from level_play_state import Level_Play
                        level_paly_state=Level_Play(self.screen.selected_level)
                        _player()
                        state=level_paly_state

                if button_head in ['1','2','3','4','5','6','7','8','9','10']:
                    self.screen.level_description_frame(int(button_head),levels)
                if button_head=="Back":
                    self.screen.levels_frame(levels)
            

    def draw(self,screen):
        self.screen.draw(screen)
        self.screen.draw_frames(screen)
        self.screen.handle_buttons()        
 

            
       
     


        
menu_state = MenuState()
#from survival_state import Survival

#survival_play_state = Survival()

state=menu_state


def get_state():
        return state
