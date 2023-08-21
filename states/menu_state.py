import pygame
from windows import Test
from levels import levels
width,height=1100,660



class MenuState():

    def __init__(self,state):
        self.main_menu_window=Test()
        self.running=state.running
        self.window=self.main_menu_window
        self.window.main_menu()
        self.buttons=self.window.get_buttons()
        self.state=state
        self.levels_numbers=[]
 
    def handle_events(self, events):
        for event in events:
            self.handle_buttons(event)
            if event.type == pygame.QUIT:
                self.running = False

             
    def handle_buttons(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.window.play_button.holding:
                self.window.game_modes()
                self.window.play_button.holding=False


            if self.window.Exit_button.holding:
                    self.state.running=False

            if self.window.back_button.holding:
                self.window.main_menu()
                self.window.back_button.holding=False
                self.window.selected_frame=False
                self.window.selected_level=None

            if self.window.levels_buttoon.holding:
                for level in levels:
                    level.chek_lock(level.number)
                self.window.levels_frame(levels)
                self.window.levels_buttoon.holding=False
            
            if self.window.selected_frame_button:
                button_text=self.window.selected_frame_button.get_text()
                if button_text in ['1','2','3','4','5','6','7','8','9','10']:
                    self.selected_level=int(button_text)
                    self.window.level_description_frame(button_text,levels)


                if button_text=='Play':
                    print('hahah')
                    self.state.level_state(levels[self.selected_level-1])

                if button_text=='Back':
                     self.window.levels_frame(levels)
                

     

    def draw(self,screen):
        print(self.window.selected_frame_button)
        self.window.draw(screen)
        self.window.draw_frames(screen)
        self.window.handle_buttons()