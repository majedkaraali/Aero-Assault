import pygame
import random
from pygame.locals import *
from math import atan2, degrees, pi
import math

pygame.init()

width=1100
height=660


screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
score=0
pygame.mixer.init()


pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)



class Missile:
    width=5
    height=17
    vel_x=2
    vel_y=-4

    def __init__(self,x,y,target):
        self.x=x
        self.y=y
        self.target=target

    def hit_target(self):
        if not (self.target.destroyed):
            rect=pygame.Rect(self.x,self.y,self.width,self.height)
            if rect.colliderect(self.target.get_rect()):
                self.target.destroyed=True
                return True
                
            else:
                return False

    def get_rect(self):
        rect=pygame.Rect(self.x,self.y,self.width,self.height)
        return  rect
    
    
    def path(self):
        enemy_dir=self.target.move_dir
        eny=(self.target.y)-self.target.height//2
        y_dis=self.y-eny
        y_dis=abs(y_dis)
        
        reach_target_time=y_dis//self.vel_y
        reach_target_time=abs(reach_target_time)

        if enemy_dir=="left":
            cx=((self.target.x)-reach_target_time)
           
        elif enemy_dir=="right":
            cx=((self.target.x)+reach_target_time)+50
        
        self.target.tracked=True
        return cx

    def turn_vel(self):
        eny=(self.target.y)-self.target.height//2
        y_dis=self.y-eny
        y_dis=abs(y_dis)

        reach_target_time=y_dis//self.vel_y
        reach_target_time=abs(reach_target_time)

        x_path_dist=self.path()-self.x
        x_path_dist=abs(x_path_dist)

        if reach_target_time and x_path_dist >0:
            missiile_x_turn_vel=x_path_dist/reach_target_time
        else:
            missiile_x_turn_vel=2


        if self.path()>self.x:
            self.x+=missiile_x_turn_vel+1
        elif self.path()<self.x:
            self.x-=missiile_x_turn_vel-1

        return  missiile_x_turn_vel 

    def move_misile(self):

        if self.path()>self.x:
            self.x+=self.turn_vel()+1
        elif self.path()<self.x:
            self.x-=self.turn_vel()-1

        self.y+=self.vel_y

        #pygame.draw.rect(screen, ('red'), (self.path(), self.target.y, 5, 5)) # THis is collisin point

    def draw_missile(self):
        width = self.width
        height = self.height
        rect = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect, pygame.Color('blue'), (0, 0, width, height))

        if self.target.move_dir=="left":
            angle = self.target.get_angle_between_rects(self.get_rect(),self.target.get_rect())+90
        else:
            angle = self.target.get_angle_between_rects(self.get_rect(),self.target.get_rect())+45

        if (self.target.destroyed):
                angle = 0

        rotated_rect = pygame.transform.rotate(rect, angle)
        x_adjustment = (rotated_rect.get_width() - width) // 2
        y_adjustment = (rotated_rect.get_height() - height) // 2

        screen.blit(rotated_rect, (self.x - x_adjustment,self.y - y_adjustment))
             


class Bullet:
    width = 3
    height = 4
    speed = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.max_y=0
        self.max_x=0
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect=pygame.draw.rect(self.surface, pygame.Color('black'), (0, 0, self.width, self.height))
        self.hitted=False
       

    def move_bullet(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.max_y+=self.vel_y
        self.max_x+=self.vel_x
        #print(self.vel_x,self.vel_y)


    def draw_bullet(self):
        screen.blit(self.surface, (self.x, self.y))

    def shoot_at(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed

    def out_of_range(self):

        x_y=abs(self.max_x)+abs(self.max_y)


        if x_y>700:
            return True

        if abs(self.max_y)>370:
            return True
        if abs(self.max_x)>550:
        
            return True
        else:
            return False

    def rotate_bullet(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        angle = math.degrees(math.atan2(dy, dx)) + 90

        rotated_surface = pygame.transform.rotate(self.surface, angle)
        x_adjustment = (rotated_surface.get_width() - self.width) // 2
        y_adjustment = (rotated_surface.get_height() - self.height) // 2

        screen.blit(rotated_surface, (self.x - x_adjustment, self.y - y_adjustment))
       


class Player():
    def __init__(self,x,y,bullets,missiles) :
        self.x=x
        self.y=y
        self.bullets=bullets
        self.missiles=missiles
        self.attacked_targets=[]
        self.enemies_in_radar=[]
        self.tracked=[]
        self.selected=0
        self.bullets_count=1080
        self.magazine=120
        self.reloading=False

    width=60
    height=33
    player_alive=True
    vel_x = 0
    vel_y = 0
    move_speed = 6
    shoot_delay = 100  
    last_shot_time = 0
    fire_missie_delay=200
    last_fire_time=0

    reload_delay=4000
    reload_start_time=0
    


    def get_centerx(self):
        center_x=self.x+(self.width//2)
        return center_x

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            vel_x = -self.move_speed
        elif keys[pygame.K_d]:
            vel_x = self.move_speed
        else:
            vel_x = 0

        self.x += vel_x
        self.x = max(0, min(self.x, width - self.width))
        
    def update_player(self):
        global pl
        pl = pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.radar()

            

        
    def reload(self):
        current_time = pygame.time.get_ticks()
        if self.reload_start_time+self.reload_delay<=current_time:
            self.magazine=120
            self.bullets_count-=120
        else:
            self.magazine='---'


    def chek_magazine(self):
        if self.magazine != '---':
            if self.magazine<0:
                self.reload()
                self.reloading=True
            else:
                self.reloading=False

   

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        
        if not self.reloading:
            if current_time - self.last_shot_time >= self.shoot_delay:
                return True
        else:
            return False
        

    
    def can_fire_missile(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_fire_time >= self.fire_missie_delay


    def shoot(self):
        if self.can_shoot():
            self.magazine-=2
            target_x, target_y = pygame.mouse.get_pos()
            bullet = Bullet(self.x + self.width // 2 - Bullet.width // 2, self.y)
            bullet2 = Bullet(20+self.x + self.width // 2 - Bullet.width // 2, self.y)
            bullet.shoot_at(target_x, target_y)
            bullet.rotate_bullet(target_x,target_y)
            bullet2.shoot_at(target_x, target_y)
            bullet2.rotate_bullet(target_x,target_y)
            self.bullets.append(bullet)
            self.bullets.append(bullet2)
            self.last_shot_time = pygame.time.get_ticks()
            self.reload_start_time=self.last_shot_time
            
            

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
        radar_range=900
        max_left=self.x-radar_range//2
        max_right=self.x+radar_range//2
        radar_angle=list(range(max_left,max_right))
        rd=  pygame.draw.rect(screen, ('green'), (max_left, 10, radar_range , 2))
        enemies_list=free_play_state.get_enemies()
        self.enemies_in_radar=[]

        for enemy in enemies_list:
            if enemy.get_centerx() in radar_angle and enemy.y < 300:
                    #enemy.tracked=True
                    self.enemies_in_radar.append(enemy)
                    if enemy not in self.tracked :
                            if enemy not in self.attacked_targets:
                                self.tracked.append(enemy)

        for target in self.tracked:
            if target.destroyed==True:
                self.tracked.remove(target)
            elif target.get_centerx() not in radar_angle:
                target.tracked=False
                self.tracked.remove(target)
            elif target in self.attacked_targets:
                self.tracked.remove(target)
            
        
        locked=self.auto_lock()

        if locked:
            for target in self.tracked:
                if target==locked:
                    locked.tracked=True
                else:
                    target.tracked=False


    def next_lock(self):
        searched_enemies=self.tracked
        enemies_count=len(searched_enemies)
        if ((self.selected)+1)>=(enemies_count):
            self.selected=0
        else:
            self.selected+=1
        
    def auto_lock(self):
        searched_enemies=self.tracked
        enemies_count=len(searched_enemies)
        if enemies_count>0:
            if self.selected>=enemies_count:
                locked=searched_enemies[0]
            else:
                locked=searched_enemies[self.selected]
            return locked
        
        else:
            return False
    
 
    
    
    def fire_missile(self):
        if self.can_fire_missile():
            if self.auto_lock():
                locked=self.auto_lock()
                missile_start_x=self.x
                missile_start_y=self.y
               
                missile=Missile(missile_start_x, missile_start_y,locked)
                self.missiles.append(missile)
                self.last_fire_time = pygame.time.get_ticks()
                locked.locked=True
                self.attacked_targets.append(locked)



class Bomb:
    def __init__(self,x,y,velx,vely):
        self.x=x
        self.y=y
        self.width=4
        self.height=6
        self.velx=velx
        self.vely=vely

    def move(self):
        self.y+=self.vely
        self.x+=self.velx
        #print(self.velx,self.vely)
        #print('moving')

    def draw(self):
        pygame.draw.rect(screen, pygame.Color('black'), (self.x, self.y, self.width, self.height))
        #print('drawing')

    

class Enemy:
    def __init__(self,x,y,width,height,vel,move_dir):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=vel
        self.move_dir=move_dir
        self.destroyed=False
        self.tracked=False
        self.locked=False
        self.bomb_dely=250
        self.last_bomb_time=0
        self.bomb_count=3
        self.health=100
        self.damaged=False
        
    bombs=[]



    def get_centerx(self):
        center_x=self.x+(self.width//2)
        return center_x
    
    def move_bombs(self):
        for bomb in self.bombs:
            bomb.move()
            if bomb.y>height-50:
                self.bombs.remove(bomb)
    
    def draw_bombs(self):
        for bomb in self.bombs:
            bomb.draw()
          
    


    def can_bomb(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_bomb_time >= self.bomb_dely
    
    def bomb(self,target):
        if self.can_bomb():
            distance_x=self.get_centerx()-target.x
            distance_x=abs(distance_x)
            distance_y=abs(self.y)-abs(target.y)
            target_x=target.get_centerx()
            target_attak_range=list(range(target_x-50,target_x+50))
            y_vel=1
            x_vel=1

            reach_time=distance_y//y_vel
            reach_time=abs(reach_time)
            
            if self.move_dir=="right":
                reach_x=self.x+reach_time//x_vel
            else:
                reach_x=self.x-reach_time//x_vel

          
            if reach_x in target_attak_range :
                if self.can_bomb():
                    if self.bomb_count>0:
                        if self.move_dir=='right':
                            bomb=Bomb(self.get_centerx(),self.y,x_vel,y_vel)
                        else:
                            bomb=Bomb(self.get_centerx(),self.y,-x_vel,y_vel)

                        self.bombs.append(bomb)
                        self.last_bomb_time = pygame.time.get_ticks()
                        self.bomb_count-=1
    


    def set_x(self,x):
        self.x=x
    def move_enemy(self):
    
        if self.move_dir=='right':
            if self.x<width+1:
                self.x+=self.vel


        elif self.move_dir=="left":
            if self.x>-1:
                self.x+=self.vel

    def get_rect(self):
        rect=pygame.Rect(self.x,self.y,self.width,self.height)
        return  rect
    
    def get_angle_between_rects(self,rect1, rect2):

        v1_x=(rect1.x)
        v1_y=(rect1.y)
        v2_x=(rect2.x)
        v2_y=(rect2.y)

        dx = v2_x - v1_x
        dy = v2_y - v1_y
        rads = atan2(-dy,dx)
        rads %= 2*pi
        degs = degrees(rads)

        return degs


    def update_enemy(self):
        target_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, "blue", target_rect)
        text = pygame.font.SysFont(None, 24).render("", True, (0, 0, 0))


        if self.locked:
            pygame.draw.rect(screen, "blue", target_rect)
            text = pygame.font.SysFont(None, 24).render("x", True, ('red'))

        elif self.tracked:
            pygame.draw.rect(screen, "blue", target_rect)
            text = pygame.font.SysFont(None, 24).render("O", True, ('green'))
        text_rect = text.get_rect(center=target_rect.center)
        screen.blit(text, text_rect)

    
    def is_taken_damage(self):
        if self.damaged==True:
            return True
        else:
            return False

    def check_collision(self, obje):
        global score
        for bullet in obje:
            if (self.x < bullet.x + bullet.width and
                self.x + self.width > bullet.x and
                self.y < bullet.y + bullet.height and
                self.y + self.height > bullet.y):
                bullet.hitted=True

                self.health-=15
                score+=5
                if self.health<0:
                    self.destroyed=True
                    score+=40
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

                    
                    bulets=[]
                    missiles=[]
                    p1=Player(400,height-70,bulets,missiles)

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
    mouse_button_pressed=False
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
    
    score_rect=pygame.Rect(35, height-15, 100, 20)
    menu_rect=pygame.Rect((width//2), height-15, 100, 66)
    missile_count_rect=pygame.Rect(width-50, height-15, 50, 66)
    bullet_count_rect=pygame.Rect(width-150, height-15, 50, 66)
    scorevalue_rect=pygame.Rect(80, height-15, 100, 20)

    enemy_list=[]

    def __init__(self):
        super().__init__()
        self.running=True
        
    def handle_events(self, events):
        global current_state
        tab_pressed = False
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_pressed=True
                mouse_pos = pygame.mouse.get_pos()
                adjusted_mouse_pos = (
                    mouse_pos[0] - self.frame_position[0],
                    mouse_pos[1] - self.frame_position[1]
                )

                if self.paues:
                    if self.resume_button_rect.collidepoint(adjusted_mouse_pos):
                        
                        print("Resume button clicked!")
                        self.paues = False

                    elif self.main_menu_button_rect.collidepoint(adjusted_mouse_pos):
                        print("Back to menu")
                        current_state = menu_state  # Update the current state
                        self.paues = False
                        self.enemy_list.clear()
                

                    elif self.exit_button_rect.collidepoint(adjusted_mouse_pos):
                        print("Exit22")
                        self.running = False
                   
       
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_pressed = False
                
    

            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.paues:
                        self.paues = False
                    else:
                        self.paues = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_TAB] and not tab_pressed:
                    p1.next_lock()
                    tab_pressed = True

            elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        tab_pressed = False

        if self.mouse_button_pressed:
                p1.shoot()
    
    def generate_enemies(self,num_of_enemies):
        y_spawns=[5,33,60,90,120,150,180,210,240,270,300,330,370,400,430,470,500]
        
        if len(self.enemy_list)<num_of_enemies:
            move_dircton=random.randint(0,1)
            
            if move_dircton==1:
                x_spawns=[-500,-300,-200,-100,-400]
                x=random.choice(x_spawns)-40
                mdir='right'
                vel=2



            else:
                x_spawns=[width+500,width+300,width+200,width+100,width+400]
                x=random.choice(x_spawns)+40
                mdir='left'
                vel=-2
          
                

            y=random.choice(y_spawns)
            enemy=Enemy(x,y,80,25,vel,mdir)
            self.enemy_list.append(enemy)

    def get_enemies(self):
        return self.enemy_list
    
    def ground(self):
        surface_width = width
        surface_height = 80
        ground_surface = pygame.Surface((surface_width, surface_height))
        ground_surface.fill(pygame.Color('green'))
        border = 1
        position = (0, height-surface_height)

        pygame.draw.rect(ground_surface, pygame.Color('green'), ground_surface.get_rect(), border)
        screen.blit(ground_surface, position)

    def statics(self):
        global score
        surface_width = width
        surface_height = 30
        startic_surface = pygame.Surface((surface_width, surface_height))
        startic_surface.fill(pygame.Color('lightgreen'))
        border = 1
        position = (0, height-30)

        pygame.draw.rect(startic_surface, pygame.Color('lightgreen'), startic_surface.get_rect(), border)
        screen.blit(startic_surface, position)
        score_value =str(score)

        score_text = font.render("Score: "+score_value, True, ('black'))
        score_text_pos=(10,height-25)

        menu_text = font.render("menu", True, 'black')
        menu_text_pos=(width//2,height-25)
        menurect=menu_text.get_rect()

        magazine=str(p1.magazine)
        bullets=str(p1.bullets_count)

        bullets_text = font.render(f"bullets: {magazine}/{bullets}", True, 'black')
        bullets_text_pos=(width-150,height-25)

        missiles_text = font.render("missiles: 0", True, 'black')
        missiles_text_pos=(width-300,height-25)
      
        screen.blit(score_text,score_text_pos)
        screen.blit(menu_text, menu_text_pos)
        screen.blit(bullets_text, bullets_text_pos)
        screen.blit(missiles_text, missiles_text_pos)


           



    def draw(self):
        

        if not (self.paues):
            clock.tick(60)
            screen.fill('aqua')
            self.ground()
            self.statics()

            p1.move_player()
            p1.update_player()
            p1.move_bullets() 
            p1.update_bullets()
            p1.move_missiles()
            p1.update_missiles()
            p1.chek_magazine()

 
            self.generate_enemies(4)
            
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                p1.shoot()
            elif keys[pygame.K_f]:
                p1.fire_missile()
                
       


            enemies_to_remove = []
            bullets_to_remove = []
            missiles_to_remove=[]


            for enemy in self.enemy_list:
                if enemy.check_collision(p1.bullets):
                    enemies_to_remove.append(enemy)
                if enemy.move_dir=='left':
                    if enemy.x<0:
                        enemy.destroyed=True
                        enemies_to_remove.append(enemy)
                 
                elif enemy.move_dir=='right':
                    if enemy.x>width:
                        enemy.destroyed=True
                        enemies_to_remove.append(enemy)
                        
             

            for bullet in p1.bullets:
                if bullet.out_of_range():
                    bullets_to_remove.append(bullet)
    
                elif bullet.hitted:
                    bullets_to_remove.append(bullet)



            for missile in  p1.missiles:
                if missile.y<=-10:
                    missiles_to_remove.append(missile)
                elif missile.hit_target():
                    missiles_to_remove.append(missile)
                    enemies_to_remove.append(missile.target)
                    


            if len(enemies_to_remove)>0:
                for enemy in enemies_to_remove:
                    enemy.destroyed=True
                    self.enemy_list.remove(enemy)
                    

            for bullet in bullets_to_remove:
                p1.bullets.remove(bullet)

            for missile in missiles_to_remove:
                p1.missiles.remove(missile)


            bombs_to_remove=[]

            

            loop_once=0
            for enemy in self.enemy_list:

                enemy.move_enemy()
                enemy.update_enemy()
                enemy.bomb(p1)
                if loop_once==0:
                    
                    enemy.move_bombs()
                    enemy.draw_bombs()
                    loop_once+=1
                
                        



            p1.update_bullets()
            #print(self.enemy_list)
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
