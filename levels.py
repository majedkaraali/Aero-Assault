class Level:

    levels_cont=0
    def __init__(self):
        Level.levels_cont+=1
       # self.icon=pygame.
        self.descreption=""
        self.number=0
    

    def get_number(self):
        return str(self.number)



class Level_1(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 1"
        self.number=1
        self.locked=False

class Level_2(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 2"
        self.number=2
        self.locked=False

class Level_3(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=3
        self.locked=False

class Level_4(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=4
        self.locked=False

class Level_5(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=5
        self.locked=False

class Level_6(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=6
        self.locked=False

class Level_7(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=7
        self.locked=False

class Level_8(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=8
        self.locked=False

class Level_9(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=9
        self.locked=False

class Level_10(Level):
    def __init__(self):
        super().__init__()
        self.name="Level 3"
        self.number=10
        self.locked=False

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

levels.append(a)
levels.append(b)
levels.append(c)
levels.extend([d,e,f,g,h,i,j])
 
def get_levels():
    print(levels)
    return levels