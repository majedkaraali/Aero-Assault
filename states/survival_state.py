import os
import pygame 
from objects import objects
from windows import game_windows
from .Game import GameState

statics_image=pygame.image.load('src/img/backgrounds/statics.png').convert_alpha()
font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
font_size = 19 
font = pygame.font.Font(font_path, font_size)

        

width,height=(1100,660)
windo=game_windows()


class Survival(GameState):
    def __init__(self,state):
        super().__init__()
        self.state=state
        self.buttons=windo.get_buttons()
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

      



    def handle_events(self, events):
        for event in events:

            if event.type == pygame.QUIT:
                self.running = False


    
            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.conform:
        
                    if windo.ok_button.holding:
                        self.conform=False
                        self.play_conformed=True

                if self.pause:
                    if windo.main_menu_button.holding:
                        self.state.menu_state()

                    if windo.resume_button.holding:
                        self.pause=False


          


                if self.lose:
                 
                        
                    if windo.main_menu_button.holding:
                        self.state.menu_state()

                    if windo.retry.holding:
                        self.state.survival_state()


                
            
            
        if self.complete or self.reward_screen or self.pause or self.tutorial or self.lose or self.conform:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)



    

    def handle_reward(self,screen):
        windo.reward_window()
        windo.draw_frames(screen)

    def handle_pause(self,screen):
        windo.puse_window()
        windo.draw(screen)
        windo.draw_frames(screen)


    def handle_lose(self,screen):
        windo.survival_lose_window(screen,self.score)
        windo.draw(screen)
        windo.draw_frames(screen)

    def handle_conform(self,screen):
        windo.survival_description_frame()
        windo.draw(screen)
        windo.draw_frames(screen)