import pygame
import random
from math import atan2, degrees, pi
import math

width,height=(1100,660)


pygame.init()

class Missile:
    width=5
    height=17
    vel_x=2
    vel_y=-4

    def __init__(self,x,y,target,owner):
        self.x=x
        self.y=y
        self.target=target
        self.owner=owner


    def hit_target(self):
        if not (self.target.destroyed):
            rect=pygame.Rect(self.x,self.y,self.width,self.height)
            if rect.colliderect(self.target.get_rect()):
                drop=Item(self.target.get_centerx(),self.target.y,'gift')
                self.owner.drops.append(drop)
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
            cx=((self.target.get_centerx())-reach_target_time)
           
        elif enemy_dir=="right":
            cx=((self.target.get_centerx())+reach_target_time)
        
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

        if missiile_x_turn_vel>=4:
            if self.vel_y<-2:
                self.vel_y+=1
 

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

    def draw_missile(self,screen):
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
                player.health=100
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

    def draw(self,screen):
        
        pygame.draw.rect(screen, pygame.Color('gold'), (self.x, self.y, self.width, self.height))


class Bullet:
    speed = 10
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.max_y=0
        self.max_x=0
        self.moved_x=0
        self.moved_y=0
        self.hitted=False
        self.image=pygame.image.load("src/img/bullet.png")
        self.rect=self.image.get_rect()
        self.angel=0
       
    def get_width(self):
        return self.image.get_width()
    def get_height(self):
        return self.image.get_height()
        

    def move_bullet(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.max_y+=self.vel_y
        self.max_x+=self.vel_x

        self.moved_x+=abs(self.vel_x)
        self.moved_y+=abs(self.vel_y)



    def draw_effect(self,screen):

        rotated_effect = pygame.transform.rotate(self.effect, -self.angle)
        rotated_rect = rotated_effect.get_rect()
        rotated_rect.center = (self.x, self.y)

        screen.blit(rotated_effect, rotated_rect)



    def draw_bullet(self,screen):
      
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = (self.x, self.y)

        self.moved_y=abs(self.moved_y)
        self.moved_x=abs(self.moved_x)
        xy=self.moved_y+self.moved_x


        if xy>100 :
            screen.blit(rotated_image, rotated_rect)

        

    def shoot_at(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed

    def out_of_range(self):

        x_y=abs(self.max_x)+abs(self.max_y)


        if x_y>650:
            return True

        if abs(self.max_y)>370:
            return True
        if abs(self.max_x)>550:
        
            return True
        else:
            return False

    def rotate_bullet(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))
       
        

        

       
    
class Player:

    def __init__(self,x,y,bullets,missiles,name,get_enemies) :
        self.x=x
        self.y=y
        self.bullets=bullets
        self.missiles=missiles
        self.name=name
        self.get_enemies=get_enemies

    attacked_targets=[]
    enemies_in_radar=[]
    tracked=[]
    drops=[]
    selected=0
    ammo=1680
    magazine=240
    magazine_size=240
    reloading=False
    moving=False
    droped_ammo=0
    missiles_storage=12
    ready_to_fire_missiles=4
    pods_size=4
    reloading_pods=False
    out_of_missiles=False
    out_of_ammo=False
    health=100
    destroyed=False
    forced=False
    forced_time = 0
    image=pygame.image.load('src/img/spaa-gepard.png')
    rect=image.get_rect()
    barrel=pygame.image.load('src/img/barrel.png')
    barrel_rect=image.get_rect()
    
    

    width=100
    height=40
    player_alive=True
    move_speed = 2
    shoot_delay = 100  
    last_shot_time = 0
    fire_missie_delay=300
    last_fire_time=0
    caluculate_rewards_deleay=2000
    reload_delay=3000
    pods_reload_delay=4000
    reload_start_time=0
    pods_reload_start_time=0
    radar_range=0
    radar_max_left=0
    radar_min_height=300
    
    def get_rect(self):
        self.rect.topleft=(self.x,self.y)
        return  self.rect
    
    def get_width(self):
        return self.image.get_width()
    def get_height(self):
        return self.image.get_height()

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
        
    def update_player(self,screen):
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, self.rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))
       
        rotated_image = pygame.transform.rotate(self.barrel, -angle)
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = (self.x+57, self.y+30)


        
        screen.blit(rotated_image, rotated_rect)
        self.radar()
        pygame.draw.rect(screen, ('darkgreen'), (self.radar_max_left, 10, self.radar_range , 2))
        pygame.draw.rect(screen, ('darkgreen'), (5, 10, 2, self.radar_min_height))
        
        #pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.get_width(), self.get_height()))
        #pygame.draw.rect(screen,('black'),self.get_rect())

            

    

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
                if self.ammo<self.magazine_size:
                    self.magazine=self.ammo
                    self.ammo=0
                else:
                    self.magazine=self.magazine_size
                    self.ammo-=self.magazine_size

   


    def reload_pods(self):
        current_time = pygame.time.get_ticks()
        if self.pods_reload_start_time+self.pods_reload_delay<=current_time:
            if self.missiles_storage>=self.pods_size:
                self.ready_to_fire_missiles=self.pods_size
                self.missiles_storage-=self.pods_size
     



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


    def shoot(self,screen):
        if self.can_shoot():
            self.magazine-=2
            target_x, target_y = pygame.mouse.get_pos()
            bullet = Bullet(self.x+62  - 6 // 2, self.y+34)

            bullet.shoot_at(target_x, target_y)
            bullet.rotate_bullet()
  

            self.bullets.append(bullet)

            self.last_shot_time = pygame.time.get_ticks()
            self.reload_start_time=self.last_shot_time
            
            

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move_bullet()

    def move_missiles(self):
        for mis in self.missiles:
            mis.move_misile()

    def update_bullets(self,screen):
        for bullet in self.bullets:
            bullet.draw_bullet(screen)

    def update_missiles(self,screen):
        for mis in self.missiles:
            mis.draw_missile(screen)

    def radar(self):
        radar_range=900
        max_left=self.x-radar_range//2
        max_right=self.x+radar_range//2
        radar_angle=list(range(max_left,max_right))
        self.radar_range=radar_range
        self.radar_max_left=max_left
        self.enemies_in_radar=[]
        enemies=self.get_enemies

        for enemy in enemies:
            if enemy.get_centerx() in radar_angle and enemy.y < self.radar_min_height:
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
    
 
    def fire_missile(self,owner):
        if self.can_fire_missile():
            if self.auto_lock():
                locked=self.auto_lock()
                missile_start_x=self.x
                missile_start_y=self.y
                self.ready_to_fire_missiles-=1
                missile=Missile(missile_start_x, missile_start_y,locked,owner)
                self.missiles.append(missile)
                self.last_fire_time = pygame.time.get_ticks()
                locked.locked=True
                self.attacked_targets.append(locked)
                self.pods_reload_start_time=self.last_fire_time



    def move_drops(self,screen,owner):
        for drop in self.drops:
            drop.move_item()
            drop.draw(screen)
            if self.get_rect().colliderect(drop.get_rect()):
                drop.activate(owner)
                self.drops.remove(drop)
            if drop.expired():
                if drop in self.drops:
                    self.drops.remove(drop)

 

class Bomb:
    def __init__(self,x,y,velx,vely,guided,target,angle):
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
        self.angle=angle
        self.image=pygame.image.load('src/img/bomb5.png')
        self.rect=self.image.get_rect()

    def get_rect(self):

        return  self.rect
    
    def draw(self,screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect()
        self.rect.topleft=(self.x,self.y)
        rotated_rect.topleft = (self.x, self.y)
        screen.blit(rotated_image,rotated_rect)

        pygame.draw.rect(screen,('black'),self.get_rect())
        pygame.draw.rect(screen,('black'),self.target.get_rect())
        

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
        

        
    def status(self,screen):
        
        if self.hit_player():
            self.explode_and_dmage()
            self.effect(screen)
            self.exploded=True
            
        elif self.y > height-30:
            self.effect(screen)
            self.exploded=True

    def effect(self,screen):
        
        pygame.draw.rect(screen, pygame.Color('orange'), (self.x, self.y, self.width+5, self.height+5))




class Enemy:
    def __init__(self,x,y,width,height,vel,move_dir,bomb_count,guided_bomb,color,shooting_range,tag,health,target,sprites):
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
        self.target=target
        self.charg=self.bomb_count
        self.left_sprite=sprites[0]
        self.right_sprite=sprites[1]
        self.left_sprite_rect=self.left_sprite.get_rect()
        self.right_sprite_rect=self.right_sprite.get_rect()


        
    bombs=[]



    def get_centerx(self):
        center_x=self.x+(self.width//2)
        return center_x
    
    def move_bombs(self):
        for bomb in self.bombs:
            bomb.move()
            if bomb.exploded==True:
                self.bombs.remove(bomb)

    def clear_bombs(self):
        self.bombs.clear()

    def draw_bombs(self,screen):
        for bomb in self.bombs:
            bomb.draw(screen)
            bomb.status(screen)
          
    


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
            
     

            if reach_x in target_attak_range:
                    if self.tag=='kamikaze':
                        self.kamikaze=True
                    if self.can_bomb():
                        if not guided:
                            if self.bomb_count>0:
                                if self.move_dir=='right':
                                    bomb=Bomb(self.get_centerx(),self.y,x_vel,y_vel,False,target,135)
                                else:
                                    bomb=Bomb(self.get_centerx(),self.y,-x_vel,y_vel,False,target,45)
                                self.bombs.append(bomb)
                                self.last_bomb_time = pygame.time.get_ticks()
                                self.bomb_count-=1


                        else:
                            if self.guided_bomb>0:
                                if self.move_dir=='right':
                                    bomb=Bomb(self.get_centerx(),self.y,x_vel,y_vel,True,target,0)
                                else:
                                    bomb=Bomb(self.get_centerx(),self.y,-x_vel,y_vel,True,target,0)

                                self.bombs.append(bomb)
                                self.last_bomb_time = pygame.time.get_ticks()
                                self.guided_bomb-=1
        


    def set_x(self,x):
        self.x=x

    def effect(self,screen):
        
        pygame.draw.rect(screen, pygame.Color('orange'), (self.x, self.y, self.width+5, self.height+5))


    def kamikaze_move(self,target,screen):
        target_x=target.x
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

        self.check_hit_player(target,screen)
            

        


    def check_hit_player(self,target,screen):
        if self.get_rect().colliderect(target.get_rect()):
            self.destroyed=True
            self.effect(screen)
            if target.health -80  <0:
                target.health=0
            else:
                target.health-=80

      

        

    def side_move(self):
        if self.move_dir=='right':
            self.x+=self.vel
         
        elif self.move_dir=="left":
            self.x-=self.vel
    
    def recharge(self):
        self.bomb_count=self.charg
            

    def move_enemy(self,screen):
        if not self.destroyed:
            if not self.kamikaze:
                self.side_move()
            else:
                self.kamikaze_move(self.target,screen)
 
    



    def get_rect(self):
        return  self.right_sprite_rect
    
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


    def update_enemy(self,screen):
        
        target_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, target_rect)
        #text = pygame.font.SysFont(None, 24).render("", True, (0, 0, 0))

        #if self.locked:
           # pygame.draw.rect(screen, self.color, target_rect)
            #text = pygame.font.SysFont(None, 24).render("x", True, ('red'))

       # elif self.tracked:
           # pygame.draw.rect(screen, self.color, target_rect)
           # text = pygame.font.SysFont(None, 24).render("O", True, ('green'))
        #text_rect = text.get_rect(center=target_rect.center)
        #screen.blit(text, text_rect)

        self.left_sprite_rect.topleft=(self.x,self.y)
        self.right_sprite_rect.topleft=(self.x,self.y)

        if self.move_dir=="left":
            screen.blit(self.left_sprite,self.left_sprite_rect)
        else:
            screen.blit(self.right_sprite,self.right_sprite_rect)

    


    
    def is_taken_damage(self):
        if self.damaged==True:
            return True
        else:
            return False

    def check_kill(self, obje):
        for bullet in obje:
            if (self.x < bullet.x + bullet.get_width() and
                self.x + self.width > bullet.x and
                self.y < bullet.y + bullet.get_height() and
                self.y + self.height > bullet.y):
                bullet.hitted=True
                self.health-=15
                if self.health<0:
                    self.destroyed=True
                    return True       

        return False