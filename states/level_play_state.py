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


class Level_Play(GameState):
    def __init__(self,state,level):
        super().__init__()
        self.state=state
        self.buttons=windo.get_buttons()
        self.allies=False
        self.level=level
        self.base=None
        self.bombs=[]
        self.ground_vhls=[]
        self.enemies_to_remove = []

        self.background_path=level.background_path
        self.background=pygame.image.load(self.background_path).convert_alpha()
        self.player.loadout(level.player_loadout)
        self.ground_vhls.append(self.player)


        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos((1000, 500))

        

        if level.tutorial:
            self.tutorial_image_path=level.tutorial_image
            self.tutorial=True


        

        if level.allies:
            self.allies=True
            self.allies_list=[]
            ally_start_point=-400
            for ally in range(level.allies_count):
                ally=objects.Ally(ally_start_point,height-95,88,46)
                self.allies_list.append(ally)
                ally_start_point-=100
            self.ground_vhls.extend(self.allies_list)

        if level.base:
            self.base=objects.Base(level.base_loc[0],level.base_loc[1],level.base_hp)
            self.ground_vhls.append(self.base)
    
    

    def draw(self,screen):

        screen.blit(self.background,self.background.get_rect())
        self.statics(screen)
        self.update_game(screen)


    def statics(self,screen):
        super().statics(screen)

        wave =str(self.wave)
        wave_text = font.render("wave: "+wave, True, ('black'))
        wave_text_pos=(10,height-25)
        screen.blit(wave_text,wave_text_pos)


    def update_game(self, screen):
        if self.can_play():
            self.handle_player(screen)
            self.handle_allies(screen)
            self.handle_base(screen)
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
    
        elif self.complete:
            self.handle_complete(screen)
        elif self.reward_screen:
            self.handle_reward(screen)
        elif self.pause:
            self.handle_pause(screen)
        elif self.tutorial:
            self.handle_tutorial(screen)
        elif self.lose:
            self.handle_lose(screen)



    def handle_base(self,screen):

        if self.base:
            self.base.draw(screen)
            if self.base.destroyed:
                self.lose=True 
 

    def handle_allies(self,screen):

        if self.allies:
            if len(self.allies_list)==0:
                self.lose=True

            for ally in self.allies_list:
                ally.move()
                ally.status(self.bombs)
                ally.draw(screen)
                if ally.destroyed:
                    self.allies_list.remove(ally)


    def handle_waves(self):
        if len(self.enemy_list)==0:
            self.wave+=1
            if self.wave<=self.level.get_waves_number():
                self.generate_enemies(self.level.make_wave(self.wave))   
            else:
                self.complete=True


    def handle_events(self, events):
        for event in events:

            if event.type == pygame.QUIT:
                self.running = False


    
            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.pause:
                    if windo.main_menu_button.holding:
                        self.state.menu_state()

                    if windo.resume_button.holding:
                        self.pause=False


                if self.tutorial:
                    if windo.ok_button.holding:
                        self.tutorial=False
                        pygame.time.delay(200)


                if self.lose:
                    if windo.retry.holding:
                        retry_lvl=self.level.retry_level()
                        self.state.level_state(retry_lvl)
                        
                    if windo.main_menu_button.holding:
                        self.state.menu_state()


                
                if self.complete:
                    self.level.unluck_level(int(self.level.get_number())+1)
                    if windo.main_menu_button.holding:
                        self.state.menu_state()

                    if windo.next_level.holding:
                        if self.level.next_level():
                            next_level=self.level.next_level()
                            self.state.level_state(next_level)
                        
            
            
        if self.complete or self.reward_screen or self.pause or self.tutorial or self.lose:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)



    def handle_complete(self,screen):
        if self.level.next_level():
            windo.reward_window()
            windo.draw(screen)
            windo.draw_frames(screen) 
        else:
            windo.finish_levels_window()
            windo.draw(screen)
            windo.draw_frames(screen) 

    def handle_reward(self,screen):
        windo.reward_window()
        windo.draw_frames(screen)

    def handle_pause(self,screen):
                    windo.puse_window()
                    windo.draw(screen)
                    windo.draw_frames(screen)

    def handle_tutorial(self,screen):
        windo.tutorial_window(self.tutorial_image_path)
        windo.draw(screen)
        windo.draw_frames(screen)

    def handle_lose(self,screen):
      
            windo.lose_window()
            windo.draw(screen)
            windo.draw_frames(screen)
