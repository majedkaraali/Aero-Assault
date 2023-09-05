import pygame
import random
from math import atan2, degrees, pi
import math
from Sprite import Sprite

debug=False

width,height=(1100,660)

firing_sound = pygame.mixer.Sound("src/sound/wopn/shoot.wav")
firing_sound.set_volume(0.25)


missile_sound3 = pygame.mixer.Sound("src/sound/wopn/missile3.wav")
missile_sound2 = pygame.mixer.Sound("src/sound/wopn/missile2.wav")

explosion_distant_001= pygame.mixer.Sound("src/sound/wopn/explosion_distant_001.mp3")
explosion_distant_002= pygame.mixer.Sound("src/sound/wopn/explosion_distant_002.mp3")
explosion_distant_003= pygame.mixer.Sound("src/sound/wopn/explosion_distant_003.mp3")

explosion_medium=pygame.mixer.Sound("src/sound/wopn/explosion_medium.mp3")
explosion_large=pygame.mixer.Sound("src/sound/wopn/explosion_large.mp3")
explosion_small=pygame.mixer.Sound("src/sound/wopn/explosion_small.mp3")


explod = pygame.mixer.Sound("src/sound/wopn/Explosion3.wav")
explod.set_volume(2)
explod1 = pygame.mixer.Sound("src/sound/wopn/Explosion.wav")



no_ammmo=pygame.mixer.Sound("src/sound/wopn/no-ammo.wav")
reloading=pygame.mixer.Sound("src/sound/wopn/reloading2.wav")

pl_shell1=pygame.mixer.Sound("src/sound/wopn/pl_shell1.wav")
pl_shell2=pygame.mixer.Sound("src/sound/wopn/pl_shell2.wav")
pl_shell3=pygame.mixer.Sound("src/sound/wopn/pl_shell3.wav")


player_exp=pygame.mixer.Sound("src/sound/wopn/player_exp.wav")

tankidle=pygame.mixer.Sound("src\\sound\\vehicle\\tank1.wav")


class Missile:
    spritesheet_1 = "src\img\weapons\smoke1.png" 
    spritesheet_2 = "src\img\weapons\smoke2.png"  
    spritesheet_3 = "src\img\weapons\smoke3.png"  
    spritesheet_4 = "src\img\weapons\smoke4.png"  
    spritesheet_5 = "src\img\weapons\smoke5.png" 
    
    def __init__(self,x,y,target,owner):
        self.x=x
        self.y=y
        self.target=target
        self.owner=owner
        self.spritesheet_path=random.choice([self.spritesheet_1,self.spritesheet_2,self.spritesheet_3,self.spritesheet_4,self.spritesheet_5])
        self.image=pygame.image.load('src/img/weapons/missile4.png').convert_alpha()
        self.sprite = Sprite(200,200,self.spritesheet_path, width=300, height=238, frame_width=25, frame_height=238, draw_limit=8)



        self.rect=self.image.get_rect()
        self.angle=0
        self.destroyed=False
        self.hitted=False

    mute=False


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
                self.destroyed=True
                if not self.mute:
                    explod.play()
                
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
    
    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()
    
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


    def mute_sound(self):
        self.mute=True

    def unmute_sound(self):
        self.mute=False

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

        if self.y<=-10:
                self.destroyed=True
                if not self.mute:
                    explod1.play()
        
        if self.hitted:
            self.destroyed=True


  

    def draw_missile(self,screen):
    
       
        if self.target.move_dir=="left":
            angle = self.get_colid_point_angle()
        else:
            angle = self.get_colid_point_angle()

        rotated_image = pygame.transform.rotate(self.image, angle)
        reect=rotated_image.get_rect()
        reect.center=(self.x,self.y)
        corner_pos=reect.center
    

        
        self.sprite.set_vars(corner_pos[0],corner_pos[1],angle-90)      
        self.sprite.update()
        self.sprite.draw(screen)
        
        screen.blit(rotated_image,reect)

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
    speed = 14

    def __init__(self, x, y,angle):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.moved_x=0
        self.moved_y=0
        self.hitted=False
        self.angle=angle
        self.destroyed=False
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.shoot_at(mouse_x, mouse_y)
        self.sprite = Sprite(200,200,self.spritesheet_path, width=75, height=3, frame_width=25, frame_height=3)

    mute=False


    spritesheet_path = "src/img/weapons/bullet4.png"  
   # image=pygame.image.load("src/img/weapons/bullet.png")
   # rect=image.get_rect()
    
       
    def get_width(self):
        return self.sprite.image.get_width()
    def get_height(self):
        return self.sprite.image.get_height()
    
    def mute_sound(self):
        self.mute=True

    def unmute_sound(self):
        self.mute=False

    def move_bullet(self):
        self.x += self.vel_x
        self.y += self.vel_y

        self.moved_x+=abs(self.vel_x)
        self.moved_y+=abs(self.vel_y)

        if self.out_of_range():
            pl_shell=random.choice([pl_shell1,pl_shell2,pl_shell3])
            if not self.mute:
                pl_shell.play()
            self.destroyed=True
    
        elif self.hitted:
            self.destroyed=True



    


    def draw_bullet(self,screen):
    
        # rotated_image = pygame.transform.rotate(self.image, self.angle)
        # rotated_rect = rotated_image.get_rect()
        # rotated_rect.topleft = (self.x, self.y)
        
        self.moved_y=abs(self.moved_y)
        self.moved_x=abs(self.moved_x)
        xy=self.moved_y+self.moved_x
        xy=round(xy)


        self.sprite.set_vars(self.x,self.y,self.angle)
        self.sprite.update()
        self.sprite.draw(screen)
        
      #  screen.blit(rotated_image, rotated_rect)

        

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
        self.effects=[]
        self.selected=0
        self.moving_dir='right'
        self.barrel_position=(self.x+20,self.y+29)
        self.barrel_top_right=0
        self.barrel_top_center=0
        self.sprite=Sprite(self.x,self.y,self.sprite_sheet,536,68,134,68)
        self.sprite_left=Sprite(self.x,self.y,self.sprite_sheet_left,536,68,134,68)
       
        self.sprite.update()
        self.idle=self.sprite.first_image
        self.rect=self.idle.get_rect()
        


    magazine_size=120
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

    effect1='src\\img\weapons\\effect_sprite.png'
    effect2='src\\img\weapons\\effect_sprite2.png'
    effect3='src\\img\weapons\\effect_sprite3.png'

    

    sprite_sheet=('src/img/vehicles/gepard_sheet.png')
    sprite_sheet_left=('src/img/vehicles/gepard_sheet-left.png')
    barrel1=pygame.image.load('src/img/vehicles/vhc_barrel.png')
    barrel2=barrel1
    barrel_width,barrel_height=barrel1.get_size()

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
    reload_delay=4500
    pods_reload_delay=4000
    reload_start_time=0
    pods_reload_start_time=0
    radar_range=900
    radar_max_left=0
    radar_min_height=250
    reload_started=False
    move_sound_started=False
    barrel_rect=barrel1.get_rect()
    mute=False


    def mute_sound(self):
        self.mute=True
    def unmute_sound(self):
        self.mute=False   

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
        self.magazine=magazine                                      #120
        self.missiles_storage=missiles_storage                      #12
        self.ready_to_fire_missiles=ready_to_fire_missiles          #4
    
    def get_rect(self):
        self.rect.topleft=(self.x,self.y)
        return  self.rect
    
    def get_width(self):
        return self.idle.get_width()
    
    def get_height(self):
        return self.idle.get_height()

    def get_centerx(self):
        center_x=self.x+(self.get_width()//2)
        return center_x
    
    def get_centery(self):
        center_y=self.y+(self.get_height()//2)
        return center_y

    def reload_sound(self):
        if not self.reload_started:
            self.reload_started=True
            if not self.mute:
                reloading.play()

    def move_sound(self):
        if not self.move_sound_started:
            self.move_sound_started=True
            tankidle.play(-1)

    def fade_out_sound(self):
        tankidle.fadeout(100)

    def move_player(self):

        self.update_last_known_position()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            
            vel_x = -self.move_speed
            self.moving_dir='left'
            self.moving=True
            
            

        elif  keys[pygame.K_d]:
            self.moving_dir='right'
            vel_x = self.move_speed
            self.moving=True
            


        else:
            vel_x = 0
            self.moving=False
            self.move_sound_started=False
            tankidle.fadeout(100)

        self.x += vel_x
        self.x = max(0, min(self.x, width - self.get_width()))

        
        if self.moving:
            if not self.mute:
                self.move_sound()


    def mouse_collid_player(self):
        mouse=pygame.mouse.get_pos()

        if self.get_rect().collidepoint(mouse) or self.barrel_rect.collidepoint(mouse):

            return True
        else:
            return False

    def update_player(self,screen):
        self.rect.topleft = (self.x, self.y)
  
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        angle_radians = math.atan2(mouse_y - (self.y + 31), mouse_x - (self.x + 60))
        angle = math.degrees(angle_radians)
        angle=-angle

        if angle<=0 and angle>=-90:
            angle=0
        elif angle >=180 or angle <=-90:
             angle=180
        self.bullet_angle=angle


        barrel2 = pygame.transform.rotate(self.barrel2, angle)
        barrel1 = pygame.transform.rotate(self.barrel1, angle)

        rotated_rect = barrel1.get_rect()
        rotated_rect.center = (self.x+55, self.y+27)
        

        rotated_rect2 = barrel2.get_rect()
        rotated_rect2.center = (self.x+60, self.y+31)

        self.barrel_rect=rotated_rect2
        self.barrel_rect.center = (self.x+60, self.y+31)

        if angle>=90:
            self.barrel_top_right=(rotated_rect2.topleft)
        else:
            self.barrel_top_right=(rotated_rect2.topright)

        if angle>=80 and angle<=100:
            self.barrel_top_right=(rotated_rect2.midtop)
        
        self.barrel_top_center=rotated_rect2.center
     
        screen.blit(barrel1, rotated_rect)


        if self.moving:
            if self.moving_dir=='left':
                self.sprite_left.set_vars(self.x,self.y,0)
                self.sprite_left.update()
                self.sprite_left.draw_topleft(screen)
                self.idle=self.sprite_left.first_image

            elif self.moving_dir=='right':
                self.sprite.set_vars(self.x,self.y,0)
                self.sprite.update()
                self.sprite.draw_topleft(screen)
                self.idle=self.sprite.first_image

        else:
            rectt=self.idle.get_rect()
            rectt.topleft=(self.x,self.y)
            screen.blit(self.idle,rectt)


        screen.blit(barrel2, rotated_rect2)

        for effect in self.effects:
            effect.update()
            effect.draw(screen)
            if effect.end_draw:
                self.effects.remove(effect)
       
        


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

            self.reload_started=False


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
                self.reload_sound()
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
            if not self.mouse_collid_player():
                if current_time - self.last_shot_time >= self.shoot_delay:
                    if self.bullet_angle>=179 or self.bullet_angle<=1:
                        return False
                    else:
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
            
            bullet = Bullet(self.barrel_top_right[0],self.barrel_top_right[1],self.bullet_angle)
            self.bullets.append(bullet)

            effect_sprite_sheet=random.choice([self.effect1,self.effect2,self.effect3])

            effect= Sprite(self.x,self.y,effect_sprite_sheet,750,38,250,38,2,self.bullet_angle)

            effect.set_vars(self.barrel_top_center[0],self.barrel_top_center[1],self.bullet_angle)

            self.effects.append(effect)

            # bullet2 = Bullet(self.x+70  // 2, self.y+32)
            # bullet2.shoot_at(target_x, target_y)
            # bullet2.rotate_bullet()
            # self.bullets.append(bullet2)

            self.last_shot_time = pygame.time.get_ticks()
            self.reload_start_time=self.last_shot_time
       
            if not self.mute:
                firing_sound.play()
            
            

    def move_bullets(self):
        for bullet in self.bullets:
            if  self.mute:
                bullet.mute_sound()
            else:
                if bullet.mute:
                    bullet.unmute_sound()

            bullet.move_bullet()
            if bullet.destroyed:
                self.bullets.remove(bullet)

    def move_missiles(self):
        for mis in self.missiles:
            if  self.mute:
                mis.mute_sound()
            else:
                if mis.mute:
                    mis.unmute_sound()

            mis.hit_target()
            mis.move_misile()
            if mis.destroyed:
                self.missiles.remove(mis)


            
            
          

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

        radar_angle=list(range(int(max_left),int(max_right)))
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
                missile_sound=random.choice([missile_sound2,missile_sound3])
                if not self.mute:
                    missile_sound.play()


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
        if self.health<=0:
            self.destroyed=True
 

class Bomb:
    mute=False
    def __init__(self,x,y,velx,vely,guided,angle):
        self.x=x
        self.y=y
        self.width=4
        self.height=6
        self.velx=velx
        self.vely=vely
        self.guided=guided
        self.target=False
        self.dmage=25
        self.exploded=False
        self.angle=angle
        self.image=pygame.image.load('src/img/weapons/bomb.png')
        self.rect=self.image.get_rect()
        self.agm=pygame.image.load('src/img/weapons/agm2.png')
        self.agm_rect=self.agm.get_rect()
        self.max_velocity=1
    
        self.moved_x=0
        self.target=None
  

    def set_target(self,target):
        self.target=target

    def get_rect(self):
        return  self.rect
    
    def mute_sound(self):
        self.mute=True

    def unmute_sound(self):
        self.mute=False

    def get_centerx(self):
        return self.x
        
    def get_center_y(self):
        return self.y


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
            rotated_image = pygame.transform.rotate(self.agm, angle)
            rotated_rect = rotated_image.get_rect()
            self.rect.topleft=(self.x,self.y)
            rotated_rect.topleft = (self.x, self.y)
            screen.blit(rotated_image,rotated_rect)


        if debug:
            pygame.draw.rect(screen,('black'),self.get_rect())
#            pygame.draw.rect(screen,('red'),(xy[0],xy[1],10,10))

        
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
        movement = distance * self.max_velocity

        self.x += movement.x
        self.y += movement.y

        # self.moved_x+=abs(movement.x)
        # if self.moved_x>=700:
        #     self.y+=0.1
       

           

    def dum_move(self):
        self.y+=self.vely
        self.x+=self.velx



    def is_hit_object(self,objects):
        for obj in objects:
            if self.get_rect().colliderect(obj.get_rect()):
                self.exploded=True
                obj.bombed(self.dmage)
                sound=player_exp
                if not self.mute:
                    sound.play()


        
    def status(self,screen):

        if self.y >= 570:
            self.exploded=True
            sound=random.choice([explosion_distant_001,explosion_distant_002,explosion_distant_003,explosion_medium,explosion_small])
            if not self.mute:
                sound.play()




class Ally:
    def __init__(self, x, y, frame_width, frame_height):
        self.spritesheet = pygame.image.load("src/img/vehicles/HMV3.png")
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
        hb_bar=pygame.Rect(self.x-40,self.y-80,self.health_percentage,10)

        if self.health_percentage>=70 and self.health_percentage<=100:
            color='green'

        elif self.health_percentage>=50  and self.health_percentage<=69:
            color='yellow'

        elif self.health_percentage>=1 and self.health_percentage<=49:
            color='red'

        pygame.draw.rect(screen,color,hb_bar)
        self.health_percentage = (self.actual_health / self.base_health) * 100

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
        self.turning_opposite_direction=True
        self.turn_opposite_direction_times=0
        

    explode_sprite_sheet= 'src/img/weapons/Explosion.png'
    lock_sprite=pygame.image.load('src/img/weapons/lock.png')
    lock_sprite_rect=lock_sprite.get_rect()
    track_sprite=pygame.image.load('src/img/weapons/track.png')
    track_sprite_rect=track_sprite.get_rect()
    lock_sprite_width=lock_sprite.get_width()
    mute=False

        
    def mute_sound(self):
        self.mute=True

    def unmute_sound(self):
        self.mute=False

    def get_center_y(self):
        return self.y+self.left_sprite.get_height()//2

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
            target_attak_range=list(range(int(target_x-self.shooting_range),int(target_x+self.shooting_range)))
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
                                    bomb=Bomb(self.get_centerx(),self.y,x_vel,y_vel,False,136)
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
                                    
                                bomb.set_target(target)
                                self.bombs.append(bomb)
                                self.last_bomb_time = pygame.time.get_ticks()
                                self.guided_bomb-=1
        


    def set_x(self,x):
        self.x=x

    def effect(self,screen):
        pygame.draw.rect(screen, pygame.Color('orange'), (self.x, self.y, self.get_width()+5, self.get_height()+5))


    def get_rect(self):
        return  self.left_sprite_rect
    
    def get_angl(self,rect1, rect2):

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

    def kamikaze_move(self,target,screen):
        xy=self.target.get_last_known_position()
        x_distance = xy[0] - self.x
        y_distance = xy[1] - self.y
        distance = pygame.math.Vector2(x_distance, y_distance)
        distance.normalize_ip()
        movement = distance * self.vel

        self.x += movement.x
        self.y += movement.y
       
        if self.y>=550:
            self.destroyed=True

        self.check_hit_player(target,screen)
            


    def side_move(self):

        if self.move_dir=='right':
            self.x+=self.vel

            if self.turning_opposite_direction:
                
                if self.x>width-self.get_width()-5:
                    self.move_dir='left'
                    self.turn_opposite_direction_times+=1

                    self.recharge()
                
         

        elif self.move_dir=="left":
            self.x-=self.vel

            if self.turning_opposite_direction:
                
                if self.x<5:
                    self.move_dir='right'
                    self.turn_opposite_direction_times+=1
                    self.recharge()


        if self.turn_opposite_direction_times>=2:
            self.turning_opposite_direction=False


        if self.y>=550:
            self.destroyed=True


        if not self.turning_opposite_direction:
            if self.x<-200 or self.x >1300:
                self.destroyed=True
            
    



            

    def move_enemy(self,screen):
        if not self.destroyed:
            if not self.kamikaze:
                self.side_move()
            else:
                self.kamikaze_move(self.target,screen)
 
    



    def update_enemy(self,screen):

       
        

        if debug:
            pygame.draw.rect(screen,('black'),self.get_rect())


        

        self.left_sprite_rect.topleft=(self.x,self.y)
        self.right_sprite_rect.topleft=(self.x,self.y)

        if not self.kamikaze:
            if self.move_dir=="left":
                screen.blit(self.left_sprite,self.left_sprite_rect)
            else:
                screen.blit(self.right_sprite,self.right_sprite_rect)

        if self.kamikaze:
            angle=self.get_angl(self.get_rect(),self.target.get_rect())
            rotated_image = pygame.transform.rotate(self.left_sprite,angle+180)
            rotated_rect = rotated_image.get_rect()
            rotated_rect.topleft = (self.x, self.y)
            screen.blit(rotated_image,rotated_rect)

            

        if self.locked:
            rect_center=self.track_sprite_rect.topleft=(self.get_centerx()-15,self.y-3)
            screen.blit(self.track_sprite,rect_center)


        elif self.tracked:
            rect_center=self.lock_sprite_rect.topleft=(self.get_centerx()-15,self.y-3)
            screen.blit(self.lock_sprite,rect_center)



 


    def check_hit_player(self,target,screen):
        if self.get_rect().colliderect(target.get_rect()):
            self.destroyed=True
            self.effect(screen)
            sound=player_exp
            if not self.mute:
                sound.play()
            if target.health -80 <=0:
                target.health=0

            else:
                target.health-=80
    
    
    def is_taken_damage(self):
        if self.damaged==True:
            return True
        else:
            return False

    def check_kill(self, bullets,missiles):
        for bullet in bullets:
            if (self.x < bullet.x + bullet.get_width() and
                self.x + self.get_width() > bullet.x and
                self.y < bullet.y + bullet.get_height() and
                self.y + self.get_height() > bullet.y):
                bullet.hitted=True
                self.health-=15
                self.damaged=True
                if self.health<0:
                    self.destroyed=True
                    if not self.mute:
                        explod.play()
                    return True
                    

        return False
    
    def recharge(self):
        self.bomb_count=self.charg