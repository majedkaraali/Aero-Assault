import objects,os
import pygame 
from windows import game_windows
from EnemyMaker import Generate_enemies


crosshair_image = pygame.image.load("src\img\weapons\crosshair.png")
crosshair_rect = crosshair_image.get_rect()


statics_image=pygame.image.load('src/img/backgrounds/statics.png').convert_alpha()

font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
font_size = 19 
font = pygame.font.Font(font_path, font_size)
#pygame.mouse.set_visible(False)

        



width,height=(1100,660)
windo=game_windows()


class Level_Play():
    
 
    

    def __init__(self,state,level):
        super().__init__()
        self.lose=False
        self.force_reload=False
        self.play_conformed=False
        self.complete=False
        self.game_over=False
        self.close=False
        self.state=state
        self.buttons=windo.get_buttons()
        self.mouse_button_pressed=False
        self.pause=False
        self.reward_screen=False
        self.allies=False
        self.level=level
        self.wave=0
        self.enemy_list=[]
        self.base=None
        self.ground_vhls=[]
        self.enemies_to_remove = []
        self.background_path=level.background_path
        self.background=pygame.image.load(self.background_path).convert_alpha()
        self.player=objects.Player(540,height-107,'Unnamed')
        


        print(level.player_loadout)
        self.player.loadout(level.player_loadout)
        self.enemies=Generate_enemies(self.player)
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos((1000, 500))

        self.tutorial=False


        if level.tutorial:
            self.tutorial_image_path=level.tutorial_image
            self.tutorial=True


        self.ground_vhls.append(self.player)

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



    def draw(self,screen):

        screen.blit(self.background,self.background.get_rect())
        self.statics(screen)
        self.update_game(screen)



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


    def can_play(self):
        return not (self.lose or self.tutorial or self.pause or self.game_over or self.complete )
    

    def handle_player(self,screen):
        if not self.player.forced:
            self.player.move_player()
            self.player.update_bullets(screen)
            self.player.update_player(screen)
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
                self.drops.append(drop)



    def handle_bullets(self,screen):
        pass
    
    def handle_missiles(self):
        pass  

    def handle_drops(self):
        pass
   

    def handle_bombs(self,screen):

        for bomb in self.bombs:
            bomb.move()
            bomb.draw(screen)
            bomb.is_hit_object(self.ground_vhls)
            bomb.status(screen)

            if bomb.exploded==True:
                self.bombs.remove(bomb)




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

        elif keys[pygame.MOUSEBUTTONDOWN]:
            print('shoo')
            if not self.player.forced or self.pause or self.tutorial:
                print('shoot`22')
                self.player.shoot()



        elif keys[pygame.K_ESCAPE]:
            if  not self.complete and not self.pause:
                self.pause = True

            elif self.pause:
                self.pause=False
            






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




                if self.complete:
                    self.level.unluck_level(int(self.level.get_number())+1)
                    if windo.main_menu_button.holding:
                        self.state.menu_state()

                    if windo.next_level.holding:
                        next_level=self.level.next_level()
                        self.state.level_state(next_level)




                if self.lose:
                    if windo.retry.holding:
                        retry_lvl=self.level.retry_level()
                        self.state.level_state(retry_lvl)
                        
                    if windo.main_menu_button.holding:
                        self.state.menu_state()
                        
            
            
        if self.complete or self.reward_screen or self.pause or self.tutorial or self.lose:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)



    def handle_complete(self,screen):
        windo.reward_window()
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
