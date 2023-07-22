import random,objects

width,height=(1100,660)


class Generate_enemies:
    enemy_list=[]
    def __init__(self,target):
            self.target=target



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
            
            enemy=objects.Enemy(x,y,80,25,vel,mdir,3,0,'blue',50,'fighter',80,self.target)
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
            
            enemy=objects.Enemy(x,y,80,25,vel,mdir,6,1,'darkgreen',200,'strike',100,self.target)
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
            
            enemy=objects.Enemy(x,y,110,25,vel,mdir,10,0,'brown',120,'bomber',130,self.target)
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
            
            enemy=objects.Enemy(x,y,40,20,vel,mdir,0,0,'white',400,'kamikaze',30,self.target)
            self.enemy_list.append(enemy)


        
    def all_time_enemies(self,num_of_enemies):
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

        
            
            while len(self.enemy_list)<num_of_enemies:
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

            return self.enemy_list

            

    def get_enemies(self):
        return self.enemy_list