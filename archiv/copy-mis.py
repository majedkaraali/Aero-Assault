class Missile:
    width=5
    height=17
    vel_x=2
    vel_y=-3

    def __init__(self,x,y,target):
        self.x=x
        self.y=y
        self.targert=target

    def turn_vel(self): # missile turn vel
        eny=self.targert.y
        y_dis=self.y-eny
        y_dis=abs(y_dis)
        
        rich_target_time=y_dis//self.vel_y
        rich_target_time=abs(rich_target_time)

        x_path_dist=self.collidepoint()-self.x


        if rich_target_time and x_path_dist >0:
            missiile_x_turn_vel=x_path_dist/rich_target_time
        else:
            missiile_x_turn_vel=0

        
        pygame.draw.rect(screen, ('red'), (self.collidepoint(), eny, 5, 5))


        return missiile_x_turn_vel
    
    def collidepoint(self):
        enemy_dir=self.targert.move_dir
        eny=self.targert.y
        y_dis=self.y-eny
        y_dis=abs(y_dis)

        rich_target_time=y_dis//self.vel_y
        rich_target_time=abs(rich_target_time)

        if enemy_dir=="left":
            cx=(self.targert.x)-rich_target_time+25
            
        elif enemy_dir=="right":
            cx=(self.targert.x)+rich_target_time-25

        return cx

    
    def move_misile(self):
        if  self.collidepoint()>self.x:
            self.x+=self.turn_vel()+1
        elif self.collidepoint()<self.x:
            self.x-=self.turn_vel()+1
        self.y+=self.vel_y


    def draw_missile(self):
        position=(self.x,self.y)
        m=pygame.Surface((5, 20))
        m.fill('blue')
        i=pygame.transform.rotate(m,180)

        screen.blit(i , position)