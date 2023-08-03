import pygame
import os

font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
font_size = 22 
font = pygame.font.Font(font_path, font_size)

class Button():
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.image = pygame.image.load('src/img/GUI/button1.png').convert_alpha()
        self.holding=False

    def scale(self, w, h):
        self.image = pygame.transform.scale(self.image, (w, h))

    def get_rect(self):
        rect = self.image.get_rect()
        rect.center = (self.x, self.y)
        return rect

    def render_text(self,holding):
        if holding:
            button_text = font.render(self.text, True, (255, 255, 255))
        else:
            button_text = font.render(self.text, True, (0, 0, 0))

        button_text_rect = button_text.get_rect()
        button_text_rect.center = self.get_rect().center
        return button_text, button_text_rect  

    def place(self, screen):
        self.chek_hold()
        button_text, button_text_rect = self.render_text(self.holding)
        screen.blit(self.image, self.get_rect())
        screen.blit(button_text, button_text_rect)

    def get_width(self):
        return self.image.get_width()
    

    def chek_hold(self):
        mouse=pygame.mouse.get_pos()
        if self.get_rect().collidepoint(mouse):
            self.holding=True
        else:
            self.holding=False

    
   

