def render_text(text):
        words = text.split()
        # lines = []
        # current_line = ""
        # line_spacing = 5 

        for word in words:
              print(word)
        #     test_line = current_line + " " + word if current_line else word
        #   #  test_size = self.font.size(test_line)
        #     if test_size[0] <= self.width:
        #         current_line = test_line
        #     else:
        #         lines.append(current_line)
        #         current_line = word
        # lines.append(current_line)

        # rendered_lines = [self.font.render(line, True, (255, 255, 255)) for line in lines]
        # text_height = sum(line.get_height() for line in rendered_lines) + (line_spacing * (len(rendered_lines) - 1))
        # y_offset = (self.height - text_height) // 2

        # text_rects = []
        # current_y = self.y + y_offset
        # for line in rendered_lines:
        #     text_rects.append(line.get_rect(topleft=(self.x+50, current_y)))
        #     current_y += line.get_height() + line_spacing

        # return rendered_lines, text_rects


        
render_text("""j7 pro ekran
araması için
İkinci El ve Sıfır Alışveriş
kategorisinde
22
sonuç bulundu""")