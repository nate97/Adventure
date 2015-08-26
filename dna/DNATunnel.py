from adventurebase.AdventureGlobals import *
from DNADummy import *

from pandac.PandaModules import CollisionHandlerFloor, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionTube, CollisionTraverser, BitMask32, CollisionRay, NodePath


class DNATunnel():
 
    def __init__(self):
        self.type = ''
        self.name = ''
        self.pos = (0,0,0)
        self.hpr = (0,0,0)
        self.scale = (0,0,0)
        self.exit = ''
        self.nextroom = ''
        
        
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
        

    def setExit(self, exit):
        self.exit = exit
        
        
    def setNextRoom(self, nextroom):
        self.nextroom = nextroom
        
        
    def createNode(self):
        print 'hello?'
        ### Build a dummy so we can attatch a collision to it later ###
        # Call this so we can create a dummy
        self.DNADummy = DNADummy()
        # Set the dummy's properties
        self.DNADummy.setType('dummy')
        self.DNADummy.setName(self.name)
        self.DNADummy.setPos(self.pos)
        self.DNADummy.setHpr(self.hpr)
        self.DNADummy.setScale(self.scale)
        self.DNADummy.createNode()

        # Allow the dummy node to be accessible to this class!!!
        self.node = self.DNADummy.node

        self.node = render.attachNewNode(self.name)
    
    
        # Set the collision geometry; we need first a CollisionNode
        sensor = self.node.attachNewNode(CollisionNode(self.name))
        # We add that to our CollisionSphere geometry primitive
        sensor.node().addSolid(CollisionTube(-14,0,0,14,0,0,1.5))
        sensor.node().setFromCollideMask(BitMask32.allOff())
        sensor.node().setIntoCollideMask(DOOR_MASK)
        sensor.show()
        

        
        # Collision logic
        #self.main.accept('playersensor-into-' + name, self.main.transition, [newroom, exittunnel])
        
        
        
        
        
        
        
        
    def destroy(self):
        print self.node
        self.node.removeNode()






