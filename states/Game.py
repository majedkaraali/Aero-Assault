import os
import pygame 
from objects import objects
from windows import game_windows
from EnemyMaker import Generate_enemies


crosshair_image = pygame.image.load("src\img\weapons\crosshair.png")
crosshair_rect = crosshair_image.get_rect()

font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
font_size = 19 
font = pygame.font.Font(font_path, font_size)

background_path= os.path.join("src/fonts", "OCRAEXT.ttf") 
statics_image=pygame.image.load('src/img/backgrounds/statics.png').convert_alpha()


width,height=(1100,660)

class GameState():

    def __init__(self):
        self.running = False
        self.lose=False
        self.force_reload=False
        self.play_conformed=False
        self.complete=False
        self.game_over=False
        self.close=False
        self.mouse_button_pressed=False
        self.pause=False
        self.reward_screen=False
        self.tutorial=False

        self.wave=0
        self.score=0

        self.player=objects.Player(540,height-107,'Unnamed')
        self.enemies=Generate_enemies(self.player)

        self.enemy_list=[]
        self.enemies_to_remove = []
        
        

        

    def handle_events(self, events):
        pass

    def draw(self):
        pass
    
    def update_game(self):
        pass









    def generate_enemies(self,wave):
        self.enemy_list=self.enemies.respawn_wave(wave)
           

    def get_enemies(self):
        return self.enemy_list
    
        
    def statics(self,screen):
        statics_rect=statics_image.get_rect()
        statics_rect.topleft=(0,630)

        screen.blit(statics_image,statics_rect)

        if self.player.reloading:
            magazine='---'
        else:
            magazine=str(self.player.magazine)
        bullets=str(self.player.ammo)

        if self.player.reloading_pods:
            missiles='--'
        else:
            missiles=self.player.ready_to_fire_missiles

        storage=self.player.missiles_storage
        bullets_text = font.render(f"bullets: {magazine}/{bullets}", True, 'black')
        bullets_text_pos=(width-375,height-25)
        missiles_text = font.render(f"missiles: {missiles}/{storage}", True, 'black')
        missiles_text_pos=(width-550,height-25)
        heath_value=self.player.health
        heatl_text = font.render(f"health: {str(heath_value)}", True, 'black')
        heatl_text_pos=(width-170,height-25)

        screen.blit(bullets_text, bullets_text_pos)
        screen.blit(missiles_text, missiles_text_pos)
        screen.blit(heatl_text, heatl_text_pos)





    def can_play(self):
        return not (self.lose or self.tutorial or self.pause or self.game_over or self.complete ) #or self.play_conformed  )
    

    def handle_player(self,screen):
        if not self.player.forced:
            self.player.move_player()
            self.player.update_player(screen)
            self.player.update_bullets(screen)
            self.player.move_bullets() 
            self.player.move_missiles()
            self.player.update_missiles(screen)
            self.player.chek_magazine()
            self.player.chek_missile_lounchers_pods()
            self.player.move_drops(screen,self.player)
            self.player.is_destroyed()   
            self.player.get_enemies=self.get_enemies()

        if self.player.destroyed:
            self.game_over=True
            self.lose=True 


    def handle_enemies(self,screen):
         
         for enemy in self.enemy_list:
            enemy.move_enemy(screen)
            enemy.update_enemy(screen)
            enemy.check_kill(self.player.bullets,self.player.missiles)
            enemy.attack(self.player)

            for bomb in enemy.bombs:
                if bomb not in  self.bombs and not bomb.exploded:
                    self.bombs.append(bomb)

            if enemy.destroyed:
                self.enemies_to_remove.append(enemy)
                drop=objects.Item(enemy.get_centerx(),enemy.y,'gift')
                self.player.drops.append(drop)





    def handle_bombs(self,screen):

        for bomb in self.bombs:
            bomb.move()
            bomb.draw(screen)
            bomb.is_hit_object(self.ground_vhls)
            bomb.status(screen)

            if bomb.exploded==True:
                self.bombs.remove(bomb)

    def clean_enemies(self):
        if len(self.enemies_to_remove)>0:
            for enemy in self.enemies_to_remove:
                enemy.destroyed=True
                if enemy in self.enemy_list:
                    self.enemy_list.remove(enemy)

    def crosshair(self,screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        crosshair_rect.center = (mouse_x, mouse_y)
        screen.blit(crosshair_image, crosshair_rect)


    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
                self.player.shoot()

        elif keys[pygame.K_f]:
                self.player.fire_missile(self.player)

        elif keys[pygame.K_TAB]:
                self.player.next_lock()

        elif keys [pygame.K_r]:
            self.player.reload_start_time=pygame.time.get_ticks()
            self.player.droped_ammo+=self.player.magazine
            self.player.magazine=0

        elif keys[pygame.K_ESCAPE]:
            if  not self.complete and not self.pause:
                self.pause = True

            elif self.pause:
                self.pause=False


        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:  
            if not self.player.forced or self.pause or self.tutorial:
                self.player.shoot()



    def handle_base(self,screen):

        pass       # Method Found In states/level_play_state.py


    def handle_allies(self,screen):

        pass        # Method Found In states/level_play_state.py

    def handle_waves(self):

        pass        # Method Found In states/all states in the folder


    def handle_bullets(self,screen):
        pass
    
    def handle_missiles(self):
        pass  

    def handle_drops(self):
        pass