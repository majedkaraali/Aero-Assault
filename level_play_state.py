from states import GameState
import objects,os
import pygame 
from windows import game_windows
from enemy_generator import Generate_enemies



background=pygame.image.load('src/img/backgrounds/background1.png').convert_alpha()
statics_image=pygame.image.load('src/img/backgrounds/statics.png').convert_alpha()

font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
font_size = 19 
font = pygame.font.Font(font_path, font_size)

def _player():
        global player
        player=objects.Player(400,height-107,[],[],'Unnamed',[])
        return player

width,height=(1100,660)

enemies=Generate_enemies(_player())
windo=game_windows()

class Level_Play(GameState):

    mouse_button_pressed=False
    paues=False
    reward_screen=False
    enemy_list=[]
    score=0

    def __init__(self,state,level):
        super().__init__()
        self.running=True
        self.force_reload=False
        self.level=level
        self.wave=0
        self.complete=False
        self.game_over=False
        self.close=False
        self.state=state
        self.buttons=windo.get_buttons()

        
    def handle_events(self, events):
        tab_pressed = False
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

                if self.complete:
                    if windo.main_menu_button.holding:
                        self.state.menu_state()

                    if windo.next_level.holding:
                        print('aa')
                        #self.state.level_state()

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_pressed = False
            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    if  not self.complete and not self.paues:
                        self.paues = True

                    elif self.paues:
                        self.paues=False
                    

              

                keys = pygame.key.get_pressed()
                if keys[pygame.K_TAB] and not tab_pressed:
                    if not player.forced:
                        player.next_lock()
                        tab_pressed = True
                        
                if keys[pygame.K_r]:
                    player.reload_start_time=pygame.time.get_ticks()
                    player.droped_ammo+=player.magazine
                    player.magazine=0

 
            elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        tab_pressed = False


        if self.mouse_button_pressed:
            if not player.forced:
                if not self.paues:
                    player.shoot()


    
    
    def generate_enemies(self,wave):
        self.enemy_list=enemies.respawn_wave(wave)
           

    def get_enemies(self):
        return self.enemy_list
        


 

    def statics(self,screen):
        statics_rect=statics_image.get_rect()
        statics_rect.topleft=(0,630)
        screen.blit(statics_image,statics_rect)


        if player.reloading:
            magazine='---'
        else:
            magazine=str(player.magazine)
        bullets=str(player.ammo)

        if player.reloading_pods:
            missiles='--'
        else:
            missiles=player.ready_to_fire_missiles

        storage=player.missiles_storage
        bullets_text = font.render(f"bullets: {magazine}/{bullets}", True, 'black')
        bullets_text_pos=(width-375,height-25)
        missiles_text = font.render(f"missiles: {missiles}/{storage}", True, 'black')
        missiles_text_pos=(width-550,height-25)
        heath_value=player.health
        heatl_text = font.render(f"health: {str(heath_value)}", True, 'black')
        heatl_text_pos=(width-170,height-25)
      
        screen.blit(bullets_text, bullets_text_pos)
        screen.blit(missiles_text, missiles_text_pos)
        screen.blit(heatl_text, heatl_text_pos)




    def draw(self,screen):
        screen.blit(background,background.get_rect())
        if not (self.paues) :
            if not self.game_over:
                if not self.complete:
                    self.statics(screen)

                    #HANDLE PLAYER
                    if not player.forced:
                        
                        player.move_player()
                        if len(self.enemy_list)==0:
                            self.wave+=1
                            if self.wave<=self.level.get_waves_number():
                    
                                self.generate_enemies(self.level.make_wave(self.wave))
                                
                            else:
                                self.complete=True


                    player.update_bullets(screen)
                    player.update_player(screen)
                    player.move_bullets() 
                    player.move_missiles()
                    player.update_missiles(screen)
                    player.chek_magazine()
                    player.chek_missile_lounchers_pods()
                    player.move_drops(screen,player)
                    player.is_destroyed()   
                    player.get_enemies=self.get_enemies() 
                    
                    
                    
                    #CLEAN BULLETS KEYS
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        if not player.forced:
                            player.shoot()
                    elif keys[pygame.K_f]:
                        if not player.forced:
                            player.fire_missile(player)
                        
                    enemies_to_remove = []
                    bullets_to_remove = []
                    missiles_to_remove=[]



                    # HANDLE ENEMIES
                    for enemy in self.enemy_list:
                        enemy.move_enemy(screen)
                        enemy.update_enemy(screen)
                        if enemy.destroyed:
                            enemies_to_remove.append(enemy)
                        if enemy.check_kill(player.bullets):
                            self.score+=100
                            drop=objects.Item(enemy.get_centerx(),enemy.y,'gift')
                            player.drops.append(drop)
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
                    for bullet in player.bullets:
                        if bullet.out_of_range():
                            bullets_to_remove.append(bullet)
            
                        elif bullet.hitted:
                            self.score+=20
                            bullets_to_remove.append(bullet)



                    # HANDLE MISSILES
                    for missile in  player.missiles:
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
                        player.bullets.remove(bullet)

                    #CLEAN MISSILES
                    for missile in missiles_to_remove:
                        player.missiles.remove(missile)

                    #ATTACK PLAYER
                    for enemy in self.enemy_list:
                        enemy.attack(player)
                        enemy.move_bombs()
                        enemy.draw_bombs(screen)
                        break
                                

                    if player.destroyed:
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
  
        
            
            