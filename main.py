import pygame
import random
from math import atan2, degrees, pi
import math
import objects
from enemy_generator import Generate_enemies

pygame.init()

pygame.mixer.init()

width=1100
height=660
score=0

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
enemy_types=['fighter','strike_aircraft','bomber','kamikaze_drone']
background=pygame.image.load('src/img/background9.png').convert_alpha()
statics=pygame.image.load('src/img/statics.png').convert_alpha()



def _player():
        global player
        player=objects.Player(400,height-107,[],[],'Unnamed',[])
        return player


ens=Generate_enemies(_player())







class GameState:

    def __init__(self):
        self.running = False

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class MenuState(GameState):

    free_play_position=pygame.Rect(20, 20, 200, 50)
    missions_position= pygame.Rect(20, 90, 200, 50)
    exit_position= pygame.Rect(20, 230, 200, 50)

    def __init__(self):
        super().__init__()

        self.running=True

        
    def handle_events(self, events):
        global current_state
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.free_play_position.collidepoint(mouse_pos):
                    current_state=free_play_state
                    _player()
                elif self.missions_position.collidepoint(mouse_pos):
                    print("Clicked Missions button")
                    
                elif self.exit_position.collidepoint(mouse_pos):
                    print("Clicked Exit button")
                    


    def draw(self):
        from screens import main_menu_screen
        main_menu_screen(screen,menu_state)
            
       
     

class FreePlayState(GameState):
   
    mouse_button_pressed=False
    paues=False
    reward_screen=False
    enemy_list=ens.all_time_enemies(3)


    #PAUSE SURFACE
    pause_frame_color = ('silver')
    rerawrds_frame_color=('silver')
    pause_surface_width=250
    pause_surface_height=150
    frame_position = ((width//2)-(pause_surface_width//2),(height//2)-(pause_surface_height//2))
    frame_surface = pygame.Surface((pause_surface_width,pause_surface_height))
    frame_surface.fill(pause_frame_color)
    border_width = 1
    border_color = (0, 0, 0)

    #REWARD SURFACE
    rwd_surface_width = width//2
    rwd_surface_height = height//2
    reward_scr_position =  ((width//2)-(rwd_surface_width//2),(height//2)-(rwd_surface_height//2))
    rewards_surface = pygame.Surface((rwd_surface_width, rwd_surface_height))
    rewards_surface.fill(rerawrds_frame_color)

    # RECTS
    resume_button_rect=pygame.Rect(75, 20, 100, 20)
    main_menu_button_rect=pygame.Rect(75, 60, 100, 20)
    exit_button_rect=pygame.Rect(75, 100, 100, 20)
    score_rect=pygame.Rect(35, height-15, 100, 20)
    menu_rect=pygame.Rect((width//2), height-15, 100, 66)
    missile_count_rect=pygame.Rect(width-50, height-15, 50, 66)
    bullet_count_rect=pygame.Rect(width-150, height-15, 50, 66)
    scorevalue_rect=pygame.Rect(80, height-15, 100, 20)
    main_menu_btn_rect=pygame.Rect((rwd_surface_width//2)-150,rwd_surface_height-70,100,20)
    exit_btn_rect=pygame.Rect((rwd_surface_width//2)+100,rwd_surface_height-70,70,20)

    def __init__(self):
        super().__init__()
        self.running=True
        self.force_reload=False
        

        
        
    def handle_events(self, events):
        global current_state
        screen.blit(background,background.get_rect())
        tab_pressed = False
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_pressed=True
                mouse_pos = pygame.mouse.get_pos()
                adjusted_mouse_pos = (
                    mouse_pos[0] - self.frame_position[0],
                    mouse_pos[1] - self.frame_position[1]
                )

                if self.paues:
                    if self.resume_button_rect.collidepoint(adjusted_mouse_pos):
                        self.paues = False

                    elif self.main_menu_button_rect.collidepoint(adjusted_mouse_pos):
                        current_state = menu_state 
                        self.paues = False
                        self.enemy_list.clear()
                        player.missiles.clear()
                        player.bullets.clear()
                        player.clear()
                

                    elif self.exit_button_rect.collidepoint(adjusted_mouse_pos):
                        self.running = False

                if self.reward_screen:
                    adjusted_mouse_pos = (
                    mouse_pos[0] - self.reward_scr_position[0],
                    mouse_pos[1] - self.reward_scr_position[1]
                    )
                    
                
                    if self.main_menu_btn_rect.collidepoint(adjusted_mouse_pos):
                        current_state = menu_state 
                        self.paues = False
                        self.reward_screen=False
                        for enemy in self.enemy_list:
                            enemy.clear_bombs()
                        self.enemy_list.clear()
                        player.missiles.clear()
                        player.bullets.clear()
                        player.clear()

                    elif self.exit_btn_rect.collidepoint(adjusted_mouse_pos):
                        self.running = False


       
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_pressed = False
            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.paues:
                        self.paues = False
                    else:
                        if not self.reward_screen:
                            self.paues = True
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
                    player.shoot(screen)


    
    
    def generate_enemies(self,num_of_enemies):
        ens.all_time_enemies(num_of_enemies)
           

    def get_enemies(self):
        return self.enemy_list
        

    def reward_screen_view(self):
       from screens import reward_screen_view
       reward_screen_view(screen,free_play_state)


    
    def ground(self):
        surface_width = width
        surface_height = 120
        ground_surface = pygame.Surface((surface_width, surface_height))
        ground_surface.fill(pygame.Color('green'))
        border = 1
        position = (0, height-surface_height)
        pygame.draw.rect(ground_surface, pygame.Color('green'), ground_surface.get_rect(), border)
        screen.blit(ground_surface, position)

    def statics(self):
        global score,pause_menurect
        surface_width = width
        surface_height = 30
        startic_surface = pygame.Surface((surface_width, surface_height))
        
        border = 1
        position = (0, height-30)
        statics_rect=statics.get_rect()
        statics_rect.topleft=(0,630)
        screen.blit(statics,statics_rect)
        pygame.draw.rect(startic_surface, pygame.Color('lightgreen'), startic_surface.get_rect(), border)
     
        score_value =str(score)
        score_text = font.render("Score: "+score_value, True, ('black'))
        score_text_pos=(10,height-23)
        menu_text = font.render("MENU", True, 'black')
        menu_text_pos=(width//2,height-23)
        pause_menurect=menu_text.get_rect()

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
        bullets_text_pos=(width-250,height-23)
        missiles_text = font.render(f"missiles: {missiles}/{storage}", True, 'black')
        missiles_text_pos=(width-400,height-23)
        heath_value=player.health
        heatl_text = font.render(f"health: {str(heath_value)}", True, 'black')
        heatl_text_pos=(width-100,height-23)
      
        screen.blit(score_text,score_text_pos)
        screen.blit(menu_text, menu_text_pos)
        screen.blit(bullets_text, bullets_text_pos)
        screen.blit(missiles_text, missiles_text_pos)
        screen.blit(heatl_text, heatl_text_pos)




    def draw(self):
        global score
        if not (self.paues) :
            if not self.reward_screen:
                clock.tick(60)
                

              #  self.ground()
                self.statics()


                #HANDLE PLAYER
                if not player.forced:
                    
                    player.move_player()
                    if len(self.enemy_list)<3:
                        self.generate_enemies(3)
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
                        score+=100
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
                        score+=20
                        bullets_to_remove.append(bullet)



                # HANDLE MISSILES
                for missile in  player.missiles:
                    if missile.y<=-10:
                        missiles_to_remove.append(missile)
                    elif missile.hit_target():
                        score+=200
                        missiles_to_remove.append(missile)
                        enemies_to_remove.append(missile.target)
                        
                # CLEAN ENEMEIS
                if len(enemies_to_remove)>0:
                    for enemy in enemies_to_remove:
                        enemy.destroyed=True
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
                    self.reward_screen=True


            elif (self.reward_screen):
                self.reward_screen_view()
               

        elif (self.paues):
            from screens import pause_screen
            pause_screen(screen,free_play_state)


    

        
            
           
menu_state = MenuState()
free_play_state = FreePlayState()
current_state = menu_state   

def main():    
    while current_state.running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                current_state.running = False
        
        next_state = current_state.handle_events(events)
        current_state.update()
        current_state.draw()
        pygame.display.flip()
       #dadda print(clock.get_fps())


    pygame.quit()
if __name__=='__main__':
    main()
