
import pygame
import os

font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
print(font_path)
font_size = 19 
font = pygame.font.Font(font_path, font_size)

background_path= os.path.join("src/fonts", "OCRAEXT.ttf")
        
statics_image=pygame.image.load('src/img/backgrounds/statics.png').convert_alpha()



width,height=(1100,660)
aaa=2
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
        self.wave=0
    
        self.enemy_list=[]
        self.enemies_to_remove = []

        self.background_path='src/'
        


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