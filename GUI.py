import pygame
import os

font_path = os.path.join("src/fonts", "OCRAEXT.ttf")
font_size = 23 




class Button():
    def __init__(self, x, y, text,font_size):
        self.x = x
        self.y = y
        self.text = text
        self.image = pygame.image.load('src/img/GUI/button.png').convert_alpha()
        self.holding_image=pygame.image.load('src/img/GUI/button_holding.png').convert_alpha()
        self.current_image=self.image
        self.holding=False
        self.custum_rect=False
        self.font = pygame.font.Font(font_path, font_size)


    def get_text(self):
        return self.text
    
    def conifig_button(self,image,holding_image,custum_rect):
        self.image=image
        self.holding_image=holding_image
        self.custum_rect=custum_rect

    def change_images(self,image,hold_image):
        self.image=image
        self.holding_image=hold_image
    def change_location(self,x,y):
        self.x=x
        self.y=y
    def scale(self, w, h):
        self.image = pygame.transform.scale(self.image, (w, h))

    def get_rect(self):
        rect = self.image.get_rect()

        if not self.custum_rect: 
            rect.center = (self.x, self.y)
            return rect
        else:
            rect.center=self.custum_rect
            return rect

    def render_text(self,holding):
     
        if holding:
            self.current_image=self.holding_image
            button_text = self.font.render(self.text, True, (255, 255, 255))
        else:
            button_text = self.font.render(self.text, True, (0, 0, 0))
            self.current_image=self.image

        button_text_rect = button_text.get_rect()
        button_text_rect.center = self.get_rect().center
        return button_text, button_text_rect  

    def place(self, screen):
   
        self.chek_hold()
        button_text, button_text_rect = self.render_text(self.holding)

        screen.blit(self.current_image, self.get_rect())
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
        self.text = ""
        self.selected_button=None 
        self.default_lines=[]

       
        self.font = pygame.font.Font(font_path, font_size)
        self.bold_font=pygame.font.Font(font_path, font_size)
        self.bold_font.set_bold(True)

    def write(self, text):
        self.text = text

    def add_line(self,text,x,y,blod:bool,color,center:bool):
        line = {'text': text, 'position_x': x, 'position_y': y,'blod': blod, 'color' : color, 'center':center}
        self.default_lines.append(line)



    def get_rect(self):
      #  print(self.image)
        rect = self.image.get_rect()
        rect.topleft = (self.x, self.y)
    
        return rect
    
    def add_button(self,button):
        self.buttons.append(button)

  

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
    def confing(self,image):
        self.image=image




    def draw(self, screen):
        rendered_lines, text_rects = self.render_text()
        screen.blit(self.image, self.get_rect())

        for line, text_rect in zip(rendered_lines, text_rects):
            screen.blit(line, text_rect)

        for line in self.default_lines:
            if not line['blod']:
                line_txt=self.font.render(line['text'],True,line['color'])
            else:
                line_txt=self.bold_font.render(line['text'],True,line['color'])
            line_rect=line_txt.get_rect()

            if line['center']:
                line_rect.center=(line['position_x'],line['position_y'])
            else:
                line_rect.topleft=(line['position_x'],line['position_y'])
            screen.blit(line_txt,line_rect)

    def draw_buttons(self,screen):
        self.selected_button=None

        for button in self.buttons:
            if button.holding:
                self.selected_button=button


            button.place(screen)

    def get_selected_btn(self):
        return 0

    def get_buttons(self):
        return self.buttons



     
       
            




        

class Levels_Frame:
    def __init__(self, x, y, width, height, rows, cols,levels):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.image = pygame.image.load('src/img/GUI/LabelFrame.png').convert_alpha()
        self.level_image=pygame.image.load('src/img/GUI/level.png').convert_alpha()
        self.locked_image=pygame.image.load('src/img/GUI/level_locked2.png').convert_alpha()
        self.hold_image=pygame.image.load('src/img/GUI/level_hold.png').convert_alpha()
      
        self.levels=[]
        self.image_width = 600 // cols
        self.image_height = 225 // rows
        self.buttons=[]
        self.selected_button=None

        for level in levels:

            self.add_level(level)


        for row in range(self.rows):
           
            for col in range(self.cols):
             
                index = row * self.cols + col
       
                if index < len(self.levels):
                   
                    center_rect=(self.x + col * (self.image_width + 10)+95, self.y + row * (self.image_height + 10)+70)

                    image=self.level_image
                    imag_rect=image.get_rect()
                    imag_rect.center=(center_rect)
                       

                    level_button=Button(0,0,self.levels[index].get_number(),22)
                    level_button.conifig_button(self.level_image,self.hold_image,center_rect)
                    

                    if not self.levels[index].locked:
                        level_button.conifig_button(self.level_image,self.hold_image,center_rect)
                
                       
                    else:
                        level_button=Button(0,0,'',22)
                        level_button.conifig_button(self.locked_image,self.locked_image,center_rect)
                
                    self.buttons.append(level_button)


    def add_level(self, level):
        self.levels.append(level)

    def get_buttons(self):
        return self.buttons

    def get_rect(self,index):
        rect = self.buttons[index].get_rect()
        return rect
    

    def chek_hold(self,rect):
        mouse=pygame.mouse.get_pos()

        if rect.collidepoint(mouse):
            return True
        else:
            return False
        



    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
  
    def get_selected_btn(self):
        return self.selected_button     
                    
    def draw_buttons(self,screen):
        self.selected_button=None

        for button in self.buttons:
            if button.holding:
                self.selected_button=button

            button.place(screen)
            




        

