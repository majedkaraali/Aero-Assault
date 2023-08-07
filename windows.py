import pygame
from GUI import Button,Frame,Levels_Frame
pygame.init()
width,height=1100,660
gui=pygame.image.load('src/img/GUI/background.png').convert_alpha()
font = pygame.font.Font(None, 24)

def pause_screen(screen,state):
    pygame.draw.rect(state.rewards_surface,state.border_color, state.frame_surface.get_rect(), state.border_width)
    screen.blit(state.frame_surface, state.frame_position)


    resume_button = pygame.draw.rect(state.frame_surface, (0, 0, 255),state.resume_button_rect)
    resume_button_text = font.render("Resume", True, (255, 255, 255))
    resume_button_text_rect = resume_button_text.get_rect(center=resume_button.center)
           

    mainmenu_button=pygame.draw.rect(state.frame_surface,(0, 0, 255),state.main_menu_button_rect)
    mainmenu_button_text=font.render("Main menu", True, (255, 255, 255))
    mainmenu_button_text_rect=mainmenu_button_text.get_rect(center=mainmenu_button.center)

    exit_button=pygame.draw.rect(state.frame_surface,(0, 0, 255),state.exit_button_rect)
    exit_button_text=font.render("Exit", True, (255, 255, 255))
    exit_button_text_rect=exit_button_text.get_rect(center=exit_button.center)


    state.frame_surface.blit(resume_button_text,resume_button_text_rect)
    state.frame_surface.blit(mainmenu_button_text,mainmenu_button_text_rect)
    state.frame_surface.blit(exit_button_text,exit_button_text_rect)



def reward_screen_view(screen,state):
        pygame.draw.rect(state.rewards_surface,state.border_color, state.rewards_surface.get_rect(), state.border_width)
        screen.blit(state.rewards_surface, state.reward_scr_position)
        state.rewards_surface.fill('silver')


        
        main_menu_text = font.render("Main Menu", True, (255, 255, 255))
        main_menu_text_rect=main_menu_text.get_rect(center=state.main_menu_btn_rect.center)

        
        exit_text = font.render("Exit ", True, (255, 255, 255))
        exit_text_rect=exit_text.get_rect(center=state.exit_btn_rect.center)


        scor_text= font.render("Score: 0", True, (255, 255, 255))
        score_pos=((state.rwd_surface_width//2)-scor_text.get_width()//2,80)

        high_score= font.render("High Score: 0", True, (255, 255, 255))
        high_score_pos=((state.rwd_surface_width//2)-high_score.get_width()//2,120)


        died_text= font.render(" YOU HAVE BEEN DESTROYED ! ", True, (255, 255, 255))
        died_text_pos=((state.rwd_surface_width//2)-(died_text.get_width()//2),20)


        state.rewards_surface.blit(main_menu_text,main_menu_text_rect)
        state.rewards_surface.blit(exit_text,exit_text_rect)
        state.rewards_surface.blit(died_text,died_text_pos)
        state.rewards_surface.blit(scor_text,score_pos)
        state.rewards_surface.blit(high_score,high_score_pos)

class Screen():
    def draw(self,screen):
        pass
    def get_buttons(self):
        pass
    def draw_frames(self,screen):
        pass
    def handle_buttons(self):
        pass


class Game_modes_window(Screen):
    def __init__(self):
        self.image=pygame.image.load('src/img/GUI/background.png').convert_alpha()
        self.buttons=[]
        self.levels_buttoon=Button(150,150,"Levels")
        self.survival_buttonn=Button(150,220,"Survival")
        self.apex_button=Button(150,290,"Apex Challenge")
        self.back_button=Button(150,400,"Return")
        self.apex_play_button=None
        self.survival_play_button=None
        self.level_play_button=None
        
        self.buttons.extend([self.levels_buttoon, self.survival_buttonn, self.apex_button,self.back_button])
  
        self.selected_frame=False
        self.holding_button=None
        self.holding_play=False
        self.selected_level=False
        


    def draw(self,screen):
      screen.blit(self.image, (0,0))
      for button in self.buttons:
          button.place(screen)
    
    def get_buttons(self):
        return self.buttons
    
    def get_frames(self):
        return []

    def levels_frame(self,levels):
        levels_frame=Levels_Frame(300,125,715,390,3,5)
        for level in levels:
            levels_frame.add_level(level)

        self.selected_frame=levels_frame
    

    def level_description_frame(self,index,levels):
        self.selected_level=levels[index-1]
        description=Frame(300,125,715,390)
        description.write(self.selected_level.get_description())
        self.selected_frame=description
        level_play_button=Button(description.width-100,description.height+100,'Play')
        back_button=Button(description.width+200,description.height+100,'Back')
        self.level_play_button=level_play_button
        description.buttons.append(back_button)
        description.buttons.append(level_play_button)



    def survival_frame(self):
        survival_frame=Frame(300,125,715,390)
        survival_frame.write("Try to engage all enemies and get the best score you can.")
        self.selected_frame=survival_frame
        self.selected_frame=survival_frame
        survival_play_button=Button(survival_frame.width+25,survival_frame.height+100,'Play')
        self.survival_play_button=survival_play_button
        survival_frame.buttons.append(survival_play_button)
        
        



    def apex_frame(self):
        apex_frame=Frame(300,125,715,390)
        apex_frame.write("Coming soon...")
        self.selected_frame=apex_frame
        apex_play_button=Button(apex_frame.width+25,apex_frame.height+100,'Play')
        self.apex_play_button=apex_play_button
        apex_frame.buttons.append(apex_play_button)
        



    def draw_frames(self,screen):
        if self.selected_frame:
            self.selected_frame.draw(screen)
            self.selected_frame.draw_buttons(screen)


    def handle_buttons(self):
        self.holding_button=None
        if self.selected_frame:
            frame_buttons=self.selected_frame.get_buttons()
            for button in frame_buttons :
                if button.holding:
                    self.holding_button=button
                 
                    

        for button in self.buttons:
            if button.holding:
                self.holding_button=button

      
    
        
 
   
         

    def clear_selection(self):
        self.selected_frame=False

    




class Main_menu_screen(Screen):
    def __init__(self):
        self.buttons=[]
        self.holding_button=None
        self.frames=[]
        self.image=pygame.image.load('src/img/GUI/background.png').convert_alpha()
        self.play_button=Button(width//2,180,"Play")
        self.options_button=Button(width//2,260,"Options")
        self.Credits_button=Button(width//2,340,"Credits")
        self.Exit_button=Button(width//2,420,"Exit")
        self.buttons.extend([self.play_button, self.options_button, self.Credits_button,self.Exit_button])
        self.window=0

    def draw(self,screen):
      screen.blit(self.image, (0,0))
      for button in self.buttons:
          button.place(screen)
    
    def get_buttons(self):
        return self.buttons
    
    def get_frames(self):
        return self.frames
    
    def handle_buttons(self):
        self.holding_button=None
        for button in self.buttons:
            if button.holding:
                self.holding_button=button

    
    
  
 
    


