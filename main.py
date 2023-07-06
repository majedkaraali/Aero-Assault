import pygame
import random
from pygame.locals import *
import sys
pygame.init()

width=1100
height=640

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Create game states
font = pygame.font.Font(None, 24)

enemy_list=[]
pygame.mixer.init()





free_play_button = pygame.draw.rect(screen, (0, 0, 255), (20, 20, 200, 50))
free_play_text = font.render("Free Play", True, (255, 255, 255))
free_play_text_rect = free_play_text.get_rect(center=free_play_button.center)
screen.blit(free_play_text, free_play_text_rect)


missions_button = pygame.draw.rect(screen, (0, 255, 0), (20, 90, 200, 50))
missions_text = font.render("Missions", True, (255, 255, 255))
missions_text_rect = missions_text.get_rect(center=missions_button.center)
screen.blit(missions_text, missions_text_rect)

shop_button = pygame.draw.rect(screen, (255, 0, 0), (20, 160, 200, 50))
shop_text = font.render("Shop", True, (255, 255, 255))
shop_text_rect = shop_text.get_rect(center=shop_button.center)
screen.blit(shop_text, shop_text_rect)

exit_button = pygame.draw.rect(screen, (255, 0, 0), (20, 230, 200, 50))
exit_text = font.render("Exit", True, (255, 255, 255))
exit_text_rect = exit_text.get_rect(center=exit_button.center)
screen.blit(exit_text, exit_text_rect)
# Set the initial game state


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


class Player:
    x=350
    y=566
    width=50
    height=50
    player_alive=True
    vel_x = 0
    vel_y = 0
    move_speed = 6
    bullets = []
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

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.draw_bullet()



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



    def update_enemy(self):
        en = pygame.draw.rect(screen, (29, 84, 158), (self.x, self.y, self.width, self.height))

    def check_collision(self, bullet_list):
        for bullet in bullet_list:
            if (self.x < bullet.x + bullet.width and
                self.x + self.width > bullet.x and
                self.y < bullet.y + bullet.height and
                self.y + self.height > bullet.y):
                return True
        return False










def generate_enemies(num_of_enemies):
    if len(enemy_list)<num_of_enemies:
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
        enemy_list.append(enemy)







class GameState:
    def __init__(self):
        self.running = False

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class MenuState(GameState):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.running=True


        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if free_play_button.collidepoint(mouse_pos):
                    print("Clicked Free Play button")
                    self.running = False
                    return "free_play"
                elif missions_button.collidepoint(mouse_pos):
                    print("Clicked Missions button")
                    
                elif shop_button.collidepoint(mouse_pos):
                    print("Clicked Shop button")
                    
                elif exit_button.collidepoint(mouse_pos):
                    print("Clicked Exit button")
                    



    def draw(self, screen):
        pass
       
       
     

class FreePlayState(GameState):
    p1=Player()
    paues=False
    def __init__(self):
        super().__init__()
        self.running=True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC key pressed")
                    if (self.paues):
                        self.paues=False
                    elif (not self.paues):
                        self.paues=True
                    print(self.paues)
                
            # Handle other events specific to the free play mode

    def draw(self, screen):
        if not (self.paues):
            clock.tick(60)
            screen.fill('aqua')

            self.p1.move_player()
            self.p1.update_player()
            self.p1.move_bullets() 
            self.p1.update_bullets() 
            generate_enemies(2)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.p1.shoot()


            enemies_to_remove = []
            bullets_to_remove = []

            for enemy in enemy_list:
                if enemy.check_collision(self.p1.bullets):
                    enemies_to_remove.append(enemy)

            for bullet in self.p1.bullets:
                if bullet.y < 0:
                    bullets_to_remove.append(bullet)

            for enemy in enemy_list:
                pass

            for enemy in enemies_to_remove:
                enemy_list.remove(enemy)

            for bullet in bullets_to_remove:
                self.p1.bullets.remove(bullet)

        
            for enemy in enemy_list:
                enemy.move_enemy()
                enemy.update_enemy()

            self.p1.update_bullets()
            
        
    






menu_state = MenuState(screen)
free_play_state = FreePlayState()
current_state = menu_state

while current_state.running:
    
    events = pygame.event.get()
   
    next_state = None  # Initialize next_state variable

    for event in events:
        if event.type == pygame.QUIT:
            current_state.running = False

    
    
    next_state = current_state.handle_events(events)
    current_state.update()
    current_state.draw(screen)

    if next_state == "free_play":
        current_state = free_play_state


    pygame.display.flip()





pygame.quit()
