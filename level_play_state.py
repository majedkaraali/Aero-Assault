from states import GameState
import objects,os
import pygame 
import math 
from math import atan2 ,pi,degrees
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


class Level_Play(GameState):
    
 
    

    def __init__(self,state,level):
        
      #  super().__init__()
        self.score=0
       # print("GG")
        self.running=True
        self.force_reload=False
        self.level=level
        self.wave=0
        self.complete=False
        self.game_over=False
        self.close=False
        self.state=state
        self.buttons=windo.get_buttons()
        self.mouse_button_pressed=False
        self.paues=False
        self.reward_screen=False
        self.allies=False
        self.enemy_list=[]
        self.bombs=[]
        self.base=None
        self.ground_vhls=[]
        self.background_path=level.background_path
        self.background=pygame.image.load(self.background_path).convert_alpha()
        self.player=objects.Player(540,height-107,'Unnamed')
        print(level.player_loadout)
        self.player.loadout(level.player_loadout)
        self.enemies=Generate_enemies(self.player)
        pygame.mouse.set_visible(False)
        self.tutorial=False


        if level.tutorial:
            self.tutorial_image_path=level.tutorial_image
            self.tutorial=True


        self.ground_vhls.append(self.player)

        if level.allies:
            self.allies=[]
            ally_start_point=-400
            for ally in range(level.allies_count):
                ally=objects.Ally(ally_start_point,height-95,88,46)
                self.allies.append(ally)
                ally_start_point-=100
            self.ground_vhls.extend(self.allies)


        if level.base:
            self.base=objects.Base(level.base_loc[0],level.base_loc[1],level.base_hp)
            self.ground_vhls.append(self.base)


            


        
        
    def handle_events(self, events):
        tab_pressed = False
        if self.allies:
            for ally in self.allies:
                ally.move()
                ally.status(self.bombs)

        for event in events:

            if event.type == pygame.QUIT:
                self.running = False
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_pressed=True

                if self.paues:
                    if windo.main_menu_button.holding:
                        self.state.menu_state()

                    if windo.resume_button.holding:
                        self.paues=False
                
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
                        

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_pressed = False
            

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    if  not self.complete and not self.paues:
                        self.paues = True

                    elif self.paues:
                        self.paues=False
                    

                
                if event.key == pygame.K_TAB and not tab_pressed:
                    if not self.player.forced:
                        self.player.next_lock()
                        tab_pressed = True
                        
                if event.key == pygame.K_r:
                    self.player.reload_start_time=pygame.time.get_ticks()
                    self.player.droped_ammo+=self.player.magazine
                    self.player.magazine=0

 
            elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        tab_pressed = False

        if self.mouse_button_pressed:
            if not self.player.forced:
                if not self.paues:
                    if not self.tutorial:
                        self.player.shoot()

        if self.complete or self.reward_screen or self.paues or self.tutorial:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

        


    
    
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

        if not self.tutorial:
            if not (self.paues) :
                if not self.game_over:
                    if not self.complete:
                        

                        #HANDLE self.PLAYER
                        if not self.player.forced:
                            
                            self.player.move_player()
                            if len(self.enemy_list)==0:
                                
                                self.wave+=1
                                if self.wave<=self.level.get_waves_number():
                        
                                    self.generate_enemies(self.level.make_wave(self.wave))
                                    
                                else:
                                    self.complete=True
                                    
                
                        if self.allies:
                            for ally in self.allies:
                                ally.draw(screen)
                                if ally.destroyed:
                                    self.allies.remove(ally)
                        if self.base:
                            self.base.draw(screen)

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


                        
                        
                        
                        #CLEAN BULLETS KEYS
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_SPACE]:
                            if not self.player.forced:
                                self.player.shoot()
                        elif keys[pygame.K_f]:
                            if not self.player.forced:
                                self.player.fire_missile(self.player)
                            
                        enemies_to_remove = []
                        bullets_to_remove = []
                        missiles_to_remove=[]



                        # HANDLE ENEMIES
                        for enemy in self.enemy_list:
                            enemy.move_enemy(screen)
                            enemy.update_enemy(screen)
                            if enemy.destroyed:
                                enemies_to_remove.append(enemy)
                            if enemy.check_kill(self.player.bullets):
                                self.score+=100
                                drop=objects.Item(enemy.get_centerx(),enemy.y,'gift')
                                self.player.drops.append(drop)
                                enemies_to_remove.append(enemy)

                            if enemy.move_dir=='left':
                                if (enemy.x)<5:
                                    enemy.move_dir='right'
                                    enemy.recharge()
                            elif enemy.move_dir=='right':
                                if (enemy.x)>width-5-enemy.get_width():
                                    enemy.move_dir='left'
                                    enemy.recharge()

                            if enemy.y>580:
                                enemy.destroyed=True
                                enemies_to_remove.append(enemy)




                    
                        # HANDLE BULLETS
                        for bullet in self.player.bullets:
                            if bullet.out_of_range():
                                bullets_to_remove.append(bullet)
                
                            elif bullet.hitted:
                                self.score+=20
                                bullets_to_remove.append(bullet)



                        # HANDLE MISSILES
                        for missile in  self.player.missiles:
                            if missile.y<=-10:
                                missiles_to_remove.append(missile)
                            elif missile.hit_target():
                                self.score+=200
                                missiles_to_remove.append(missile)
                                enemies_to_remove.append(missile.target)
                                
                        # CLEAN ENEMEIS
                        if len(enemies_to_remove)>0:
                            for enemy in enemies_to_remove:
                                enemy.destroyed=True
                                if enemy in self.enemy_list:
                                    self.enemy_list.remove(enemy)


                        #CLEAN BULLETS
                        for bullet in bullets_to_remove:
                            self.player.bullets.remove(bullet)

                        #CLEAN MISSILES
                        for missile in missiles_to_remove:
                            self.player.missiles.remove(missile)

                        #ATTACK self.PLAYER
                        for enemy in self.enemy_list:
                            # if len(self.allies)>0:
                            #     enemy.attack(self.player,self.allies)
                            # else:
                            #     enemy.attack(self.player)
                            enemy.attack(self.player)
                            for bomb in enemy.bombs:
                                if bomb not in  self.bombs and not bomb.exploded:
                                    self.bombs.append(bomb)
                        

                        for bomb in self.bombs:
                            bomb.move()
                            if bomb.exploded==True:
                                self.bombs.remove(bomb)



                        for bomb in self.bombs:
                            bomb.draw(screen)
                            bomb.is_hit_object(self.ground_vhls)
                            bomb.status(screen)


                       




                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        crosshair_rect.center = (mouse_x, mouse_y)
                        screen.blit(crosshair_image, crosshair_rect)
                                    

                        if self.player.destroyed:
                            self.game_over=True

                    elif self.complete:
                        windo.reward_window()
                        windo.draw(screen)
                        windo.draw_frames(screen)                   


                elif (self.reward_screen):
          
                    windo.reward_window()
                    windo.draw(screen)
                    windo.draw_frames(screen)
    

            elif (self.paues):

                windo.puse_window()
                windo.draw(screen)
                windo.draw_frames(screen)

        elif self.tutorial:
            
            
            windo.tutorial_window(self.tutorial_image_path)
            windo.draw(screen)
            windo.draw_frames(screen)
  
        
            
            