from adventurebase.AdventureGlobals import *


class DNADummy():
 
    def __init__(self):
        self.type = ''
        self.name = ''
        self.pos = (0,0,0)
        self.hpr = (0,0,0)
        self.scale = (1,1,1)
        
        
    def setType(self, type):
        self.type = type
        
        
    def setName(self, name):
        self.name = name
        
        
    def setPos(self, pos):
        self.pos = pos
        
        
    def setHpr(self, hpr):
        self.hpr = hpr
        
        
    def setScale(self, scale):
        self.scale = scale
        
        
    def createDummy(self):
        self.node = render.attachNewNode(self.name)
        self.node.reparentTo(render)
        self.node.setPosHprScale(self.pos, self.hpr, self.scale)
        
        
    def destroy(self):
        self.node.removeNode()


