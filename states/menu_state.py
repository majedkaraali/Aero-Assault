import pygame
from windows import menu_windows
from levels import levels
width,height=1100,660


select_sound=pygame.mixer.Sound("src\\sound\\ui\\button_click.mp3")
up_menu_sound=pygame.mixer.Sound("src\\sound\\ui\\button_click_up.mp3")
down_menu_sound=pygame.mixer.Sound("src\\sound\\ui\\button_click_down.mp3")

credits_image=pygame.image.load('src\\img\\meta\\credits.png').convert_alpha()

select_sound.set_volume(999)  
up_menu_sound.set_volume(999) 
down_menu_sound.set_volume(999)








class MenuState():
    credits_height=credits_image.get_height()
    cretdits_height_point=0
    def __init__(self,state):
        self.main_menu_window=menu_windows()
        self.running=state.running
        self.window=self.main_menu_window
        self.window.main_menu()
        self.buttons=self.window.get_buttons()
        self.state=state
        self.levels_numbers=[]
        self.window.achvm()
        self.show_credits=False

        self.play_music_on=self.state.music_play
        self.play_fx_on=self.state.sound_play
        self.window.music_turn_on= self.play_music_on
        self.window.sound_turn_on= self.play_fx_on

        
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

            if self.window.Credits_button.holding:
                self.window.Credits_button.holding=False
                select_sound.play()
                self.show_credits=True

            if self.window.options_button.holding:
                select_sound.play()
                self.window.options_button.holding=False
                self.window.selected_frame=False
                self.window.option_view()

            if self.window.Audio.holding:
                up_menu_sound.play()
                self.window.audio_view()
                self.window.Audio.holding=False

            if self.window.Controls.holding:
                up_menu_sound.play()
                self.window.controls_view()
                self.window.Controls.holding=False
                
            if self.window.Reset.holding:
                select_sound.play()
                self.window.reset_data_view()
                self.window.Reset.holding=False

            if self.window.reset.holding:
                up_menu_sound.play()
                self.window.reset_data()
                self.levels_numbers=[]
                self.window.reset.holding=False

                for level in levels:
                    self.levels_numbers.append(level.get_number())
                    level.chek_lock(level.number)

                self.window.data_reseted_view()
          

     


            if self.window.music_btn.holding:
                    
                    self.window.music_btn.holding=False
                    if self.play_music_on:
                        self.window.music_turn_on=False
                        self.play_music_on=False

                    elif not self.play_music_on:
                        self.window.music_turn_on=True
                        self.play_music_on=True
                    self.window.audio_view()

            if self.window.sound_btn.holding:
                    self.window.sound_btn.holding=False
                    if self.play_fx_on:
                        self.window.sound_turn_on=False
                        self.play_fx_on=False

                    elif not self.play_fx_on:
                        self.window.sound_turn_on=True
                        self.play_fx_on=True
                    self.window.audio_view()


            
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
                    self.state.sound_play=self.play_music_on
                    self.state.music_play=self.play_music_on
                    if not self.window.selected_frame_button.locked:
                        
                        select_sound.play()
                        if self.window.selected_game_mode=='levels':
                            self.state.level_state(levels[self.selected_level-1])
                        elif self.window.selected_game_mode=='survival':
                            self.state.survival_state()
                    

                if button_text=='Back':
                    self.window.levels_frame(levels)
                    down_menu_sound.play()
                

        if event.type==pygame.KEYDOWN:
            keys = pygame.key.get_pressed() 
            if keys[pygame.K_ESCAPE]:
                if self.show_credits:
                    self.show_credits=False
                    self.cretdits_height_point=0
               
                    
    def credits_show(self,screen):
    
        if abs(self.cretdits_height_point)<self.credits_height:
            self.cretdits_height_point-=1.5
        else:
            self.show_credits=False
            self.cretdits_height_point=0
        screen.blit(credits_image,(0,self.cretdits_height_point))                       

                

     

    def draw(self,screen):
        if self.show_credits:
            self.credits_show(screen)
        else:
            self.window.draw(screen)
            self.window.draw_frames(screen)
            self.window.handle_buttons()