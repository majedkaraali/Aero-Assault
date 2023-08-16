import pygame

class Sprite():
    def __init__(self, x, y, frame_width, frame_height):
        self.spritesheet = pygame.image.load("src/img/HMV3.png")
        self.sprite_width=self.spritesheet.get_width()
        self.sprite_height= self.spritesheet.get_height()
        self.x=x
        self.y=y
        self.frames = []  
        self.current_frame = 0

        
        self.load_frames(self.sprite_width, self.sprite_height, frame_width, frame_height)
    
    def load_frames(self, width, height, frame_width, frame_height):
        for y_offset in range(0, height, frame_height):
            for x_offset in range(0, width, frame_width):
                frame_rect = pygame.Rect(x_offset, y_offset, frame_width, frame_height)
                frame = self.spritesheet.subsurface(frame_rect)
                self.frames.append(frame)

    def move(self):
        self.x+=1
        

    def draw(self,screen):
        screen.blit(self.frames[self.current_frame], (self.x, self.y))
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0  


pygame.init()

clock=pygame.time.Clock()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sprite Example")




sprite = Sprite(20,20,88,46)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((22, 44, 88))  
    
    sprite.draw(screen)
    sprite.move()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
