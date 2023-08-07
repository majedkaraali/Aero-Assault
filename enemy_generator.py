import random,objects
import loader

width,height=(1100,660)


class Generate_enemies:
    
    def __init__(self,target):
            self.target=target
            self.enemy_list=[]
            
    def respawn_fighter(self,move_dircton,y):
            x=self.random_distance(move_dircton)
            vel=3
            sprites=loader.random_fighter()
            enemy=objects.Enemy(x,y,vel,move_dircton,3,0,50,'fighter',80,self.target,sprites)
            self.enemy_list.append(enemy)
            
        
    def respawn_strike(self,move_dircton,y):
            x=self.random_distance(move_dircton)   
            sprites=loader.random_strike()
            vel=2
            enemy=objects.Enemy(x,y,vel,move_dircton,6,1,400,'strike',100,self.target,sprites)
            self.enemy_list.append(enemy)

    def respawn_bomber(self,move_dircton,y):
            vel=2
            x=self.random_distance(move_dircton)
            sprites=loader.random_bomber()
            enemy=objects.Enemy(x,y,vel,move_dircton,10,0,120,'bomber',130,self.target,sprites)
            self.enemy_list.append(enemy)


    def respawn_drone(self,move_dircton,y):
            vel=3
            x=self.random_distance(move_dircton)
            sprites=loader.random_drone()
            enemy=objects.Enemy(x,y,vel,move_dircton,0,0,400,'kamikaze',30,self.target,sprites)
            self.enemy_list.append(enemy)


    def random_type():
            respawn_chance = random.random()
            if respawn_chance <= 0.3:  
                return 'strike_aircraft'
            elif respawn_chance <= 0.5:  
                return 'fighter_aircraft'
            elif respawn_chance <= 0.8:  
                return 'bomber'
            elif respawn_chance <= 1.0:  
                return 'kamikaze_drone'
            else:
                return None  
            
    def random_distance(direction):
        if direction=='right':  
            x_spawns=[-700,-650,-600,-550,-500,-450,-400,-350,-300,-250,-200]
        else:
            x_spawns=[width+700,width+650,width+600,width+550,width+500,width+450,width+400,width+350,width+300,width+250,width+200]
        
        x=random.choice(x_spawns)+40
        return x
        

    def random_height():
        y_spawns=[5,33,60,90,120,150,180,210,240,270,300,330,370,400,430,470,500]
        y=random.choice(y_spawns)
        return y
    
    def random_direction():
         move_dircton=random.choice(['right','left'])
         return move_dircton
        

    def all_time_enemies(self,num_of_enemies):
            while len(self.enemy_list)<num_of_enemies:
                enemy_type = self.random_type()
                move_dircton=self.random_direction()
                height=self.random_height()

                if enemy_type=='fighter_aircraft':
                    self.respawn_fighter(move_dircton,height)
                
                elif enemy_type=='strike_aircraft':
                    self.respawn_strike(move_dircton,height)
        

                elif enemy_type=="bomber":
                    self.respawn_bomber(move_dircton,height)
                
                
                elif enemy_type=="kamikaze_drone":
                    self.respawn_drone(move_dircton,height)

            return self.enemy_list

            
    def respawn_wave(self,wave):
    
       
        for _ in range(wave[0]):
            self.respawn_fighter(self.random_direction(),self.random_height())
            
        for _ in range(wave[1]):
            self.respawn_strike(self.random_direction(),self.random_height())
 
        for _ in range(wave[2]):
            self.respawn_bomber(self.random_direction(),self.random_height())
         
        for _ in range(wave[3]):
            self.respawn_drone(self.random_direction(),self.random_height())
        
      
        return self.enemy_list



    def get_enemies(self):
        return self.enemy_list