import pygame
from GUI import Button,Frame,Levels_Frame
pygame.init()
width,height=1100,660
gui=pygame.image.load('src/img/GUI/background.png').convert_alpha()

font = pygame.font.Font(None, 24)



class Screen():
    def draw(self,screen):
        pass
    def get_buttons(self):
        pass
    def draw_frames(self,screen):
        pass
    def handle_buttons(self):
        pass
    
class game_windows(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.pause_image=pygame.image.load('src/img/GUI/pause_frame.png').convert_alpha()
        self.buttons=[]
        self.center=(width//2,height//2)
        self.resume_button=Button(self.center[0],self.center[1]-50,'Resume',18)
        self.options_button=Button(self.center[0],self.center[1]-5,'Options',18)
        self.main_menu_button=Button(self.center[0],self.center[1]+40,'Main Menu',18)
        self.next_level=Button(self.center[0]+65,self.center[1]+40,'Next Level',18)
        self.retry=Button(self.center[0]+65,self.center[1]+40,'Retry',18)
        self.ok_button=Button(self.center[0],self.center[1]+217,'OK',18)

        self.buttons.extend([self.resume_button,self.options_button,])
        self.smooth_button=pygame.image.load('src/img/GUI/smooth_button.png')
        self.smooth_button_hold=pygame.image.load('src/img/GUI/smooth_button_holding.png')
        self.selected_window=False

    
    def puse_window(self):

        pause_frame=Frame(self.center[0]-self.pause_image.get_width()//2,self.center[1]-self.pause_image.get_height()//2,self.pause_image.get_width(),self.pause_image.get_height())
        pause_frame.confing(self.pause_image)
        self.resume_button.change_images(self.smooth_button,self.smooth_button_hold)
        self.options_button.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_location(self.center[0],self.center[1]+40)
        pause_frame.add_button(self.main_menu_button)
        pause_frame.add_button(self.resume_button)
        pause_frame.add_button(self.options_button)
        self.selected_window=pause_frame

    def reward_window(self):
        reward_frame=Frame(self.center[0]-self.pause_image.get_width()//2,self.center[1]-self.pause_image.get_height()//2,self.pause_image.get_width(),self.pause_image.get_height())
        reward_frame.confing(self.pause_image)
        self.next_level.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_location(self.center[0]-65,self.center[1]+40)
        reward_frame.add_button(self.main_menu_button)
        reward_frame.add_button(self.next_level)
    
        reward_frame.write("Level Completed")
        self.selected_window=reward_frame  


    def tutorial_window(self,image_path):
 
        image=pygame.image.load(image_path).convert_alpha()
        tuturial=Frame(self.center[0]-image.get_width()//2,self.center[1]-image.get_height()//2,image.get_width(),image.get_height())
        tuturial.confing(image)


        self.ok_button.change_images(self.smooth_button,self.smooth_button_hold)
        tuturial.add_button(self.ok_button)

        self.selected_window=tuturial   

    def lose_window(self):
        lose_frame=Frame(self.center[0]-self.pause_image.get_width()//2,self.center[1]-self.pause_image.get_height()//2,self.pause_image.get_width(),self.pause_image.get_height())
        lose_frame.confing(self.pause_image)
        self.retry.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_location(self.center[0]-65,self.center[1]+40)
        lose_frame.add_button(self.main_menu_button)
        lose_frame.add_button(self.retry)
    
        lose_frame.write("Game Over")
        self.selected_window=lose_frame     

        
    def draw_frames(self, screen):
        if self.selected_window:
            self.selected_window.draw(screen)
            self.selected_window.draw_buttons(screen)
    

    def draw(self, screen):
        pass

class Game_modes_window(Screen):
    def __init__(self):
        self.name='gamemode'
        self.image=pygame.image.load('src/img/GUI/background.png').convert_alpha()
        self.buttons=[]
        self.levels_buttoon=Button(150,150,"Levels",22)
        self.survival_buttonn=Button(150,220,"Survival",22)
        self.apex_button=Button(150,290,"Apex Challenge",22)
        self.back_button=Button(150,400,"Return",22)
        
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
        level_play_button=Button(description.width-100,description.height+100,'Play',22)
        back_button=Button(description.width+200,description.height+100,'Back',22)
        self.level_play_button=level_play_button
        description.buttons.append(back_button)
        description.buttons.append(level_play_button)



    def survival_frame(self):
        survival_frame=Frame(300,125,715,390)
        survival_frame.write("Try to engage all enemies and get the best score you can.")
        self.selected_frame=survival_frame
        survival_play_button=Button(survival_frame.width+25,survival_frame.height+100,'Play',22)
        self.survival_play_button=survival_play_button
        survival_frame.buttons.append(survival_play_button)
        
        



    def apex_frame(self):
        apex_frame=Frame(300,125,715,390)
        apex_frame.write("Coming soon...")
        self.selected_frame=apex_frame
        apex_play_button=Button(apex_frame.width+25,apex_frame.height+100,'Play',20)
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

    




class Main_menu_window(Screen):
    def __init__(self):
        self.name='menu'
        self.buttons=[]
        self.holding_button=None
        self.frames=[]
        self.image=pygame.image.load('src/img/GUI/background.png').convert_alpha()
        self.play_button=Button(width//2,180,"Play",22)
        self.options_button=Button(width//2,260,"Options",22)
        self.Credits_button=Button(width//2,340,"Credits",22)
        self.Exit_button=Button(width//2,420,"Exit",22)
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

    
    
  
 
    


