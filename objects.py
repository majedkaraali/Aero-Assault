import pygame
import random

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
                self.target.destroyed=True
                chanse=random.randint(1,2)
                if chanse==1:
                    from main import Item
                    drop=Item(self.target.get_centerx(),self.target.y,'gift')
                    self.owner.drops.append(drop)
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
        from main import screen

        screen.blit(rotated_rect, (self.x - x_adjustment,self.y - y_adjustment))