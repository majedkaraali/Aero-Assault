import json


completed_levels = []
try:
    with open('data.json', 'r') as progress_file:
        data = json.load(progress_file)
except (FileNotFoundError, json.JSONDecodeError):
    pass

completed_levels=data['completed_levels']



class Level:

    levels_cont=0
    def __init__(self):
        Level.levels_cont+=1
        self.description="Level Play"
        self.number=0
        self.allies=False
        self.waves=[]
        self.background_path='src\\img\\maps\\LunarVein.png' # default path
        self.tutorial=False
        self.tutorial_image=''
        self.player_loadout=(1680,240,12,4) # default
        self.base=False
    
    def chek_lock(self,number):
        if number not in completed_levels:
            self.locked=True
        else:
            self.locked=False

    def get_number(self):
        return str(self.number)
    
    def get_description(self):
        return self.description
    
    def get_waves_number(self):
        return len(self.waves)
    
    def next_level(self):
      
        if self.number+1 <= len(levels):
            return levels[self.number] 
        else :
     
            return False
        
    def retry_level(self):
        return levels[self.number-1]
    
    def unluck_level(self,level_number):
        completed_level_number = level_number
        if completed_level_number not in completed_levels and completed_level_number<=len(levels):
            completed_levels.append(completed_level_number)
            with open('data.json', 'w') as progress_file:
                json.dump(data, progress_file,indent=completed_level_number)


    def make_wave(self,wave_number):
        wave=self.waves[wave_number-1]
        return wave
    
    def get_waves_number(self):
        return len(self.waves)

class Level_1(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 1"
        self.description=f"{self.name}: {'Learn controls.'}"
        self.number=1
        self.chek_lock(self.number)
        self.background_path='src\\img\\maps\\LunarVein.png'
        self.waves=[]
        self.wave_1=[2,0,0,0]
        self.wave_2=[2,0,0,0]
        self.waves.extend([self.wave_1,self.wave_2])
        self.tutorial=True
        self.tutorial_image='src\\img\\tutorials\\tuturial1.png'
        self.player_loadout=(480,240,0,0)


    


class Level_2(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 2"
        self.description=f"{self.name}: {'Learn How to lead targets'}"
        self.number=2
        self.chek_lock(self.number)
        self.background_path = 'src\\img\\maps\\MidnightMirage.png'
  


        self.wave_1=[2,0,0,0]
        self.wave_2=[1,0,1,0]
        self.wave_3=[4,0,1,0]

        self.waves.extend([self.wave_1,self.wave_2,self.wave_3])
        self.tutorial=True
        self.tutorial_image='src\\img\\tutorials\\tuturial2.png'
    

class Level_3(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.description=f"{self.name}: {'Learn How to Launch Missiles'}"
        self.number=3
        self.background_path='src\\img\\maps\\Shadowfire.png'
        self.chek_lock(self.number)
        self,
        self.wave_1=[4,0,0,0]
        self.wave_2=[2,0,2,0]
        self.wave_2=[4,0,2,0]
        self.waves.extend([self.wave_1,self.wave_2])
        self.tutorial=True
        self.tutorial_image='src\\img\\tutorials\\tuturial3.png'
    

class Level_4(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 4"
        self.description=f"{self.name}: {'Learn How to avoid  guided bombs'}"
        self.number=4
        self.background_path='src\\img\\maps\\CrimsonCitadel.png'
        self.wave_1=[0,1,0,0]
        self.wave_2=[2,1,0,0]

        self.waves.extend([self.wave_1,self.wave_2])
        self.chek_lock(self.number)
        self.tutorial=True
        self.tutorial_image='src\\img\\tutorials\\tuturial4.png'
    
class Level_5(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 5"
        self.number=5
        self.background_path='src\\img\\maps\\CelestialRuins.png'
        self.description=f"{self.name}: {'Attack and defeat all incoming enemy waves , Defend the base from enemy bombs.'}"
        self.wave_1=[3,0,2,0]
        self.wave_2=[3,0,0,2]
        self.wave_3=[4,0,2,0]
        self.wave_4=[0,1,2,0]
        self.waves.extend([self.wave_1,self.wave_2,self.wave_3,self.wave_4])
        self.chek_lock(self.number)
        self.base=True
        self.base_loc=(400,568)      
        self.base_hp=800
    

class Level_6(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 6"
        self.number=6
        self.chek_lock(self.number)
        self.description=f"{self.name}: {'Protect  allies from enemy bombs until they get in safe zone.'}"
        self.background_path='src\\img\\maps\Crossroads.png'
        self.waves=[]
        self.wave_1=[2,0,0,0]
        self.wave_2=[2,0,1,2]
        self.wave_2=[2,2,0,0]
        self.wave_2=[0,1,3,1]
        self.wave_2=[4,1,1,0]

        self.waves.extend([self.wave_1,self.wave_2])
        self.allies=True
        self.allies_count=3
    

class Level_7(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 7"
        self.number=7
        self.chek_lock(self.number)
        self.description=f"{self.name}: {'Attack and defeat all incoming enemy waves.'}"
        self.background_path='src\\img\\maps\\Azure.png'
        
        self.waves=[]
        self.wave_1=[2,0,0,0]
        self.wave_2=[2,0,2,0]
        self.wave_3=[0,1,1,0]
        self.wave_4=[2,1,2,0]
        self.wave_5=[4,0,0,0]
        self.wave_6=[0,0,0,4]
        self.wave_7=[2,2,0,2]
        self.wave_8=[0,2,3,0]
        self.wave_9=[0,0,5,0]
        self.wave_10=[6,0,0,0]
        self.waves.extend([self.wave_1,self.wave_2,self.wave_3,self.wave_4,self.wave_5,self.wave_6,self.wave_7,self.wave_8,self.wave_9,self.wave_10])

    

class Level_8(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 8"
        self.number=8
        self.chek_lock(self.number)
        self.description=f"{self.name}: {'Protect  allies from enemy bombs until they get in safe zone.'}"
        self.background_path='src\\img\\maps\\Crossroads.png'
        self.waves=[]
        self.wave_1=[4,0,0,0]
        self.wave_2=[5,2,0,0]
        self.wave_3=[2,2,2,2]
        self.wave_4=[2,0,4,0]
        self.waves.extend([self.wave_1,self.wave_2,self.wave_3,self.wave_4])    
        self.allies=True
        self.allies_count=4

class Level_9(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 9"
        self.number=9
        self.description=f"{self.name}: {'Attack and defeat all incoming enemy waves.'}"
        self.chek_lock(self.number)
        self.background_path='src\\img\\maps\\NovaExpanse.png'
        self.waves=[]
        self.wave_1=[2,0,0,0]
        self.wave_2=[2,0,0,0]
        self.waves.extend([self.wave_1,self.wave_2])    

class Level_10(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 10"
        self.number=10
        self.description=f"{self.name}: {'Attack and defeat all incoming enemy waves , Defend the base from enemy bombs.'}"
        self.chek_lock(self.number)
        self.background_path='src\\img\\maps\\CelestialRuins.png'
        self.waves=[]
        self.wave_1=[3,0,0,0]
        self.wave_2=[0,0,0,0]
        self.waves.extend([self.wave_1,self.wave_2])
        self.base=True
        self.base_loc=(650,568)      
        self.base_hp=300
        

levels=[]
a=Level_1()
b=Level_2()
c=Level_3()
d=Level_4()
e=Level_5()
f=Level_6()
g=Level_7()
h=Level_8()
i=Level_9()
j=Level_10()
# k=Level_3()
# l=Level_3()
# m=Level_3()
# n=Level_3()
# o=Level_3()


levels.extend([a,b,c,d,e,f,g,h,i,j])
 
def get_levels():
    print(levels)
    return levels

