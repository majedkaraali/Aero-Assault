import pygame
import random
from math import atan2, degrees, pi
import math
import objects

pygame.init()

def _player():
        global player
        player=objects.Player(400,height-70,[],[],'player',[])
        player=objects.Player(400,height-70,[],[],player,[])

     

width=1100
height=660

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
score=0
enemy_types=['fighter','strike_aircraft','bomber','kamikaze_drone']

pygame.mixer.init()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

def get_player():
    return free_play_state.get_player()
def get_enemies():

    return free_play_state.get_enemies()



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

    free_play_posit=pygame.Rect(20, 20, 200, 50)
    missions_posit= pygame.Rect(20, 90, 200, 50)
    exit_posit= pygame.Rect(20, 230, 200, 50)

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
                if self.free_play_posit.collidepoint(mouse_pos):
                    current_state=free_play_state
                    _player()
                elif self.missions_posit.collidepoint(mouse_pos):
                    print("Clicked Missions button")
                    
                elif self.exit_posit.collidepoint(mouse_pos):
                    print("Clicked Exit button")
                    


    def draw(self):
        screen.fill('black')
        free_play_button = pygame.draw.rect(screen, (0, 0, 255),self.free_play_posit)
        free_play_text = font.render("Free Play", True, (255, 255, 255))
        free_play_text_rect = free_play_text.get_rect(center=free_play_button.center)
        screen.blit(free_play_text, free_play_text_rect)


        missions_button = pygame.draw.rect(screen, (0, 255, 0),self.missions_posit)
        missions_text = font.render("Missions", True, (255, 255, 255))
        missions_text_rect = missions_text.get_rect(center=missions_button.center)
        screen.blit(missions_text, missions_text_rect)



        exit_button = pygame.draw.rect(screen, (255, 0, 0),self.exit_posit)
        exit_text = font.render("Exit", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, exit_text_rect)
            
       
     

class FreePlayState(GameState):
   
    mouse_button_pressed=False
    paues=False
    reward_screen=False

    pause_frame_color = ('silver')
    rerawrds_frame_color=('silver')
    pause_surface_width=250
    pause_surface_height=150
    frame_position = ((width//2)-(pause_surface_width//2),(height//2)-(pause_surface_height//2))
    frame_surface = pygame.Surface((pause_surface_width,pause_surface_height))
    frame_surface.fill(pause_frame_color)

    border_width = 1
    border_color = (0, 0, 0)


    
    rwd_surface_width = width//2
    rwd_surface_height = height//2
    reward_scr_position =  ((width//2)-(rwd_surface_width//2),(height//2)-(rwd_surface_height//2))
    rewards_surface = pygame.Surface((rwd_surface_width, rwd_surface_height))
    rewards_surface.fill(rerawrds_frame_color)


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




    enemy_list=[]
    

    def __init__(self):
        super().__init__()
        self.running=True
        self.force_reload=False
        self.generate_player()
        
        
    def handle_events(self, events):
        global current_state
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
                    player.shoot()


    def respawn_fighter(self,move_dircton,y):
        if move_dircton==1:
                x_spawns=[-700,-650,-600,-550,-500,-450,-400,-350,-300,-250,-200]
                x=random.choice(x_spawns)-40
                mdir='right'
                vel=2

        else:
            x_spawns=[width+700,width+650,width+600,width+550,width+500,width+450,width+400,width+350,width+300,width+250,width+200]
            x=random.choice(x_spawns)+40
            mdir='left'
            vel=-2
           
        enemy=objects.Enemy(x,y,80,25,vel,mdir,3,0,'blue',50,'fighter',80,player)
        self.enemy_list.append(enemy)

    
    def respawn_strike(self,move_dircton,y):
        if move_dircton==1:
                x_spawns=[-700,-650,-600,-550,-500,-450,-400,-350,-300,-250,-200]
                x=random.choice(x_spawns)-40
                mdir='right'
                vel=2

        else:
            x_spawns=[width+700,width+650,width+600,width+550,width+500,width+450,width+400,width+350,width+300,width+250,width+200]
            x=random.choice(x_spawns)+40
            mdir='left'
            vel=-2
           
        enemy=objects.Enemy(x,y,80,25,vel,mdir,6,1,'darkgreen',200,'strike',100,player)
        self.enemy_list.append(enemy)

    def respawn_bomber(self,move_dircton,y):
        if move_dircton==1:
                x_spawns=[-700,-650,-600,-550,-500,-450,-400,-350,-300,-250,-200]
                x=random.choice(x_spawns)-40
                mdir='right'
                vel=2

        else:
            x_spawns=[width+700,width+650,width+600,width+550,width+500,width+450,width+400,width+350,width+300,width+250,width+200]
            x=random.choice(x_spawns)+40
            mdir='left'
            vel=-2
           
        enemy=objects.Enemy(x,y,110,25,vel,mdir,10,0,'brown',120,'bomber',130,player)
        self.enemy_list.append(enemy)


    def respawn_drone(self,move_dircton,y):
        if move_dircton==1:
                x_spawns=[-700,-650,-600,-550,-500,-450,-400,-350,-300,-250,-200]
                x=random.choice(x_spawns)-40
                mdir='right'
                vel=2

        else:
            x_spawns=[width+700,width+650,width+600,width+550,width+500,width+450,width+400,width+350,width+300,width+250,width+200]
            x=random.choice(x_spawns)+40
            mdir='left'
            vel=-2
           
        enemy=objects.Enemy(x,y,40,20,vel,mdir,0,0,'white',400,'kamikaze',30,player)
        self.enemy_list.append(enemy)


    
    def generate_enemies(self,num_of_enemies):

        def respawn_enemy():
            respawn_chance = random.random()
            if respawn_chance <= 0.4:  
                return 'strike_aircraft'
            elif respawn_chance <= 0.6:  
                return 'fighter_aircraft'
            elif respawn_chance <= 0.8:  
                return 'bomber'
            elif respawn_chance <= 1.0:  
                return 'kamikaze_drone'
            else:
                return None  

    
        
        if len(self.enemy_list)<num_of_enemies:
            respawned_enemy = respawn_enemy()
            move_dircton=random.randint(0,1)
            y_spawns=[5,33,60,90,120,150,180,210,240,270,300,330,370,400,430,470,500]
            y=random.choice(y_spawns)
            
            if respawned_enemy=='fighter_aircraft':
                self.respawn_fighter(move_dircton,y)
            
            elif respawned_enemy=='strike_aircraft':
                self.respawn_strike(move_dircton,y)
     

            elif respawned_enemy=="bomber":
                self.respawn_bomber(move_dircton,y)
               
            
            elif respawned_enemy=="kamikaze_drone":
                self.respawn_drone(move_dircton,y)

           

            

    def get_enemies(self):
        return self.enemy_list
        
    def generate_player(self):
        global player
        
        #player=objects.Player(400,height-70,[],[],'self.player')


    def reward_screen_view(self):
        pygame.draw.rect(self.rewards_surface,self.border_color, self.rewards_surface.get_rect(), self.border_width)
        screen.blit(self.rewards_surface, self.reward_scr_position)
        self.rewards_surface.fill('silver')


        
        main_menu_text = font.render("Main Menu", True, (255, 255, 255))
        main_menu_text_rect=main_menu_text.get_rect(center=self.main_menu_btn_rect.center)

        
        exit_text = font.render("Exit ", True, (255, 255, 255))
        exit_text_rect=exit_text.get_rect(center=self.exit_btn_rect.center)


        scor_text= font.render("Score: 0", True, (255, 255, 255))
        score_pos=((self.rwd_surface_width//2)-scor_text.get_width()//2,80)

        high_score= font.render("High Score: 0", True, (255, 255, 255))
        high_score_pos=((self.rwd_surface_width//2)-high_score.get_width()//2,120)


        died_text= font.render(" YOU HAVE BEEN DESTROYED ! ", True, (255, 255, 255))
        died_text_pos=((self.rwd_surface_width//2)-(died_text.get_width()//2),20)


        self.rewards_surface.blit(main_menu_text,main_menu_text_rect)
        self.rewards_surface.blit(exit_text,exit_text_rect)
        self.rewards_surface.blit(died_text,died_text_pos)
        self.rewards_surface.blit(scor_text,score_pos)
        self.rewards_surface.blit(high_score,high_score_pos)



        
   

    
    def ground(self):
        surface_width = width
        surface_height = 80
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
        startic_surface.fill(pygame.Color('lightgreen'))
        border = 1
        position = (0, height-30)

        pygame.draw.rect(startic_surface, pygame.Color('lightgreen'), startic_surface.get_rect(), border)
        screen.blit(startic_surface, position)
        from objects import score
        score_value =str(score)

        score_text = font.render("Score: "+score_value, True, ('black'))
        score_text_pos=(10,height-25)

        menu_text = font.render("menu", True, 'black')
        menu_text_pos=(width//2,height-25)
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
        bullets_text_pos=(width-250,height-25)

        missiles_text = font.render(f"missiles: {missiles}/{storage}", True, 'black')
        missiles_text_pos=(width-400,height-25)

        heath_value=player.health

        heatl_text = font.render(f"health: {str(heath_value)}", True, 'black')
        heatl_text_pos=(width-100,height-25)
      
        screen.blit(score_text,score_text_pos)
        screen.blit(menu_text, menu_text_pos)
        screen.blit(bullets_text, bullets_text_pos)
        screen.blit(missiles_text, missiles_text_pos)
        screen.blit(heatl_text, heatl_text_pos)


           



    def draw(self):
        
        
        if not (self.paues) :
            if not self.reward_screen:
                
                clock.tick(60)
                screen.fill('aqua')
                self.ground()
                self.statics()
                if not player.forced:
                    player.move_player()
                    self.generate_enemies(3)
                player.update_player()
                player.move_bullets() 
                player.update_bullets()
                player.move_missiles()
                player.update_missiles()
                player.chek_magazine()
                player.chek_missile_lounchers_pods()
                player.move_drops()
                player.is_destroyed()   
                player.get_enemies=self.get_enemies() 
                
                
    
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if not player.forced:
                        player.shoot()
                elif keys[pygame.K_f]:
                    if not player.forced:
                        player.fire_missile()
                    
                enemies_to_remove = []
                bullets_to_remove = []
                missiles_to_remove=[]

                for enemy in self.enemy_list:
                    if enemy.destroyed:
                        enemies_to_remove.append(enemy)
                    if enemy.check_collision(player.bullets):
                        drop=objects.Item(enemy.get_centerx(),enemy.y,'gift')
                        player.drops.append(drop)
                        print(player.drops,'mmmmm')
                        enemies_to_remove.append(enemy)
                    if enemy.move_dir=='left':
                        if (enemy.x)<-300:
                            enemy.destroyed=True
                            enemies_to_remove.append(enemy)
                    
                    elif enemy.move_dir=='right':
                        if (enemy.x)>width+300:
                            enemy.destroyed=True
                            enemies_to_remove.append(enemy)

                    if enemy.y>580:
                        enemy.destroyed=True
                        enemies_to_remove.append(enemy)

            

                for bullet in player.bullets:
                    if bullet.out_of_range():
                        bullets_to_remove.append(bullet)
        
                    elif bullet.hitted:
                        bullets_to_remove.append(bullet)


                for missile in  player.missiles:
                    if missile.y<=-10:
                        missiles_to_remove.append(missile)
                    elif missile.hit_target():
                        missiles_to_remove.append(missile)
                        enemies_to_remove.append(missile.target)
                        

                if len(enemies_to_remove)>0:
                    for enemy in enemies_to_remove:
                        enemy.destroyed=True
                        self.enemy_list.remove(enemy)
                        
                for bullet in bullets_to_remove:
                    player.bullets.remove(bullet)

                for missile in missiles_to_remove:
                    player.missiles.remove(missile)

                loop_once=0
                for enemy in self.enemy_list:
                    if enemy.destroyed==True:
                        enemies_to_remove.append(enemy)

                    enemy.move_enemy()
                    enemy.update_enemy()
                    enemy.attack(player)
                    if loop_once==0:
                        enemy.move_bombs()
                        enemy.draw_bombs()
                        loop_once+=1
                            

                player.update_bullets()

                if player.destroyed:
                    self.reward_screen=True

            elif (self.reward_screen):
                self.reward_screen_view()
               

        elif (self.paues):

            pygame.draw.rect(self.rewards_surface,self.border_color, self.frame_surface.get_rect(), self.border_width)
            screen.blit(self.frame_surface, self.frame_position)


            resume_button = pygame.draw.rect(self.frame_surface, (0, 0, 255),self.resume_button_rect)
            resume_button_text = font.render("Resume", True, (255, 255, 255))
            resume_button_text_rect = resume_button_text.get_rect(center=resume_button.center)
           

            mainmenu_button=pygame.draw.rect(self.frame_surface,(0, 0, 255),self.main_menu_button_rect)
            mainmenu_button_text=font.render("Main menu", True, (255, 255, 255))
            mainmenu_button_text_rect=mainmenu_button_text.get_rect(center=mainmenu_button.center)

            exit_button=pygame.draw.rect(self.frame_surface,(0, 0, 255),self.exit_button_rect)
            exit_button_text=font.render("Exit", True, (255, 255, 255))
            exit_button_text_rect=exit_button_text.get_rect(center=exit_button.center)


            self.frame_surface.blit(resume_button_text,resume_button_text_rect)
            self.frame_surface.blit(mainmenu_button_text,mainmenu_button_text_rect)
            self.frame_surface.blit(exit_button_text,exit_button_text_rect)


    

        
            
           
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



        

    pygame.quit()
if __name__=='__main__':
    main()
