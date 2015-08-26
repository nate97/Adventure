from pandac.PandaModules import CollisionHandlerFloor, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionTube, CollisionTraverser, BitMask32, CollisionRay, NodePath
from AdventureGlobals import *



class LocalPlayer():
 
    def __init__(self):
        # THIS SHOULD BE ELSE WHERE!!!
        # We probably need a class that act's like a manager for
        # all players currently in game so we can keep track of
        # everyone online
        self.playerList = {}
        
        # Define default player model
        self.model = PlayerModel
        # Define default position
        self.pos = (1,1,1)
        # Define default scale
        self.scale = (1,1,1)
        # Define default color
        self.colorIndex = (1,1,1)



    def loadPlayerModel(self, model):   
        self.model = model
        self.player = loader.loadModel(self.model)
        self.player.reparentTo(render)



    def setPos(self, pos):
        self.pos = pos
        self.player.setPos(pos)



    def setScale(self, scale):
        self.scale = scale
        self.player.setPos(self.scale)



    def setColor(self, colorIndex):
        self.colorIndex = colorIndex
        self.player.setColor(self.colorIndex)
        
        
        
    def setCollisions(self):
        # Add physical collision object to player
        self.playerCollider = self.player.attachNewNode(CollisionNode('playercnode'))
        self.playerCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))
        # Adding to trav turns it into a from object( moving object )
        #base.cTrav.addCollider(self.playerCollider, self.collisionHandler)
        self.playerCollider.node().setFromCollideMask(WALL_MASK)
        self.playerCollider.node().setIntoCollideMask(BitMask32.allOff())

        # Sensor collision
        self.playerSensor = self.player.attachNewNode(CollisionNode('playersensor'))
        cs=CollisionSphere(0, 0, 0, 1.2)
        self.playerSensor.node().addSolid(cs)
        self.playerSensor.node().setFromCollideMask(DOOR_MASK)
        self.playerSensor.node().setIntoCollideMask(BitMask32.allOff())
        # as said above, to act correctly we need to make clear to the system that this is just a sensor, with no solid parts
        cs.setTangible(0)