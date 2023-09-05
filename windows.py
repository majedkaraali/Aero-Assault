import pygame
from GUI import Button,Frame,Levels_Frame
import json


pygame.init()
width,height=1100,660
gui=pygame.image.load('src/img/GUI/background2.png').convert_alpha()

from levels import levels


def get_highest_score(): 

    try:
        with open('data.json', 'r') as progress_file:
            data = json.load(progress_file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    highest_score=data['highest_score']
    

    return highest_score



def get_completed_levels(): 

    try:
        with open('data.json', 'r') as progress_file:
            data = json.load(progress_file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    completed_levels=data['completed_levels']
    

    return completed_levels



def update_highest_score(new_score):
    # Read the JSON data from the file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Update the "highest_score" field
    data["highest_score"] = new_score

    # Write the updated JSON data back to the file
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

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
        self.smooth_frame=pygame.image.load('src/img/GUI/smooth_frame.png').convert_alpha()
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


    def finish_levels_window(self):
        finish_frame=Frame(self.center[0]-self.pause_image.get_width()//2,self.center[1]-self.pause_image.get_height()//2,self.pause_image.get_width(),self.pause_image.get_height())
        finish_frame.confing(self.pause_image)
        self.main_menu_button.change_images(self.smooth_button,self.smooth_button_hold)
        finish_frame.add_button(self.main_menu_button)
 
    
        finish_frame.write("Congrats! All Levels Completed")
        self.selected_window=finish_frame  



    def tutorial_window(self,image_path):
 
        image=pygame.image.load(image_path).convert_alpha()
        tuturial=Frame(self.center[0]-image.get_width()//2,self.center[1]-image.get_height()//2,image.get_width(),image.get_height())
        tuturial.confing(image)


        self.ok_button.change_images(self.smooth_button,self.smooth_button_hold)
        tuturial.add_button(self.ok_button)

        self.selected_window=tuturial   

    def level_lose_window(self):
        lose_frame=Frame(self.center[0]-self.pause_image.get_width()//2,self.center[1]-self.pause_image.get_height()//2,self.pause_image.get_width(),self.pause_image.get_height())
        lose_frame.confing(self.pause_image)
        self.retry.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_location(self.center[0]-65,self.center[1]+40)
        lose_frame.add_button(self.main_menu_button)
        lose_frame.add_button(self.retry)

        lose_frame.write("Game Over")
        self.selected_window=lose_frame    


    def survival_lose_window(self,screen,score):
        topleft=self.center[0]-self.smooth_frame.get_width()//2,self.center[1]-self.smooth_frame.get_height()//2
        center=self.center[0],self.center[1]

        lose_frame=Frame(topleft[0],topleft[1],self.smooth_frame.get_width(),self.smooth_frame.get_height())
        lose_frame.confing(self.smooth_frame)
        self.retry.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_images(self.smooth_button,self.smooth_button_hold)
        self.main_menu_button.change_location(self.center[0]-65,self.center[1]+40)
        lose_frame.add_button(self.main_menu_button)
        lose_frame.add_button(self.retry)
        score =str(score)

        hq=get_highest_score()

        lose_frame.add_line("GAME OVER!",center[0],center[1]-100,True,'white',True)
        lose_frame.add_line(f"Score: {score}",center[0],center[1]-50,False,'white',True)
        lose_frame.add_line(f" Height Score: {hq}",center[0],center[1]-20,False,'white',True)
      
        self.selected_window=lose_frame  

        if int(hq)<int(score):
            update_highest_score(int(score))
           


    def in_game_level_description_frame(self,level):
        _level=level
        description=Frame(self.center[0]-357,self.center[1]-195,715,390)
        description.write(_level.get_description())
        self.ok_button=Button(description.width-65,description.height+100,'Conform',22)
        self.ok_button.change_images(self.smooth_button,self.smooth_button_hold)
        self.selected_window=description
        description.add_button(self.ok_button)

    def survival_description_frame(self):
            description=Frame(self.center[0]-357,self.center[1]-195,715,390)
            description.write('Try to get best score and take down  enemies aircrafts without being bombed, GOOD LUCK')
            self.ok_button=Button(description.width-65,description.height+100,'Conform',22)
            self.ok_button.change_images(self.smooth_button,self.smooth_button_hold)
            self.selected_window=description
            description.add_button(self.ok_button)
        
    def draw_frames(self, screen):
        if self.selected_window:
            self.selected_window.draw(screen)
            self.selected_window.draw_buttons(screen)
    

    def draw(self, screen):
        pass

class Test():
    def __init__(self):
        self.name='gamemode'
        self.image=pygame.image.load('src/img/GUI/background2.png').convert_alpha()
        self.smooth_edge_frame=pygame.image.load('src/img/GUI/smooth_frame.png').convert_alpha()
        self.acvm_img=pygame.transform.scale(self.smooth_edge_frame, (350, 350))
        self.buttons=[]
        self.levels_buttoon=Button(150,150,"Levels",22)
        self.survival_buttonn=Button(150,220,"Survival",22)
        self.apex_button=Button(150,290,"Apex Challenge",22)
        self.back_button=Button(150,400,"Return",22)

        self.play_button=Button(width//2,180,"Play",22)
        self.options_button=Button(width//2,260,"Options",22)
        self.Credits_button=Button(width//2,340,"Credits",22)
        self.Exit_button=Button(width//2,420,"Exit",22)
        self.game_modes_buttons=[self.levels_buttoon, self.survival_buttonn, self.apex_button,self.back_button]
        self.menu_buttons=[self.play_button, self.options_button, self.Credits_button,self.Exit_button]
        self.apex_play_button=None
        self.survival_play_button=None
        self.level_play_button=None
        
        
        
  
        self.selected_frame=False
        self.selected_frame_button=None
        self.holding_play=False
        self.selected_level=False
        
        self.selected_game_mode=None


    
    def get_buttons(self):
        return self.buttons
    
    def get_frames(self):
        return []


     
    def main_menu(self):
        self.buttons=self.menu_buttons
        
        



    def game_modes(self):
        
        self.buttons=self.game_modes_buttons



    def levels_frame(self,levels):
        
        levels_frame=Levels_Frame(300,125,715,390,3,5,levels)

        self.selected_frame=levels_frame

        

    def level_description_frame(self,index,levels):
        index=int(index)
        selected_level=levels[index-1]

        description=Frame(300,125,715,390)
        description.write(selected_level.get_description())
        self.selected_frame=description
        level_play_button=Button(description.width-100,description.height+100,'Play',22)
        back_button=Button(description.width+200,description.height+100,'Back',22)
        self.level_play_button=level_play_button
        description.buttons.append(back_button)
        description.buttons.append(level_play_button)





    def game_mode_description_frame(self,description_text):
        description=Frame(300,125,715,390)
        description.write(description_text)
        self.selected_frame=description
        level_play_button=Button(description.width-100,description.height+100,'Play',22)
        back_button=Button(description.width+200,description.height+100,'Back',22)
        self.level_play_button=level_play_button
        description.buttons.append(back_button)
        description.buttons.append(level_play_button)

    def survival_frame(self):
        survival_frame=Frame(300,125,715,390)
        competed_levels=get_completed_levels()
       
        
        self.selected_frame=survival_frame
        level_play_button=Button(survival_frame.width+25,survival_frame.height+100,'Play',22)
        self.level_play_button=level_play_button

        if len(competed_levels)<5:
            survival_frame.write("You must complete 5. levels to unluck this game mode.")
            level_play_button.lock()

        else:
            survival_frame.write("Try to engage all enemies and get the best score you can.")

        survival_frame.buttons.append(level_play_button)
            

      


    def apex_frame(self):
        apex_frame=Frame(300,125,715,390)
        apex_frame.write("Coming soon...")
        self.selected_frame=apex_frame
        apex_play_button=Button(apex_frame.width+25,apex_frame.height+100,'Play',20)
        self.apex_play_button=apex_play_button
        apex_frame.buttons.append(apex_play_button)
        apex_play_button.lock()


    def achvm(self):
        hq=get_highest_score()
        completed_levels=len(get_completed_levels())
        levels_leng=len(levels)


        frame=Frame(42,142,350,350)
        frame.confing(self.acvm_img)
        frame.add_line('Achievements',42+self.acvm_img.get_width()//2,165,True,(255,210,100),True)
        frame.add_line('Completed Levels: ',55,200,False,(255,255,255),False)
        frame.add_line('Highest score: ',55,250,False,(255,255,255),False)
        frame.add_line('Apex Challenge:  ',55,300,False,(255,255,255),False)

        frame.add_line(f'  {completed_levels}/{levels_leng}',275,200,False,'#fee300',False)
        frame.add_line(f'  {hq}',230,250,False,'#fee300',False)
        frame.add_line('  Wave 0',245,300,False,'#fee300',False)

        self.selected_frame=frame
        
        

    def draw(self,screen):
    
        screen.blit(self.image, (0,0))
        for button in self.buttons:
            button.place(screen)

    def draw_frames(self,screen):
        if self.selected_frame:
            self.selected_frame.draw(screen)
            self.selected_frame.draw_buttons(screen)

        


    def handle_buttons(self):
        

        if self.selected_frame:
           self.selected_frame_button=self.selected_frame.selected_button
           
                    

      
    
        
    def clear_selection(self):
        self.selected_frame=False

    





    
    
  
 
    


