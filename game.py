import random 
import pygame
pygame.init()
WIDTH=1280
HEIGHT=677
win=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hunt")

class Player:
    x=350
    y=566
    width=50
    height=50
    player_alive=True
    score=0
    vel_x = 0
    vel_y = 0
    move_speed = 6

    def move_player(self):
        if keys[pygame.K_LEFT]:
            vel_x = -self.move_speed
        elif keys[pygame.K_RIGHT]:
            vel_x = self.move_speed
        else:
            vel_x = 0

        self.x += vel_x
        self.x = max(0, min(self.x, WIDTH - self.width))
        
    def update_player(self):
        pl = pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))




class Enemy:
    x=300
    y=10
    width=50
    height=50
    def set_x(self,x):
        self.x=x
    def move_enemy(self):
        self.y+=2
    def update_enemy(self):
        en = pygame.draw.rect(win, (29, 84, 158), (self.x, self.y, self.width, self.height))



p1=Player()

enemy_lsit=[]
clock = pygame.time.Clock()
pygame.font.init()
pygame.mixer.init()

for i in range(5):
    enemy=Enemy()
    enemy.set_x(random.randint(1,WIDTH))
    enemy_lsit.append(enemy)


def generate_enemies():
    pass



run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    clock.tick(60)
    win.fill('aqua')

    p1.move_player()
    p1.update_player()



    for enemy in enemy_lsit:
        enemy.move_enemy()
        enemy.update_enemy()

    pygame.display.update()

    

pygame.quit()