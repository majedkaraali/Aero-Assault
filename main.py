import pygame
import random
from math import atan2, degrees, pi
import math

from objects import Missile

pygame.init()



width=1100
height=660


screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
score=0
enemy_types=['fighter','strike_aircraft','bomber','kamikaze_drone']



pygame.mixer.init()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)


class Item:
    def __init__(self,x,y,tag):
        self.x=x
        self.y=y
        self.tag=tag

    width=20
    height=20
    vely=1


    def drop_value(self):
        value_list=['health','ammo','missiles']
        value=random.choice(value_list)
        return value


    def activate(self,player):
        if self.drop_value()=='health':
            if player.health+50>100:
                player.healh=100
            else:
                player.health+=50
        elif self.drop_value()=='ammo':
            player.ammo+=180
        elif self.drop_value()=='missiles':
            player.missiles_storage+=4

    def expired(self):
        return self.y >=height-70



    def move_item(self):
        self.y+=self.vely

    def get_rect(self):
        rect=pygame.Rect(self.x,self.y,self.width,self.height)
        return  rect

    def draw(self):
        pygame.draw.rect(screen, pygame.Color('gold'), (self.x, self.y, self.width, self.height))


             


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
        self.drops=[]
        self.selected=0
        self.ammo=1200
        self.magazine=180
        self.reloading=False
        self.moving=False
        self.droped_ammo=0
        self.missiles_storage=12
        self.ready_to_fire_missiles=4
        self.reloading_pods=False
        self.out_of_missiles=False
        self.out_of_ammo=False
        self.health=100
        self.destroyed=False
        self.forced=False
        self.forced_time = 0


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
    caluculate_rewards_deleay=2000
    reload_delay=3000
    pods_reload_delay=7000
    reload_start_time=0
    pods_reload_start_time=0
    
    
    def get_rect(self):
        rect=pygame.Rect(self.x,self.y,self.width,self.height)
        return  rect

    def get_centerx(self):
        center_x=self.x+(self.width//2)
        return center_x

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            vel_x = -self.move_speed
            self.moving=True
        elif keys[pygame.K_d]:
            vel_x = self.move_speed
            self.moving=True
        else:
            vel_x = 0
            self.moving=False
        
        self.x += vel_x
        self.x = max(0, min(self.x, width - self.width))
        
    def update_player(self):
        global pl
        pl = pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.radar()

            

    

    def is_destroyed(self):
        if self.health <= 0:
            if not self.forced:
                self.forced = True
                self.forced_time = pygame.time.get_ticks()  
            else:
                current_time = pygame.time.get_ticks()
                if current_time >= self.forced_time + 2000: 
                    self.destroyed = True

           

    def reload(self):
        current_time = pygame.time.get_ticks()
        if self.reload_start_time+self.reload_delay<=current_time:
            if self.droped_ammo>0:
                self.ammo+=self.droped_ammo
                self.droped_ammo=0
            
            if self.ammo>0:
                if self.ammo<180:
                    self.magazine=self.ammo
                    self.ammo=0
                else:
                    self.magazine=180
                    self.ammo-=180

   


    def reload_pods(self):
        current_time = pygame.time.get_ticks()
        if self.pods_reload_start_time+self.pods_reload_delay<=current_time:
            if self.missiles_storage>=4:
                self.ready_to_fire_missiles=4
                self.missiles_storage-=4
     



    def chek_missile_lounchers_pods(self):
        if  self.missiles_storage>0:
            if self.ready_to_fire_missiles<=0:
                self.reload_pods()
                self.reloading_pods=True
            else:
                self.reloading_pods=False

        elif self.missiles_storage<=0:
            if self.ready_to_fire_missiles<=0:
                self.reloading_pods=True
            else:
                self.reloading_pods=False
            self.out_of_missiles=True

    def chek_magazine(self):
        if  self.ammo>0:
            if self.magazine<=0:
                self.reload()
                self.reloading=True
            else:
                self.reloading=False

        elif self.ammo<=0:
            if self.magazine<=0:
                self.reloading=True
            else:
                self.reloading=False
            self.out_of_ammo=True


   

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        
        if not self.reloading:
            if current_time - self.last_shot_time >= self.shoot_delay:
                return True
        else:
            return False
        

    
    def can_fire_missile(self):
        current_time = pygame.time.get_ticks()
        if not self.reloading_pods:
            if current_time - self.last_fire_time >= self.fire_missie_delay:
                return True
        else:
            return False


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
                self.ready_to_fire_missiles-=1
                missile=Missile(missile_start_x, missile_start_y,locked,p1)
                self.missiles.append(missile)
                self.last_fire_time = pygame.time.get_ticks()
                locked.locked=True
                self.attacked_targets.append(locked)
                self.pods_reload_start_time=self.last_fire_time



    def move_drops(self):
        for drop in self.drops:
            drop.move_item()
            drop.draw()
            if self.get_rect().colliderect(drop.get_rect()):
                drop.activate(p1)
                self.drops.remove(drop)
            if drop.expired():
                if drop in self.drops:
                    self.drops.remove(drop)


        



class Bomb:
    def __init__(self,x,y,velx,vely,guided,target):
        self.x=x
        self.y=y
        self.width=4
        self.height=6
        self.velx=velx
        self.vely=vely
        self.guided=guided
        self.target=target
        self.dmage=50
        self.exploded=False
    def get_rect(self):
        rect=pygame.Rect(self.x,self.y,self.width,self.height)
        return  rect

    def move(self):
        if self.guided:
            self.dmage=75
            self.width=6
            self.height=10
            self.guide_move()
        else:
            self.dum_move()

    def guide_move(self):
        target_x=self.target.get_centerx()
        target_y=self.target.y
        x_dis=self.x-target_x
        x_dis=abs(x_dis)
        self.vely=0.5
        y_dis=abs(self.y-target_y)
        reach_time=y_dis//self.vely

        if reach_time >0:
            velx=x_dis/reach_time
        else:
            velx=2

        if velx>1:
            velx=1
            if self.vely>0:
                self.vely-=0.3

        if self.x<target_x:
            self.x+=velx
        else:
            self.x-=velx

        self.y+=self.vely
           

    def dum_move(self):
        self.y+=self.vely
        self.x+=self.velx



    def hit_player(self):
        if self.get_rect().colliderect(self.target.get_rect()):
            return True
        
    def explode_and_dmage(self):
        if not self.exploded:
            if self.target.health-self.dmage<0:
                self.target.health=0
            else:
                self.target.health-=self.dmage
        

        
    def status(self):
        if self.hit_player():
            self.explode_and_dmage()
            self.effect()
            self.exploded=True
        elif self.y > height-70:
            self.effect()
            self.exploded=True

    def effect(self):
        pygame.draw.rect(screen, pygame.Color('orange'), (self.x, self.y, self.width+5, self.height+5))


    def draw(self):
        pygame.draw.rect(screen, pygame.Color('black'), (self.x, self.y, self.width, self.height))


    

class Enemy:
    def __init__(self,x,y,width,height,vel,move_dir,bomb_count,guided_bomb,color,shooting_range,tag,health):
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
        self.bomb_count=bomb_count
        self.health=health
        self.damaged=False
        self.color=color
        self.shooting_range=shooting_range
        self.tag=tag
        self.guided_bomb=guided_bomb
        self.kamikaze=False
        
    bombs=[]



    def get_centerx(self):
        center_x=self.x+(self.width//2)
        return center_x
    
    def move_bombs(self):
        for bomb in self.bombs:
            bomb.move()
            bomb.status()
            if bomb.exploded==True:
                self.bombs.remove(bomb)

    def clear_bombs(self):
        self.bombs.clear()

    def draw_bombs(self):
        for bomb in self.bombs:
            bomb.draw()
          
    


    def can_bomb(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_bomb_time >= self.bomb_dely
    
    def attack(self,target):
        if self.can_bomb():
            distance_x=self.get_centerx()-target.x
            distance_x=abs(distance_x)
            distance_y=abs(self.y)-abs(target.y)
            target_x=target.get_centerx()


            guided=False
            if self.tag=='strike':
                guided=True
            if self.y >300:
                guided=False
             
                self.shooting_range=70
            target_attak_range=list(range(target_x-self.shooting_range,target_x+self.shooting_range))
            y_vel=1
            x_vel=1

            reach_time=distance_y//y_vel
            reach_time=abs(reach_time)
            
            if self.move_dir=="right":
                reach_x=self.x+reach_time//x_vel
            else:
                reach_x=self.x-reach_time//x_vel
            
          


            if  self.get_centerx()>0 and self.get_centerx()<width-10:
                if reach_x in target_attak_range:
                    if self.tag=='kamikaze':
                        self.kamikaze=True
                    if self.can_bomb():
                        if not guided:
                            if self.bomb_count>0:
                                if self.move_dir=='right':
                                    bomb=Bomb(self.get_centerx(),self.y,x_vel,y_vel,False,target)
                                else:
                                    bomb=Bomb(self.get_centerx(),self.y,-x_vel,y_vel,False,target)
                                self.bombs.append(bomb)
                                self.last_bomb_time = pygame.time.get_ticks()
                                self.bomb_count-=1


                        else:
                            if self.guided_bomb>0:
                                if self.move_dir=='right':
                                    bomb=Bomb(self.get_centerx(),self.y,x_vel,y_vel,True,target)
                                else:
                                    bomb=Bomb(self.get_centerx(),self.y,-x_vel,y_vel,True,target)

                                self.bombs.append(bomb)
                                self.last_bomb_time = pygame.time.get_ticks()
                                self.guided_bomb-=1
        


    def set_x(self,x):
        self.x=x

    def effect(self):
        pygame.draw.rect(screen, pygame.Color('orange'), (self.x, self.y, self.width+5, self.height+5))


    def kamikaze_move(self,target):
        target_x=target.get_centerx()
        target_y=target.y
        x_dis=self.x-target_x
        x_dis=abs(x_dis)
        self.vely=1.5
        y_dis=abs(self.y-target_y)
        reach_time=y_dis//self.vely

        if reach_time >0:
            velx=x_dis/reach_time
        else:
            velx=2

        if velx>=2.2:
            velx=2.2

        if self.x<target_x:
            self.x+=velx
        else:
            self.x-=velx
            
        self.y+=self.vely

        self.check_hit_player(target)
            

        


    def check_hit_player(self,target):
        if self.get_rect().colliderect(target.get_rect()):
            self.destroyed=True
            self.effect()
            if 80 - target.health <0:
                target.target.health=0
            else:
                target.health-=80

      

        

    def side_move(self):
        if self.move_dir=='right':
            self.x+=self.vel
        elif self.move_dir=="left":
            self.x+=self.vel

    def move_enemy(self):
        if not self.destroyed:
            if not self.kamikaze:
                self.side_move()
            else:
                self.kamikaze_move(p1)
 
    



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
        pygame.draw.rect(screen, self.color, target_rect)
        text = pygame.font.SysFont(None, 24).render("", True, (0, 0, 0))


        if self.locked:
            pygame.draw.rect(screen, self.color, target_rect)
            text = pygame.font.SysFont(None, 24).render("x", True, ('red'))

        elif self.tracked:
            pygame.draw.rect(screen, self.color, target_rect)
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
    reward_screen=False

    pause_frame_color = ('silver')
    rerawrds_frame_color=('silver')
    pause_surface_width=250
    pause_surface_height=150
    frame_position = ((width//2)-(pause_surface_width//2),(height//2)-(pause_surface_height//2))
    frame_surface = pygame.Surface((pause_surface_width,pause_surface_height))
    frame_surface.fill(pause_frame_color)

    border_width = 1
    border_color = (0, 0, 0)


    
    rwd_surface_width = width//2
    rwd_surface_height = height//2
    reward_scr_position =  ((width//2)-(rwd_surface_width//2),(height//2)-(rwd_surface_height//2))
    rewards_surface = pygame.Surface((rwd_surface_width, rwd_surface_height))
    rewards_surface.fill(rerawrds_frame_color)


    resume_button_rect=pygame.Rect(75, 20, 100, 20)
    main_menu_button_rect=pygame.Rect(75, 60, 100, 20)
    exit_button_rect=pygame.Rect(75, 100, 100, 20)


    
    score_rect=pygame.Rect(35, height-15, 100, 20)
    menu_rect=pygame.Rect((width//2), height-15, 100, 66)
    missile_count_rect=pygame.Rect(width-50, height-15, 50, 66)
    bullet_count_rect=pygame.Rect(width-150, height-15, 50, 66)
    scorevalue_rect=pygame.Rect(80, height-15, 100, 20)

    main_menu_btn_rect=pygame.Rect((rwd_surface_width//2)-150,rwd_surface_height-70,100,20)
    exit_btn_rect=pygame.Rect((rwd_surface_width//2)+100,rwd_surface_height-70,70,20)




    enemy_list=[]
    

    def __init__(self):
        super().__init__()
        self.running=True
        self.force_reload=False
        
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
                        self.paues = False

                    elif self.main_menu_button_rect.collidepoint(adjusted_mouse_pos):
                        current_state = menu_state 
                        self.paues = False
                        self.enemy_list.clear()
                

                    elif self.exit_button_rect.collidepoint(adjusted_mouse_pos):
                        self.running = False

                if self.reward_screen:
                    adjusted_mouse_pos = (
                    mouse_pos[0] - self.reward_scr_position[0],
                    mouse_pos[1] - self.reward_scr_position[1]
                    )
                    
                
                    if self.main_menu_btn_rect.collidepoint(adjusted_mouse_pos):
                        current_state = menu_state 
                        self.paues = False
                        self.reward_screen=False
                        for enemy in self.enemy_list:
                            enemy.clear_bombs()
                        self.enemy_list.clear()


                    elif self.exit_btn_rect.collidepoint(adjusted_mouse_pos):
                        self.running = False
       
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_pressed = False
            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.paues:
                        self.paues = False
                    else:
                        if not self.reward_screen:
                            self.paues = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_TAB] and not tab_pressed:
                    if not p1.forced:
                        p1.next_lock()
                        tab_pressed = True
                        

                if keys[pygame.K_r]:
                    p1.reload_start_time=pygame.time.get_ticks()
                    p1.droped_ammo+=p1.magazine
                    p1.magazine=0
 
            elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        tab_pressed = False

        

        if self.mouse_button_pressed:
                if not p1.forced:
                    p1.shoot()




    def respawn_fighter(self,move_dircton,y):
        if move_dircton==1:
                x_spawns=[-700,-650,-600,-550,-500,-450,-400,-350,-300,-250,-200]
                x=random.choice(x_spawns)-40
                mdir='right'
                vel=2

        else:
            x_spawns=[width+700,width+650,width+600,width+550,width+500,width+450,width+400,width+350,width+300,width+250,width+200]
            x=random.choice(x_spawns)+40
            mdir='left'
            vel=-2
           
        enemy=Enemy(x,y,80,25,vel,mdir,3,0,'blue',50,'fighter',80)
        self.enemy_list.append(enemy)

    
    def respawn_strike(self,move_dircton,y):
        if move_dircton==1:
                x_spawns=[-700,-650,-600,-550,-500,-450,-400,-350,-300,-250,-200]
                x=random.choice(x_spawns)-40
                mdir='right'
                vel=2

        else:
            x_spawns=[width+700,width+650,width+600,width+550,width+500,width+450,width+400,width+350,width+300,width+250,width+200]
            x=random.choice(x_spawns)+40
            mdir='left'
            vel=-2
           
        enemy=Enemy(x,y,80,25,vel,mdir,6,1,'darkgreen',200,'strike',100)
        self.enemy_list.append(enemy)

    def respawn_bomber(self,move_dircton,y):
        if move_dircton==1:
                x_spawns=[-700,-650,-600,-550,-500,-450,-400,-350,-300,-250,-200]
                x=random.choice(x_spawns)-40
                mdir='right'
                vel=2

        else:
            x_spawns=[width+700,width+650,width+600,width+550,width+500,width+450,width+400,width+350,width+300,width+250,width+200]
            x=random.choice(x_spawns)+40
            mdir='left'
            vel=-2
           
        enemy=Enemy(x,y,110,25,vel,mdir,10,0,'brown',120,'bomber',130)
        self.enemy_list.append(enemy)


    def respawn_drone(self,move_dircton,y):
        if move_dircton==1:
                x_spawns=[-700,-650,-600,-550,-500,-450,-400,-350,-300,-250,-200]
                x=random.choice(x_spawns)-40
                mdir='right'
                vel=2

        else:
            x_spawns=[width+700,width+650,width+600,width+550,width+500,width+450,width+400,width+350,width+300,width+250,width+200]
            x=random.choice(x_spawns)+40
            mdir='left'
            vel=-2
           
        enemy=Enemy(x,y,40,20,vel,mdir,0,0,'white',400,'kamikaze',30)
        self.enemy_list.append(enemy)


    
    def generate_enemies(self,num_of_enemies):

        def respawn_enemy():
            respawn_chance = random.random()
            if respawn_chance <= 0.4:  
                return 'strike_aircraft'
            elif respawn_chance <= 0.6:  
                return 'fighter_aircraft'
            elif respawn_chance <= 0.8:  
                return 'bomber'
            elif respawn_chance <= 1.0:  
                return 'kamikaze_drone'
            else:
                return None  

    
        
        if len(self.enemy_list)<num_of_enemies:
            respawned_enemy = respawn_enemy()
            move_dircton=random.randint(0,1)
            y_spawns=[5,33,60,90,120,150,180,210,240,270,300,330,370,400,430,470,500]
            y=random.choice(y_spawns)
            
            if respawned_enemy=='fighter_aircraft':
                self.respawn_fighter(move_dircton,y)
            
            elif respawned_enemy=='strike_aircraft':
                self.respawn_strike(move_dircton,y)
     

            elif respawned_enemy=="bomber":
                self.respawn_bomber(move_dircton,y)
               
            
            elif respawned_enemy=="kamikaze_drone":
                self.respawn_drone(move_dircton,y)

           

            

    def get_enemies(self):
        return self.enemy_list
        


    def reward_screen_view(self):
        pygame.draw.rect(self.rewards_surface,self.border_color, self.rewards_surface.get_rect(), self.border_width)
        screen.blit(self.rewards_surface, self.reward_scr_position)
        self.rewards_surface.fill('silver')


        
        main_menu_text = font.render("Main Menu", True, (255, 255, 255))
        main_menu_text_rect=main_menu_text.get_rect(center=self.main_menu_btn_rect.center)

        
        exit_text = font.render("Exit ", True, (255, 255, 255))
        exit_text_rect=exit_text.get_rect(center=self.exit_btn_rect.center)


        scor_text= font.render("Score: 0", True, (255, 255, 255))
        score_pos=((self.rwd_surface_width//2)-scor_text.get_width()//2,80)

        high_score= font.render("High Score: 0", True, (255, 255, 255))
        high_score_pos=((self.rwd_surface_width//2)-high_score.get_width()//2,120)


        died_text= font.render(" YOU HAVE BEEN DESTROYED ! ", True, (255, 255, 255))
        died_text_pos=((self.rwd_surface_width//2)-(died_text.get_width()//2),20)

       

        self.rewards_surface.blit(main_menu_text,main_menu_text_rect)
        self.rewards_surface.blit(exit_text,exit_text_rect)
        self.rewards_surface.blit(died_text,died_text_pos)
        self.rewards_surface.blit(scor_text,score_pos)
        self.rewards_surface.blit(high_score,high_score_pos)



        
   

    
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
        global score,pause_menurect
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
        pause_menurect=menu_text.get_rect()

        if p1.reloading:
            magazine='---'
        else:
            magazine=str(p1.magazine)

        bullets=str(p1.ammo)

        if p1.reloading_pods:
            missiles='--'
        else:
            missiles=p1.ready_to_fire_missiles

        storage=p1.missiles_storage

        bullets_text = font.render(f"bullets: {magazine}/{bullets}", True, 'black')
        bullets_text_pos=(width-250,height-25)

        missiles_text = font.render(f"missiles: {missiles}/{storage}", True, 'black')
        missiles_text_pos=(width-400,height-25)

        heath_value=p1.health

        heatl_text = font.render(f"health: {str(heath_value)}", True, 'black')
        heatl_text_pos=(width-100,height-25)
      
        screen.blit(score_text,score_text_pos)
        screen.blit(menu_text, menu_text_pos)
        screen.blit(bullets_text, bullets_text_pos)
        screen.blit(missiles_text, missiles_text_pos)
        screen.blit(heatl_text, heatl_text_pos)


           



    def draw(self):
        
        
        if not (self.paues) :
            if not self.reward_screen:
                clock.tick(60)
                screen.fill('aqua')
                self.ground()
                self.statics()
                if not p1.forced:
                    p1.move_player()
                    self.generate_enemies(3)
                p1.update_player()
                p1.move_bullets() 
                p1.update_bullets()
                p1.move_missiles()
                p1.update_missiles()
                p1.chek_magazine()
                p1.chek_missile_lounchers_pods()
                p1.move_drops()
                p1.is_destroyed()    
                
    
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if not p1.forced:
                        p1.shoot()
                elif keys[pygame.K_f]:
                    if not p1.forced:
                        p1.fire_missile()
                    
                enemies_to_remove = []
                bullets_to_remove = []
                missiles_to_remove=[]

                for enemy in self.enemy_list:
                    if enemy.destroyed:
                        enemies_to_remove.append(enemy)
                    if enemy.check_collision(p1.bullets):
                        chanse=random.randint(1,5)
                        if chanse==1:
                            drop=Item(enemy.get_centerx(),enemy.y,'gift')
                            p1.drops.append(drop)
                        enemies_to_remove.append(enemy)
                    if enemy.move_dir=='left':
                        if (enemy.x)<-300:
                            enemy.destroyed=True
                            enemies_to_remove.append(enemy)
                    
                    elif enemy.move_dir=='right':
                        if (enemy.x)>width+300:
                            enemy.destroyed=True
                            enemies_to_remove.append(enemy)

                    if enemy.y>580:
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

                loop_once=0
                for enemy in self.enemy_list:
                    if enemy.destroyed==True:
                        enemies_to_remove.append(enemy)

                    enemy.move_enemy()
                    enemy.update_enemy()
                    enemy.attack(p1)
                    if loop_once==0:
                        
                        enemy.move_bombs()
                        enemy.draw_bombs()
                        loop_once+=1
                            

                p1.update_bullets()

                if p1.destroyed:
                    self.reward_screen=True

            elif (self.reward_screen):
                self.reward_screen_view()
               


    


        
        
        elif (self.paues):

            pygame.draw.rect(self.rewards_surface,self.border_color, self.frame_surface.get_rect(), self.border_width)
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
def main():    
          

    while current_state.running:
        
        events = pygame.event.get()


        for event in events:
            if event.type == pygame.QUIT:
                current_state.running = False

        
        
        next_state = current_state.handle_events(events)
        current_state.update()
        current_state.draw()
        #print(clock.get_fps())

        pygame.display.flip()



        

    pygame.quit()
if __name__=='__main__':
    main()
