import os
import pygame 
from objects import objects
from windows import game_windows
from .Game import GameState
import random
from Sprite import Sprite
statics_image=pygame.image.load('src/img/backgrounds/statics.png').convert_alpha()
font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
font_size = 19 
font = pygame.font.Font(font_path, font_size)

        

width,height=(1100,660)

button_click=pygame.mixer.Sound("src\\sound\\ui\\btn_click.wav")


class Survival(GameState):
    def __init__(self,state):
        super().__init__()
        self.state=state
        self.windo=game_windows()
        self.buttons=self.windo.get_buttons()
        self.base=None
        self.bombs=[]
        self.ground_vhls=[]
        self.enemies_to_remove = []
        self.conform=True
        self.background=pygame.image.load('src/img/maps/CelestialRuins.png').convert_alpha()
        self.ground_vhls.append(self.player)
        self.enemies_to_respawn=1
        self.score=0
        self.player.loadout([1680,240,12,4])


        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos((1000, 500))



    

    def draw(self,screen):
        screen.blit(self.background,self.background.get_rect())
        self.statics(screen)
        self.update_game(screen)


    def statics(self,screen):
        super().statics(screen)

        score =str(self.score)
        score_text = font.render("score: "+score, True, ('black'))
        score_text_pos=(10,height-25)
        screen.blit(score_text,score_text_pos)




    def update_game(self, screen):
        if self.can_play() and not self.conform:
            
            self.handle_player(screen)
            self.handle_bullets(screen)
            self.handle_missiles()
            self.handle_enemies(screen)
            self.handle_bombs(screen)
            self.handle_keys()
            self.crosshair(screen)
            self.handle_waves()
            self.handle_drops()
            self.handle_base(screen)
            self.clean_enemies()
    

 
        elif self.pause:
            self.handle_pause(screen)
        elif self.lose:
            self.handle_lose(screen)



        elif self.conform:
            if not self.tutorial:
                self.handle_conform(screen)




    def generate_enemies(self,num):
        self.enemy_list=self.enemies.all_time_enemies(num)


    def handle_waves(self):

        if self.score>=200:
            self.enemies_to_respawn=2

        if  self.score>=1000:
            self.enemies_to_respawn=3

        if  self.score>=2500:
            self.enemies_to_respawn=4

        if  self.score>=5000:
            self.enemies_to_respawn=5

        if  self.score>=10000:
            self.enemies_to_respawn=6

        if len(self.enemy_list)==0:
            self.generate_enemies(self.enemies_to_respawn)   

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
                self.score+=100
                self.enemies_to_remove.append(enemy)
                drop=objects.Item(enemy.get_centerx(),enemy.y,'gift')
                self.player.drops.append(drop)
                explode_sprite_sheet1= 'src/img/weapons/Explosion.png'
                explode_sprite_sheet2= 'src/img/weapons/Explosion2.png'
                explode_sprite_sheet3= 'src/img/weapons/Explosion3.png'
                explode_sprite_sheet=random.choice([explode_sprite_sheet1,explode_sprite_sheet2,explode_sprite_sheet3])
                explode_sprite=Sprite(enemy.get_centerx(),enemy.get_center_y(),explode_sprite_sheet,1536,96,96,96,1,0)
                self.explodes.append(explode_sprite)

      



    def handle_events(self, events):
        for event in events:

            if event.type == pygame.QUIT:
                self.running = False


    
            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.conform:
        
                    if self.windo.ok_button.holding:
                        button_click.play()
                        self.conform=False
                        self.player.last_shot_time=pygame.time.get_ticks()
                        self.play_conformed=True

                if self.pause:
                    if self.windo.main_menu_button.holding:
                        button_click.play()
                        self.state.menu_state()

                    if self.windo.resume_button.holding:
                        button_click.play()
                        self.player.last_shot_time=pygame.time.get_ticks()
                        self.pause=False
                        


          


                if self.lose:
                 
                        
                    if self.windo.main_menu_button.holding:
                        button_click.play()
                        self.state.menu_state()

                    if self.windo.retry.holding:
                        button_click.play()
                        self.state.survival_state()


                
            
            
        if self.complete or self.reward_screen or self.pause or self.tutorial or self.lose or self.conform:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)



    

    def handle_reward(self,screen):
        self.player.fade_out_sound()
        self.windo.reward_window()
        self.windo.draw_frames(screen)

    def handle_pause(self,screen):
        self.windo.puse_window()
        self.windo.draw(screen)
        self.windo.draw_frames(screen)


    def handle_lose(self,screen):
        self.player.fade_out_sound()
        self.windo.survival_lose_window(screen,self.score)
        self.windo.draw(screen)
        self.windo.draw_frames(screen)

    def handle_conform(self,screen):
        self.windo.survival_description_frame()
        self.windo.draw(screen)
        self.windo.draw_frames(screen)