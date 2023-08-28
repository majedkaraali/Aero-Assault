import pygame
import os

class Sprite:
    def __init__(self, x, y ,spritesheet_path, width, height, frame_width, frame_height, draw_limit=-1,angle=0):
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.width = width
        self.height = height
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.draw_limit = draw_limit
        self.draw_count = 0
        self.current_frame = 0
        self.image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.x=int(x)
        self.y=int(y)
        self.end_draw=False
        self.angle=angle
        self.first_image=None
        self.first_image_taken=False

        self.topleft=(0,0)
        self.topright=(0,0)
        self.bottomleft=(0,0)
        self.bottomright=(0,0)
        self.midbottom=(0,0)
        self.midtop=(0,0)
        self.midleft=(0,0)
        self.midright=(0,0)


    def change_spritesheet(self,spritesheet):
        self.spritesheet=spritesheet
    
  
    def get_rect(self):
        return self.image.get_rect()
    
    def set_corners(self,topf,topr,botf,botr,midl,midr,midt,midb):
        self.topleft=topf
        self.topright=topr
        self.bottomleft=botf
        self.bottomright=botr
        self.midleft=midl
        self.midright=midr
        self.midtop=midt
        self.midbottom=midb

    def set_vars(self,x,y,angle):
        self.x=int(x)
        self.y=int(y)
        self.angle=angle

    def update(self):
        self.current_frame += 1
        if self.current_frame * self.frame_width >= self.spritesheet.get_width():
            self.current_frame = 0
            self.draw_count += 1

            if self.draw_limit != -1 and self.draw_count >= self.draw_limit:
                self.end_draw = True

        self.image = self.spritesheet.subsurface(
            pygame.Rect(
                self.current_frame * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            )
        )
        if not self.first_image_taken:
            self.first_image=self.image

    def draw(self, screen):

        rotated_image=pygame.transform.rotate(self.image,self.angle)
        image_rect = rotated_image.get_rect()
        image_rect.center=(self.x,self.y)
         
    
        
        if not self.end_draw:
            screen.blit(rotated_image,image_rect)

    def draw_topleft(self, screen):

        rotated_image=pygame.transform.rotate(self.image,self.angle)
        image_rect = rotated_image.get_rect()
        image_rect.topleft=(self.x,self.y)
         
    
        
        if not self.end_draw:
            screen.blit(rotated_image,image_rect)
          