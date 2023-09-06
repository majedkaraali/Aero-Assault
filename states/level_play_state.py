import os
import pygame 
from objects import objects
from windows import game_windows
from .Game import GameState
import random 

statics_image=pygame.image.load('src/img/backgrounds/statics.png').convert_alpha()
font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
font_size = 19 
font = pygame.font.Font(font_path, font_size)
button_click=pygame.mixer.Sound("src\\sound\\ui\\btn_click.wav")
        

width,height=(1100,660)


ambince1=pygame.mixer.Sound("src\\sound\\ambience\\torn_AK-47.wav")
ambince2=pygame.mixer.Sound("src\\sound\\ambience\\wind.wav")
ambince3=pygame.mixer.Sound("src\\sound\\ambience\\torn_MGun1.wav")



class Level_Play(GameState):
    def __init__(self,state,level):

        super().__init__()
        
        self.state=state
        self.windo=game_windows()
        self.buttons=self.windo.get_buttons()
        self.allies=False
        self.level=level
        self.base=None
        self.bombs=[]
        self.ground_vhls=[]
        self.enemies_to_remove = []

        self.conform=True

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

        if self.base:
            base_hp =str(self.base.actual_health)
            base_hp_text = font.render("Base Health: "+base_hp, True, ('black'))
            base_hp_text_pos=(200,height-25)
            screen.blit(base_hp_text,base_hp_text_pos) 

        if self.allies:
            ally_cont =str(len(self.allies_list))
            ally_cont_text = font.render("Allies cont: "+ally_cont, True, ('black'))
            ally_cont_text_pos=(200,height-25)
            screen.blit(ally_cont_text,ally_cont_text_pos) 


    def update_game(self, screen):
        if self.can_play() and not self.conform:
            self.handle_sound()
            self.handle_allies(screen)
            
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



        elif self.conform:
            if not self.tutorial:
                self.handle_conform(screen)



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
                    
    def generate_enemies(self,wave):
        self.enemy_list=self.enemies.respawn_wave(wave)

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

                if self.conform:
        
                    if self.windo.ok_button.holding:
                        button_click.play()
                        self.conform=False
                        self.play_conformed=True
                        self.player.last_shot_time=pygame.time.get_ticks()
                        ambince=random.choice([ambince1,ambince2,ambince3])
                        ambince.play()
               

                if self.pause:
                    if self.windo.main_menu_button.holding:
                        button_click.play()
                        self.music.fadeout(100)

                        self.state.menu_state()

                    if self.windo.resume_button.holding:
                        button_click.play()
                        self.player.last_shot_time=pygame.time.get_ticks()
                        self.pause=False
                    if self.windo.options_button.holding:
                        self.windo.options_button_click=True
                        self.windo.options_button.holding=False
                           
                                
                                
                    if self.windo.back.holding:
                        self.windo.options_button_click=False
                        self.windo.back.holding=False

                    if self.windo.music_btn.holding:
            
                        self.windo.music_btn.holding=False
                        if self.play_music_on:
                            self.windo.music_turn_on=False
                            self.play_music_on=False
                            self.music.fadeout(100)

                        elif not self.play_music_on:
                            self.windo.music_turn_on=True
                            self.play_music_on=True
                            self.music.play(-1)

                    if self.windo.sound_btn.holding:
                        self.windo.sound_btn.holding=False
                        if self.play_fx_on:
                            self.windo.sound_turn_on=False
                            self.play_fx_on=False

                        elif not self.play_fx_on:
                            self.windo.sound_turn_on=True
                            self.play_fx_on=True

                if self.tutorial:
                    if self.windo.ok_button.holding:
                        button_click.play()
                        self.tutorial=False
                        self.player.last_shot_time=pygame.time.get_ticks()


                if self.lose:

                    if self.windo.retry.holding:
                        self.music.fadeout(100)

                        button_click.play()
                        retry_lvl=self.level.retry_level()
                        self.state.level_state(retry_lvl)
                        
                    if self.windo.main_menu_button.holding:
                        self.music.fadeout(100)

                        button_click.play()
                        self.state.menu_state()


                
                if self.complete:
                    self.level.unluck_level(int(self.level.get_number())+1)
                    if self.windo.main_menu_button.holding:
                        self.music.fadeout(100)

                        button_click.play()
                        self.state.menu_state()

                    if self.windo.next_level.holding:
                        button_click.play()
                        if self.level.next_level():
                            self.music.fadeout(100)

                            next_level=self.level.next_level()
                            self.state.level_state(next_level)
                            
                        
            
            
        if self.complete or self.reward_screen or self.pause or self.tutorial or self.lose or self.conform:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)



    def handle_complete(self,screen):
        self.player.fade_out_sound()
        if self.level.next_level():
            self.windo.reward_window()
            self.windo.draw(screen)
            self.windo.draw_frames(screen) 
        else:
            self.windo.finish_levels_window()
            self.windo.draw(screen)
            self.windo.draw_frames(screen) 

    def handle_reward(self,screen):
        self.player.fade_out_sound()
        self.windo.reward_window()
        self.windo.draw_frames(screen)

    def handle_pause(self,screen):
                    self.windo.puse_window()
                    self.windo.draw(screen)
                    self.windo.draw_frames(screen)

    def handle_tutorial(self,screen):
        self.windo.tutorial_window(self.tutorial_image_path)
        self.windo.draw(screen)
        self.windo.draw_frames(screen)

    def handle_lose(self,screen):
            self.player.fade_out_sound()
            self.windo.level_lose_window()
            self.windo.draw(screen)
            self.windo.draw_frames(screen)

    def handle_conform(self,screen):

        self.windo.in_game_level_description_frame(self.level)
        self.windo.draw(screen)
        self.windo.draw_frames(screen)