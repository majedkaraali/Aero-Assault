import pygame
from windows import Main_menu_window,Game_modes_window

width,height=1100,660
main_menu_window=Main_menu_window()
game_mode_window=Game_modes_window()


class MenuState():

    def __init__(self,state):
        self.running=True
        self.screen=main_menu_window
        self.buttons=self.screen.get_buttons()
        self.state=state
 
    def handle_events(self, events):
        for event in events:
            self.handle_buttons(event)
            if event.type == pygame.QUIT:
                self.running = False

             
    def handle_buttons(self,event):
        
        if event.type==pygame.MOUSEBUTTONDOWN:

            if self.screen.name=='menu':

                if self.screen.play_button.holding:
                    game_mode_window=Game_modes_window()
                    self.screen=game_mode_window

                   
            elif self.screen.name=='gamemode':
                if self.screen.survival_buttonn.holding:
                    self.screen.survival_frame()

                elif self.screen.apex_button.holding:
                    self.screen.apex_frame()

                elif self.screen.levels_buttoon.holding:
                    from levels import levels 
                    for level in levels:
                        level.chek_lock(level.number)
                    self.screen.levels_frame(levels)

                elif self.screen.back_button.holding:
                    self.screen.selected_frame=False
                    self.screen=main_menu_window
                    

                if self.screen.apex_play_button:
                    if self.screen.apex_play_button.holding:
                        pass

                if self.screen.survival_play_button:
                    if self.screen.survival_play_button.holding:
                        self.state.survival_state()

                if self.screen.level_play_button:
                    if self.screen.level_play_button.holding:
                        level=self.screen.selected_level
                        self.state.level_state(level)


            if self.screen.holding_button:
                button_head=self.screen.holding_button.get_text()

                if button_head in ['1','2','3','4','5','6','7','8','9','10']:
                    from levels import levels
                    for level in levels:
                        level.chek_lock(level.number)
                
                    self.screen.level_description_frame(int(button_head),levels)

                elif button_head=="Back":
                    from levels import levels
                    for level in levels:
                        level.chek_lock(level.number)
                    self.screen.levels_frame(levels)
                

    def draw(self,screen):
     #   print(self.screen)
        self.screen.draw(screen)
        self.screen.draw_frames(screen)
        self.screen.handle_buttons()