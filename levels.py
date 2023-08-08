class Level:

    levels_cont=0
    def __init__(self):
        Level.levels_cont+=1
        self.description="Level Play"
        self.number=0
        self.waves=[]
    

    def get_number(self):
        return str(self.number)
    
    def get_description(self):
        return self.description
    
    def get_waves_number(self):
        return len(self.waves)



class Level_1(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 1"
        self.description='Level 1'
        self.number=1
        self.locked=False
        self.waves=[]
        self.wave_1=[1,0,0,0]
        self.wave_2=[0,0,1,0]
        self.waves.extend([self.wave_1,self.wave_2])

    def make_wave(self,wave_number):
        wave=self.waves[wave_number-1]
        return wave
    
    def get_waves_number(self):
        return len(self.waves)
    


class Level_2(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 2"
        self.description='Level 2'
        self.number=2
        self.locked=True

class Level_3(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=3
        self.locked=True

class Level_4(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=4
        self.locked=True
    
class Level_5(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=5
        self.locked=True

class Level_6(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=6
        self.locked=True

class Level_7(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=7
        self.locked=True

class Level_8(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=8
        self.locked=True

class Level_9(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=9
        self.locked=True

class Level_10(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=10
        self.locked=True

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