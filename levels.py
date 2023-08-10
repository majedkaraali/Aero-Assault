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
        self.waves=[]
        self.background_path='src\\img\\backgrounds\\background1.png' # defult path
    
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
        if self.number+1-1 <= len(levels):
            return levels[self.number+1-1] #   +1 we need the next level, and -1 cuz lists starts from 0    :D
        else :
            return False
    
    def unluck_level(self,level_number):
        completed_level_number = level_number
        if completed_level_number not in completed_levels:
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
        self.description='Level 1'
        self.number=1
        self.chek_lock(self.number)
        self.background_path='src\\img\\backgrounds\\background1.png'
        self.waves=[]
        self.wave_1=[3,0,0,0]
        self.wave_2=[0,0,2,0]
        self.waves.extend([self.wave_1,self.wave_2])


    


class Level_2(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 2"
        self.description='Level 2'
        self.number=2
        self.chek_lock(self.number)
        self.background_path = 'src\\img\\backgrounds\\background2.png'
        #print(str(self.background_path))


        self.wave_1=[0,1,0,0]
        self.wave_2=[1,0,0,0]

        self.waves.extend([self.wave_1,self.wave_2])
    

class Level_3(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=3
        self.chek_lock(self.number)
    

class Level_4(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=4
        self.chek_lock(self.number)
    
    
class Level_5(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=5
        self.chek_lock(self.number)
    

class Level_6(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=6
        self.chek_lock(self.number)
    

class Level_7(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=7
        self.chek_lock(self.number)
    

class Level_8(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=8
        self.chek_lock(self.number)
    

class Level_9(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=9
        self.chek_lock(self.number)
    

class Level_10(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=10
        self.chek_lock(self.number)
        

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