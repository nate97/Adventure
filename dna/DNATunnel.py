from adventurebase.AdventureGlobals import *
from DNANode import *

from pandac.PandaModules import CollisionHandlerFloor, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionTube, CollisionTraverser, BitMask32, CollisionRay, NodePath


class DNATunnel(DNANode):
 
    def __init__(self, DNAParser):
        DNANode.__init__(self)
        
        # Call back to DNAParser
        self.DNAParser = DNAParser
        
        self.exit = ''
        self.nextroom = ''


    def setExit(self, exit):
        self.exit = exit
        
        
    def setNextRoom(self, nextroom):
        self.nextroom = nextroom
        
        
    def createDoor(self):
        # Tell DNANode to create the dummy node now
        self.createDummy()
    
        # Set the collision geometry; we need first a CollisionNode
        sensor = self.node.attachNewNode(CollisionNode(self.name))
        # We add that to our CollisionSphere geometry primitive
        sensor.node().addSolid(CollisionTube(-14,0,0,14,0,0,1.5))
        sensor.node().setFromCollideMask(BitMask32.allOff())
        sensor.node().setIntoCollideMask(DOOR_MASK)
        sensor.show()
        
        # Collision logic
        self.DNAParser.main.accept('playersensor-into-' + self.name, self.DNAParser.main.transition, [self.nextroom, self.exit])
        
