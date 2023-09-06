import pygame
from windows import Test
from levels import levels
width,height=1100,660


select_sound=pygame.mixer.Sound("src\\sound\\ui\\button_click.mp3")
up_menu_sound=pygame.mixer.Sound("src\\sound\\ui\\button_click_up.mp3")
down_menu_sound=pygame.mixer.Sound("src\\sound\\ui\\button_click_down.mp3")

select_sound.set_volume(999)  
up_menu_sound.set_volume(999) 
down_menu_sound.set_volume(999)  



class MenuState():

    def __init__(self,state):
        self.main_menu_window=Test()
        self.running=state.running
        self.window=self.main_menu_window
        self.window.main_menu()
        self.buttons=self.window.get_buttons()
        self.state=state
        self.levels_numbers=[]
        self.window.achvm()
        for level in levels:
            self.levels_numbers.append(level.get_number())
            level.chek_lock(level.number)
 
    def handle_events(self, events):

        for event in events:
            self.handle_buttons(event)
            if event.type == pygame.QUIT:
                self.running = False



             
    def handle_buttons(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:

                    

            if self.window.play_button.holding:
                select_sound.play()
                self.window.game_modes()
                self.window.play_button.holding=False
                self.window.selected_frame=False


            if self.window.Exit_button.holding:
                    self.state.running=False

            if self.window.back_button.holding:
                self.window.main_menu()
                self.window.back_button.holding=False
                self.window.selected_frame=False
                self.window.selected_level=None
                self.window.achvm()
                down_menu_sound.play()

            if self.window.levels_buttoon.holding:
                self.window.selected_game_mode='levels'
                self.window.levels_frame(levels)
                self.window.levels_buttoon.holding=False

                up_menu_sound.play()
            if self.window.survival_buttonn.holding:
                self.window.selected_game_mode='survival'
                self.window.survival_buttonn.holding=False
                self.window.survival_frame()
                up_menu_sound.play()

            if self.window.apex_button.holding:
                self.window.selected_game_mode='apex'
                self.window.apex_button.holding=False
                self.window.apex_frame()
                up_menu_sound.play()



                

            if self.window.selected_frame_button:
                button_text=self.window.selected_frame_button.get_text()
                if button_text in self.levels_numbers:
                    self.selected_level=int(button_text)
                    self.window.level_description_frame(button_text,levels)
                    select_sound.play()

            


                if button_text=='Play':
                    if not self.window.selected_frame_button.locked:
                        select_sound.play()
                        if self.window.selected_game_mode=='levels':
                            self.state.level_state(levels[self.selected_level-1])
                        elif self.window.selected_game_mode=='survival':
                            self.state.survival_state()
                    

                if button_text=='Back':
                    self.window.levels_frame(levels)
                    down_menu_sound.play()
                


               
                    
                        

                

     

    def draw(self,screen):
        
        self.window.draw(screen)
        self.window.draw_frames(screen)
        self.window.handle_buttons()