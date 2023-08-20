import pygame
from windows import Main_menu_window,Game_modes_window

width,height=1100,660



class MenuState():

    def __init__(self,state):
        self.main_menu_window=Main_menu_window()
        self.game_mode_window=Game_modes_window()
        self.running=state.running
        self.screen=self.main_menu_window
        self.buttons=self.screen.get_buttons()
        self.state=state
 
    def handle_events(self, events):
        for event in events:
            self.handle_buttons(event)
            if event.type == pygame.QUIT:
                self.running = False

             
    def handle_buttons(self,event):
        
        if event.type==pygame.MOUSEBUTTONDOWN:

    
            if self.main_menu_window.play_button.holding:
                self.screen=self.game_mode_window

            if self.main_menu_window.Exit_button.holding:
                    self.state.running=False


            if self.game_mode_window.survival_buttonn.holding:
                self.screen.survival_frame()

            elif self.game_mode_window.apex_button.holding:
                self.screen.apex_frame()

            elif self.game_mode_window.levels_buttoon.holding:
                from levels import levels 
                for level in levels:
                    level.chek_lock(level.number)
                self.screen.levels_frame(levels)

            elif self.game_mode_window.back_button.holding:
                # self.screen.selected_frame=False
                self.screen=self.main_menu_window
                

            if self.game_mode_window.apex_play_button:
                    pass

            if self.game_mode_window.survival_play_button:
                    self.state.survival_state()

            if self.game_mode_window.level_play_button:
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
                    print('WWWWWWWWWWWWWWWWWW')
                    from levels import levels
                    for level in levels:
                        level.chek_lock(level.number)
                    self.screen.levels_frame(levels)
                

    def draw(self,screen):
     #   print(self.screen)
        self.screen.draw(screen)
        self.screen.draw_frames(screen)
        self.screen.handle_buttons()