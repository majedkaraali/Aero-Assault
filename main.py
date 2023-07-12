import pygame
import random
from pygame.locals import *
import sys
import numpy as np
import math

pygame.init()

width=1100
height=640
rect = pygame.Rect(100, 20, 100, 20)
rect_color = (255, 0, 0)  # Red color
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Create game states
font = pygame.font.Font(None, 24)


pygame.mixer.init()





class Missile:
    width=5
    height=10
    vel_x=2
    vel_y=-3


    def __init__(self,x,y,target):
        self.x=x
        self.y=y
        self.targert=target
    
    def move_misile(self):
        if self.targert.x>self.x:
            self.x+=self.vel_x
        elif self.targert.x<self.x:
            self.x+=self.vel_x*-1
        else :
            self.x+=self.vel_x
        self.y+=self.vel_y

    def draw_missile(self):
        pygame.draw.rect(screen, ('red'), (self.x, self.y, self.width, self.height))



class Bullet:
    width = 3
    height = 7
    vel_y = -10

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_bullet(self):
        self.y += self.vel_y

    def draw_bullet(self):
        pygame.draw.rect(screen, ('black'), (self.x, self.y, self.width, self.height))


class Player():
    def __init__(self,x,y,bullets,missiles) :
        self.x=x
        self.y=y
        self.bullets=bullets
        self.missiles=missiles

    width=50
    height=50
    player_alive=True
    vel_x = 0
    vel_y = 0
    move_speed = 6
    
    shoot_delay = 100  
    last_shot_time = 0

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            vel_x = -self.move_speed
        elif keys[pygame.K_RIGHT]:
            vel_x = self.move_speed
        else:
            vel_x = 0

        self.x += vel_x
        self.x = max(0, min(self.x, width - self.width))
        
    def update_player(self):
        global pl
        pl = pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= self.shoot_delay

    def shoot(self):
        if self.can_shoot():
            bullet = Bullet(self.x + self.width // 2 - Bullet.width // 2, self.y)
            self.bullets.append(bullet)
            self.last_shot_time = pygame.time.get_ticks()

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move_bullet()

    def move_missiles(self):
        for mis in self.missiles:
            mis.move_misile()

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.draw_bullet()

    def update_missiles(self):
        for mis in self.missiles:
            mis.draw_missile()

    def radar(self):
        radar_range=300
        max_left=self.x-radar_range//2
        max_right=self.x+radar_range//2
        radar_angle=list(range(max_left,max_right))
        return radar_angle
    
    def lock_target(self):
        global enemies_in_radar
        get_enemies=FreePlayState.enemy_list
        enemies_in_radar=[]
        for enemy in get_enemies:
            if enemy.x in self.radar():
                enemies_in_radar.append(enemy)
                print("append in radar ")

        if len(enemies_in_radar)>0:        
            locked_target=enemies_in_radar[0]
            return locked_target
        else:
            return False
        
    

    def fire_missile(self):
        if self.lock_target():
            if self.can_shoot():
                locked=self.lock_target()
                missile_start_x=self.x
              
                missile_start_y=self.y
               
                missile=Missile(missile_start_x, missile_start_y,locked)
                self.missiles.append(missile)
                self.last_shot_time = pygame.time.get_ticks()
                print("append  list ")
        else:
            print("No")
      

    
        
        


class Enemy:
    def __init__(self,x,y,width,height,vel,move_dir):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=vel
        self.move_dir=move_dir

    def set_x(self,x):
        self.x=x
    def move_enemy(self):
    
        if self.move_dir=='right':
            if self.x<width-60:
                self.x+=self.vel


        elif self.move_dir=="left":
            if self.x>60:
                self.x+=self.vel


    def get_angle_between_rects(rect1, rect2):
        v1_x=(rect1.x)
        v1_y=(rect1.y)
        v2_x=(rect2.x)
        v2_y=(rect2.y)

        ddd=(v1_x*v2_x)+(v1_y*v2_y) 

        direction1 = math.atan2(rect1.centery - rect1.top, rect1.centerx - rect1.left)
        # Calculate the direction of the second rect.
        direction2 = math.atan2(rect2.centery - rect2.top, rect2.centerx - rect2.left)

        # Calculate the difference between the two directions.
        difference = direction2 - direction1

        # Convert the difference to degrees.
        angle = difference * 180 / math.pi

        # Return the angle.
        return ddd


    def update_enemy(self):
        global en
        en = pygame.draw.rect(screen, (29, 84, 158), (self.x, self.y, self.width, self.height))

    def check_collision(self, bullet_list):
        for bullet in bullet_list:
            if (self.x < bullet.x + bullet.width and
                self.x + self.width > bullet.x and
                self.y < bullet.y + bullet.height and
                self.y + self.height > bullet.y):
                return True
        return False










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
    #print('if current state is menu state this line must print')

    free_play_posit=pygame.Rect(20, 20, 200, 50)
    missions_posit= pygame.Rect(20, 90, 200, 50)
    exit_posit= pygame.Rect(20, 230, 200, 50)

    def __init__(self):
        super().__init__()

        self.running=True



        
    def handle_events(self, events):
        global current_state,p1
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.free_play_posit.collidepoint(mouse_pos):
                    print("Clicked Free Play button")
                #    self.running = False
               #     return "free_play"
                    
                    bulets=[]
                    missiles=[]
                    p1=Player(400,500,bulets,missiles)

                    print('new player',p1)
                    print(p1.x,p1.y,p1.bullets)
                    current_state=free_play_state
                 
                elif self.missions_posit.collidepoint(mouse_pos):
                    print("Clicked Missions button")
                    
                elif self.exit_posit.collidepoint(mouse_pos):
                    print("Clicked Exit button")
                    



    def draw(self):
        screen.fill('black')
        free_play_button = pygame.draw.rect(screen, (0, 0, 255),self.free_play_posit)
        free_play_text = font.render("Free Play", True, (255, 255, 255))
        free_play_text_rect = free_play_text.get_rect(center=free_play_button.center)
        screen.blit(free_play_text, free_play_text_rect)


        missions_button = pygame.draw.rect(screen, (0, 255, 0),self.missions_posit)
        missions_text = font.render("Missions", True, (255, 255, 255))
        missions_text_rect = missions_text.get_rect(center=missions_button.center)
        screen.blit(missions_text, missions_text_rect)



        exit_button = pygame.draw.rect(screen, (255, 0, 0),self.exit_posit)
        exit_text = font.render("Exit", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, exit_text_rect)
            
       
     

class FreePlayState(GameState):
    paues=False
    pause_frame_color = ('silver')
    pause_surface_width=250
    pause_surface_height=150
    frame_position = ((width//2)-(pause_surface_width//2),(height//2)-(pause_surface_height//2))
    frame_surface = pygame.Surface((pause_surface_width,pause_surface_height))
    frame_surface.fill(pause_frame_color)
    border_width = 1
    border_color = (0, 0, 0)

    resume_button_rect=pygame.Rect(75, 20, 100, 20)
    main_menu_button_rect=pygame.Rect(75, 60, 100, 20)
    exit_button_rect=pygame.Rect(75, 100, 100, 20)

    enemy_list=[]

    def __init__(self):
        super().__init__()
        self.running=True
        
    def handle_events(self, events):
        global current_state
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                adjusted_mouse_pos = (
                    mouse_pos[0] - self.frame_position[0],
                    mouse_pos[1] - self.frame_position[1]
                )
                if self.resume_button_rect.collidepoint(adjusted_mouse_pos):
                    print("Resume button clicked!")
                    self.paues = False

                elif self.main_menu_button_rect.collidepoint(adjusted_mouse_pos):
                    print("Back to menu")
                    current_state = menu_state  # Update the current state
                    self.paues = False
                    self.enemy_list.clear()
                #    return  # Exit the handle_events method

                elif self.exit_button_rect.collidepoint(adjusted_mouse_pos):
                    print("Exit")
                    self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.paues:
                        self.paues = False
                    else:
                        self.paues = True
    
    def generate_enemies(self,num_of_enemies):
        if len(self.enemy_list)<num_of_enemies:
            move_dircton=random.randint(0,1)
            if move_dircton==1:
                vel=2
                x=random.randint(-350,-50)
                mdir='right'
            else:
                vel=-2
                x=random.randint(width+50,width+350)
                mdir='left'
        
            enemy=Enemy(x,10,50,50,vel,mdir)
            self.enemy_list.append(enemy)


    def draw(self):

        if not (self.paues):
            clock.tick(60)
            screen.fill('aqua')

            p1.move_player()
            p1.update_player()
            p1.move_bullets() 
            p1.update_bullets()
            p1.move_missiles()
            p1.update_missiles()
            #print(pl)
            
           # p1.fire_missile()
            self.generate_enemies(1)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                p1.shoot()
            elif keys[pygame.K_f]:
                p1.fire_missile()


            enemies_to_remove = []
            bullets_to_remove = []

            for enemy in self.enemy_list:
                if enemy.check_collision(p1.bullets):
                    enemies_to_remove.append(enemy)

            for bullet in p1.bullets:
                if bullet.y < 0:
                    bullets_to_remove.append(bullet)

            for enemy in self.enemy_list:
                pass

            for enemy in enemies_to_remove:
                self.enemy_list.remove(enemy)

            for bullet in bullets_to_remove:
                p1.bullets.remove(bullet)

        
            for enemy in self.enemy_list:
                enemy.move_enemy()
                enemy.update_enemy()

            p1.update_bullets()
            #print(en)
            #print(pl)
            #print(Enemy.get_angle_between_rects(pl,en))

        elif (self.paues):

            pygame.draw.rect(self.frame_surface,self.border_color, self.frame_surface.get_rect(), self.border_width)
            screen.blit(self.frame_surface, self.frame_position)


            resume_button = pygame.draw.rect(self.frame_surface, (0, 0, 255),self.resume_button_rect)
            resume_button_text = font.render("Resume", True, (255, 255, 255))
            resume_button_text_rect = resume_button_text.get_rect(center=resume_button.center)
           

            mainmenu_button=pygame.draw.rect(self.frame_surface,(0, 0, 255),self.main_menu_button_rect)
            mainmenu_button_text=font.render("Main menu", True, (255, 255, 255))
            mainmenu_button_text_rect=mainmenu_button_text.get_rect(center=mainmenu_button.center)

            exit_button=pygame.draw.rect(self.frame_surface,(0, 0, 255),self.exit_button_rect)
            exit_button_text=font.render("Exit", True, (255, 255, 255))
            exit_button_text_rect=exit_button_text.get_rect(center=exit_button.center)


            self.frame_surface.blit(resume_button_text,resume_button_text_rect)
            self.frame_surface.blit(mainmenu_button_text,mainmenu_button_text_rect)
            self.frame_surface.blit(exit_button_text,exit_button_text_rect)
            
           
            
            
          

menu_state = MenuState()
free_play_state = FreePlayState()
current_state = menu_state

while current_state.running:
    
    events = pygame.event.get()
   
  #  next_state = None  # Initialize next_state variable

    for event in events:
        if event.type == pygame.QUIT:
            current_state.running = False

    
    
    next_state = current_state.handle_events(events)
    current_state.update()
    current_state.draw()




    pygame.display.flip()
    




pygame.quit()
