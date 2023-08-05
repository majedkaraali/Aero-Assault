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

class Frame:
    def __init__(self, x, y, width, height):  
        self.x = x
        self.y = y
        self.width = width -100
        self.height = height  -60
        self.image = pygame.image.load('src/img/GUI/LabelFrame.png').convert_alpha()
        self.buttons = []
        self.text = "NON"
        self.font = pygame.font.Font(font_path, font_size)

    def write(self, text):
        self.text = text

    def get_rect(self):
        rect = self.image.get_rect()
        rect.topleft = (self.x, self.y)
        return rect

    def render_text(self):
        words = self.text.split()
        lines = []
        current_line = ""
        line_spacing = 5 

        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_size = self.font.size(test_line)
            if test_size[0] <= self.width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        rendered_lines = [self.font.render(line, True, (255, 255, 255)) for line in lines]
        text_height = sum(line.get_height() for line in rendered_lines) + (line_spacing * (len(rendered_lines) - 1))
        y_offset = (self.height - text_height) // 2

        text_rects = []
        current_y = self.y + y_offset
        for line in rendered_lines:
            text_rects.append(line.get_rect(topleft=(self.x+50, current_y)))
            current_y += line.get_height() + line_spacing

        return rendered_lines, text_rects

    def draw(self, screen):

        rendered_lines, text_rects = self.render_text()
        screen.blit(self.image, self.get_rect())

        for line, text_rect in zip(rendered_lines, text_rects):
            screen.blit(line, text_rect)
    def draw_buttons(self,screen):
        for button in self.buttons:
            button.place(screen)

