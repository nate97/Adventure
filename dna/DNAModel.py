from adventurebase.AdventureGlobals import *


class DNAModel():
 
    def __init__(self):
        self.type = ''
        self.name = ''
        self.model = ''
        self.pos = (0,0,0)
        self.hpr = (0,0,0)
        self.scale = (1,1,1)
        self.colorIndex = (1,1,1,1)
        
        
    def setType(self, type):
        self.type = type
        
    def setName(self, name):
        self.name = name
        
        
    def setModel(self, model):   
        self.model = model
        
        
    def setPos(self, pos):
        self.pos = pos
        
        
    def setHpr(self, hpr):
        self.hpr = hpr
        
        
    def setScale(self, scale):
        self.scale = scale
        
        
    def setColor(self, colorIndex):
        self.colorIndex = colorIndex

        
    def createNode(self):
        self.node = loader.loadModel(self.model)
        self.node.reparentTo(render)
        self.node.setPosHprScale(self.pos, self.hpr, self.scale)
        self.node.setColor(self.colorIndex)
        
        
    def destroy(self):
        self.node.removeNode()

