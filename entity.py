import pymem
class Entity:
    def __init__(self, contptr, pawnptr, bones, pos, name, teamID):
        self.name = name
        self.pos = [0,0,0]
        self.health = 0
        self.pawnptr = pawnptr
        self.controller_ptr = contptr
        self.bones = bones
        self.pos = pos
        self.team = teamID

    def getInfo(self):
        print(self.name)
        print(self.team)
        print(self.pos)
        print(self.health)
        print(self.bones)
    
    #def read_name(self, )