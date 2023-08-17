import pygame
import random
from math import atan2, degrees, pi
import math

debug=False

width,height=(1100,660)


class Missile:

    def __init__(self,x,y,target,owner):
        self.x=x
        self.y=y
        self.target=target
        self.owner=owner
        self.image=pygame.image.load('src/img/weapons/missile3.png')
        self.rect=self.image.get_rect()
        self.angle=0


    max_velocity = 4
    mx_x=2
    velocity_on_angle=max_velocity/90



    def hit_target(self):
        if not (self.target.destroyed):
            rect=self.get_rect()
            if rect.colliderect(self.target.get_rect()):
                drop=Item(self.target.get_centerx(),self.target.y,'gift')
                self.owner.drops.append(drop)
                self.target.destroyed=True
                return True
                
            else:
                return False

    def get_rect(self):

        rect=self.rect
        rect.topleft=(self.x,self.y)
        return  rect
    def get_angle(self):
        angle = self.target.get_angle_between_rects(self.get_rect(),self.target.get_rect())
        return angle
    
    def get_colid_point_angle(self):
        v1_x=(self.colid_point_x())
        v1_y=(self.colid_point_y())
        v2_x=(self.x)
        v2_y=(self.y)

        dx = v1_x - v2_x 
        dy = v1_y- v2_y 
        rads = atan2(-dy,dx)
        rads %= 2*pi
        degs = degrees(rads)

        return degs


    def colid_point_x(self):
        enemy_dir=self.target.move_dir
        eny=self.colid_point_y()-self.target.get_width()//2
        y_dis=self.y-eny
        y_dis=abs(y_dis)
        
        reach_target_time=y_dis//self.max_velocity
        reach_target_time=abs(reach_target_time)

        if enemy_dir=="left":
            cx=((self.target.get_centerx())-reach_target_time)
           
        elif enemy_dir=="right":
            cx=((self.target.get_centerx())+reach_target_time)
        
        self.target.tracked=True

        return cx
    
    def colid_point_y(self):
        if  not self.target.destroyed:
            return self.target.y
        else:
            return self.target.y-500

    def turn_vel(self):
        angle=self.get_colid_point_angle()
        angle=round(angle)
        if angle>90:
            fixed_angle=angle-90
            velx=fixed_angle*self.velocity_on_angle
            vely=self.max_velocity-velx
            velx=-velx

        elif angle<=90:
            vely=angle*self.velocity_on_angle
            velx=self.max_velocity-vely

        return velx,vely


        

    def move_misile(self):
  
        self.get_colid_point_angle()
        x_turn=self.turn_vel()[0]
        y_turn=self.turn_vel()[1]
        
        self.x+=x_turn
        self.y-=y_turn


        

    def draw_missile(self,screen):
        
    
        rect = self.rect.topleft=(self.x,self.y)
       
        if self.target.move_dir=="left":
            angle = self.get_colid_point_angle()
        else:
            angle = self.get_colid_point_angle()


        rotated_image = pygame.transform.rotate(self.image, angle)


        screen.blit(rotated_image,rect)
        if debug:
            pygame.draw.rect(screen, ('red'), (self.colid_point_x(), self.target.y, 15, 15)) # THis is colid point

class Item:
    
    
    def __init__(self,x,y,tag):
        self.x=x
        self.y=y
        self.tag=tag
        self.drop_image=self.drop_image()
        self.drop_rect=self.drop_image.get_rect()
        

    width=20
    height=20
    vely=1


  
    
    def drop_image(self):
        value_list=['repair','repair','ammo','ammo','ammo','missiles']
        value=random.choice(value_list)
        if value=="repair":
            image=pygame.image.load('src/img/drops/drop-repair.png').convert_alpha()
            self.value=value
        elif value=="ammo":
            image=pygame.image.load('src/img/drops/drop-ammo.png').convert_alpha()
            self.value=value
        elif value=="missiles":
            image=pygame.image.load('src/img/drops/drop-missile.png').convert_alpha()
            self.value=value
        
        return image

    def activate(self,player):
        if self.value=='repair':
            if player.health+50>100:
                player.health=100
            else:
                player.health+=50
        elif self.value=='ammo':
            player.ammo+=180
        elif self.value=='missiles':
            player.missiles_storage+=4

    def expired(self):
        
        return self.y >=height-70



    def move_item(self):
        self.drop_rect.topleft=(self.x,self.y)
        self.y+=self.vely
    def get_rect(self):
        rect=pygame.Rect(self.x,self.y,self.width,self.height)
        return  rect

    def draw(self,screen):
        screen.blit(self.drop_image,self.drop_rect)


class Bullet:
    speed = 10
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.moved_x=0
        self.moved_y=0
        self.hitted=False
        self.angel=0

    image=pygame.image.load("src/img/weapons/bullet.png")
    rect=image.get_rect()
    
       
    def get_width(self):
        return self.image.get_width()
    def get_height(self):
        return self.image.get_height()
        

    def move_bullet(self):
        self.x += self.vel_x
        self.y += self.vel_y

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
        rotated_rect.topleft = (self.x, self.y)

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


        if abs(self.moved_y)>800:
            return True

        else:
            return False

    def rotate_bullet(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))
       
 
    
class Player:

    def __init__(self,x,y,name) :
        self.x=x
        self.y=y
        self.bullets=[]
        self.missiles=[]
        self.name=name
        self.get_enemies=[]
        self.drops=[]
        self.attacked_targets=[]
        self.enemies_in_radar=[]
        self.tracked=[]
        self.selected=0
        self.moving_dir='right'


    magazine_size=240
    reloading=False
    moving=False
    droped_ammo=0

    pods_size=4
    reloading_pods=False
    out_of_missiles=False
    out_of_ammo=False
    health=100
    destroyed=False
    forced=False
    forced_time = 0
    right_sprite=pygame.image.load('src/img/vehicles/spaa-gepard3.png')
    rect=right_sprite.get_rect()
    left_sprite=pygame.transform.flip(right_sprite, True, False)
    barrel1=pygame.image.load('src/img/vehicles/barrel1.png')
    barrel2=pygame.image.load('src/img/vehicles/barrel2.png')
    
    

    last_known_position=(0,0)
    last_known_position_update_delay=800
    last_known_position_updated=False
    last_known_position_update_time = 0
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
    radar_range=900
    radar_max_left=0
    radar_min_height=250
    

    def clear(self):
        self.attacked_targets.clear()
        self.enemies_in_radar.clear()
        self.tracked.clear()
        self.drops.clear()
        self.selected=0

    def loadout(self,player_loadout):
        ammo=player_loadout[0]
        magazine=player_loadout[1]
        missiles_storage=player_loadout[2]
        ready_to_fire_missiles=player_loadout[3]
        self.ammo=ammo                                              #1680
        self.magazine=magazine                                      #240
        self.missiles_storage=missiles_storage                      #12
        self.ready_to_fire_missiles=ready_to_fire_missiles          #4
    
    def get_rect(self):
        self.rect.topleft=(self.x,self.y)
        return  self.rect
    
    def get_width(self):
        return self.left_sprite.get_width()
    def get_height(self):
        return self.left_sprite.get_height()

    def get_centerx(self):
        center_x=self.x+(self.get_width()//2)
        return center_x
    
    def get_centery(self):
        center_y=self.y+(self.get_height()//2)
        return center_y

    

    def move_player(self):
        self.update_last_known_position()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            vel_x = -self.move_speed
            self.moving_dir='left'
            
            self.moving=True
        elif keys[pygame.K_d]:
            self.moving_dir='right'
            vel_x = self.move_speed
            self.moving=True
        else:
            vel_x = 0
            self.moving=False
        
        self.x += vel_x
        self.x = max(0, min(self.x, width - self.get_width()))
        
    def update_player(self,screen):
        self.rect.topleft = (self.x, self.y)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))
       
        barrel2 = pygame.transform.rotate(self.barrel2, -angle)
        barrel1 = pygame.transform.rotate(self.barrel1, -angle)
        rotated_rect = barrel2.get_rect()
        rotated_rect.center = (self.x+57, self.y+30)

        screen.blit(barrel1, rotated_rect)
        if self.moving_dir=='left':
            screen.blit(self.left_sprite, self.rect)
        else:
            screen.blit(self.right_sprite, self.rect)            
        screen.blit(barrel2, rotated_rect)
        



        self.radar()
        pygame.draw.rect(screen, ('#66CD00'), (self.radar_max_left, 10, self.radar_range , 4))
        pygame.draw.rect(screen, ('#66CD00'), (5, 10, 4, self.radar_min_height))
        
        if debug:
            pygame.draw.rect(screen,('black'),self.get_rect())

            
    def update_last_known_position(self):
        current_time = pygame.time.get_ticks()
        
        if not self.last_known_position_updated:

            self.last_known_position = (self.x, self.y)
            self.last_known_position_update_time = current_time
            self.last_known_position_updated = True
        else:
            if current_time >= self.last_known_position_update_time + self.last_known_position_update_delay:

                self.last_known_position = (self.get_centerx(), self.get_centery())
                self.last_known_position_update_time = current_time
            
            
    def get_last_known_position(self):
        return self.last_known_position
    

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


    def shoot(self):
        if self.can_shoot():
            self.magazine-=2
            target_x, target_y = pygame.mouse.get_pos()
            bullet = Bullet(self.x+70  - 6 // 2, self.y+34)

            bullet.shoot_at(target_x, target_y)
            bullet.rotate_bullet()
            self.bullets.append(bullet)

            # bullet2 = Bullet(self.x+70  // 2, self.y+32)
            # bullet2.shoot_at(target_x, target_y)
            # bullet2.rotate_bullet()
            # self.bullets.append(bullet2)

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
        max_left=self.x-self.radar_range//2
        max_right=self.x+self.radar_range//2
        self.radar_max_left=max_left

        radar_angle=list(range(max_left,max_right))
        radar_rect=pygame.Rect(max_left,10,self.radar_range,self.radar_min_height)
        
        
        enemies=self.get_enemies

        for enemy in enemies:
            if enemy.get_rect().colliderect(radar_rect) :
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
  
    def bombed(self,dmage):
        self.health-=dmage
 

class Bomb:
    def __init__(self,x,y,velx,vely,guided,angle):
        self.x=x
        self.y=y
        self.width=4
        self.height=6
        self.velx=velx
        self.vely=vely
        self.guided=guided
        self.target=False
        self.dmage=50
        self.exploded=False
        self.angle=angle
        self.image=pygame.image.load('src/img/weapons/bomb.png')
        self.rect=self.image.get_rect()
        self.agm=pygame.image.load('src/img/weapons/agm2.png')
        self.agm_rect=self.agm.get_rect()
        self.max_velocity=2
        self.velocity_on_angle=self.max_velocity/90
        self.moved_x=0


        

    def get_rect(self):
        return  self.rect
    
    def draw(self,screen):
       
        if not self.guided:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect()
            self.rect.topleft=(self.x,self.y)
            rotated_rect.topleft = (self.x, self.y)
            screen.blit(rotated_image,rotated_rect)

        else:
            xy=self.target.get_last_known_position()
            
            angle=self.get_angle()
            angle=round(angle)
         #   print(angle)
            rotated_image = pygame.transform.rotate(self.agm, angle)
            rotated_rect = rotated_image.get_rect()
            self.rect.topleft=(self.x,self.y)
            rotated_rect.topleft = (self.x, self.y)
            screen.blit(rotated_image,rotated_rect)


        if debug:
            pygame.draw.rect(screen,('black'),self.get_rect())
            pygame.draw.rect(screen,('red'),(xy[0],xy[1],10,10))

        
    def get_angle(self):
        xy=self.target.x,self.target.y
        v1_x=xy[0]
        v1_y=xy[1]+15
        v2_x=(self.x)
        v2_y=(self.y)

        dx = v1_x - v2_x 
        dy = v1_y- v2_y 
        rads = atan2(-dy,dx)
        rads %= 2*pi
        degs = degrees(rads)
        self.angle=degs

        return degs
        
    

    def move(self):
        if self.guided:
            self.dmage=75
            self.guide_move()

        else:
            self.dum_move()


    




    def guide_move(self):
        xy=self.target.get_last_known_position()
        x_distance = xy[0] - self.x
        y_distance = xy[1] - self.y
        distance = pygame.math.Vector2(x_distance, y_distance)
        distance.normalize_ip()
        movement = distance * 1

        self.x += movement.x
        self.y += movement.y
        self.moved_x+=abs(movement.x)
        if self.moved_x>=700:
            self.y+=0.1
       


   
      
   

            



           

    def dum_move(self):
        self.y+=self.vely
        self.x+=self.velx



    def is_hit_object(self,objects):
        for obj in objects:
            if self.get_rect().colliderect(obj.get_rect()):
                self.exploded=True
                obj.bombed(self.dmage)
      
        
 
        

        
    def status(self,screen):

        if self.y >= 580:
            self.exploded=True

        if self.exploded:
            self.effect(screen)

    def effect(self,screen):
        
        pygame.draw.rect(screen, pygame.Color('orange'), (self.x, self.y, self.width+5, self.height+5))




class Ally:
    def __init__(self, x, y, frame_width, frame_height):
        self.spritesheet = pygame.image.load("src/img/HMV3.png")
        self.sprite_width=self.spritesheet.get_width()
        self.sprite_height= self.spritesheet.get_height()
        self.x=x
        self.y=y
        self.height=frame_height
        self.width=frame_width
        self.frames = []  
        self.current_frame = 0
        self.health=100
        self.destroyed=False

        
        self.load_frames(self.sprite_width, self.sprite_height, frame_width, frame_height)
    
    def load_frames(self, width, height, frame_width, frame_height):
        for y_offset in range(0, height, frame_height):
            for x_offset in range(0, width, frame_width):
                frame_rect = pygame.Rect(x_offset, y_offset, frame_width, frame_height)
                frame = self.spritesheet.subsurface(frame_rect)
                self.frames.append(frame)

    def move(self):
        if self.health<=0:
            self.destroyed=True

        self.x+=1
        
    def status(self,bombs):
        pass

    def get_rect(self):
        rect=pygame.Rect(self.x,self.y,self.width,self.height)
        return rect
    
    def draw(self,screen):

        screen.blit(self.frames[self.current_frame], (self.x, self.y))
        
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0  
        if debug:
            pygame.draw.rect(screen,'blue',self.get_rect())
    def bombed(self,dmage):
        self.health-=dmage

         



class Base:
    def __init__(self,x,y,hp):
        self.x=x
        self.y=y
        self.image=pygame.image.load('src\\img\\maps\\base.png')
        self.rect=self.image.get_rect()
        self.rect.center=(self.x,self.y)
        self.base_health=hp
        self.actual_health=self.base_health
        self.health_percentage = (self.actual_health / self.base_health) * 100
        self.destroyed=False


    def draw(self,screen):
        screen.blit(self.image,self.rect)
        hb_bar=pygame.Rect(self.x,self.y-50,self.health_percentage,10)
        if self.health_percentage<70:
            color='green'
        elif self.health_percentage<50:
            color='yellow'
        else:
            color='red'
        pygame.draw.rect(screen,color,hb_bar)
        self.health_percentage = (self.actual_health / self.base_health) * 100
        print(self.health_percentage)

    def get_rect(self):
        return self.rect

    def bombed(self,dmage):
        self.actual_health-=dmage
        if self.actual_health<=0:
            self.destroyed=True




class Enemy:
    def __init__(self,x,y,vel,move_dir,bomb_count,guided_bomb,shooting_range,tag,health,target,sprite):
        self.x=x
        self.y=y
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
        self.shooting_range=shooting_range
        self.tag=tag
        self.guided_bomb=guided_bomb
        self.kamikaze=False
        self.target=target
        self.charg=self.bomb_count
        self.right_sprite= sprite
        self.left_sprite=pygame.transform.flip(self.right_sprite, True, False)
        self.bombs=[]
        self.left_sprite_rect=self.left_sprite.get_rect()
        self.right_sprite_rect=self.right_sprite.get_rect()
        self.up=False
        self.down=False

    lock_sprite=pygame.image.load('src/img/weapons/lock.png')
    lock_sprite_rect=lock_sprite.get_rect()
    track_sprite=pygame.image.load('src/img/weapons/track.png')
    track_sprite_rect=track_sprite.get_rect()
    lock_sprite_width=lock_sprite.get_width()


        
    

    def get_center_y(self):
        return self.left_sprite.get_height()//2

    def get_centerx(self):
        center_x=self.x+(self.get_width()//2)
        return center_x
    def get_width(self):
        return self.left_sprite.get_width()
    def get_height(self):
        return self.left_sprite.get_height()   
    


    def clear_bombs(self):
        self.bombs.clear()

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
                                    bomb=Bomb(self.get_centerx(),self.y,x_vel,y_vel,False,135)
                                else:
                                    bomb=Bomb(self.get_centerx(),self.y,-x_vel,y_vel,False,45)
                                self.bombs.append(bomb)
                                self.last_bomb_time = pygame.time.get_ticks()
                                self.bomb_count-=1


                        else:
                            if self.guided_bomb>0:
                                if self.move_dir=='right':
                                    bomb=Bomb(self.get_centerx(),self.y,x_vel,y_vel,True,0)
                                else:
                                    bomb=Bomb(self.get_centerx(),self.y,-x_vel,y_vel,True,0)

                                self.bombs.append(bomb)
                                self.last_bomb_time = pygame.time.get_ticks()
                                self.guided_bomb-=1
        


    def set_x(self,x):
        self.x=x

    def effect(self,screen):
        
        pygame.draw.rect(screen, pygame.Color('orange'), (self.x, self.y, self.get_width()+5, self.get_height()+5))


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
       # pass
        self.bomb_count=self.charg


            

    def move_enemy(self,screen):
        if not self.destroyed:
            if not self.kamikaze:
                self.side_move()
            else:
                self.kamikaze_move(self.target,screen)
 
    



    def get_rect(self):
        return  self.left_sprite_rect
    
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
        

        if debug:
            pygame.draw.rect(screen,('black'),self.get_rect())

        self.left_sprite_rect.topleft=(self.x,self.y)
        self.right_sprite_rect.topleft=(self.x,self.y)

        if self.move_dir=="left":
            screen.blit(self.left_sprite,self.left_sprite_rect)
        else:
            screen.blit(self.right_sprite,self.right_sprite_rect)

        if self.locked:
            rect_center=self.track_sprite_rect.topleft=(self.get_centerx()-15,self.y-3)
            screen.blit(self.track_sprite,rect_center)


        elif self.tracked:
            rect_center=self.lock_sprite_rect.topleft=(self.get_centerx()-15,self.y-3)
            screen.blit(self.lock_sprite,rect_center)

    
    
    def is_taken_damage(self):
        if self.damaged==True:
            return True
        else:
            return False

    def check_kill(self, obje):
        for bullet in obje:
            if (self.x < bullet.x + bullet.get_width() and
                self.x + self.get_width() > bullet.x and
                self.y < bullet.y + bullet.get_height() and
                self.y + self.get_height() > bullet.y):
                bullet.hitted=True
                self.health-=15
                if self.health<0:
                    self.destroyed=True
                    return True       

        return False