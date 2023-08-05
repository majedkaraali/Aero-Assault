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
        self.locked=True

levels=[]
a=Level_1()
b=Level_2()
c=Level_3()
d=Level_3()
e=Level_3()
f=Level_3()
g=Level_3()
h=Level_3()
i=Level_3()
j=Level_3()
k=Level_3()
l=Level_3()
m=Level_3()
n=Level_3()
o=Level_3()

levels.append(a)
levels.append(b)
levels.append(c)
levels.extend([d,e,f,g,h,i,j,k,l,m,n,o])
 
def get_levels():
    print(levels)
    return levels