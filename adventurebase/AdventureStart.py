from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task.Task import Task
from panda3d.core import *
import sys

from pandac.PandaModules import CollisionHandlerFloor, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionTube, CollisionTraverser, BitMask32, CollisionRay, NodePath

from AdventureGlobals import *

class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)


        ###### Collisions ######
        base.cTrav = CollisionTraverser()
        self.collisionHandler = CollisionHandlerEvent()
        self.wallHandler = CollisionHandlerPusher()
        
        self.collisionHandler.addInPattern('%fn-into-%in')

        # this is on the other hand the relative call for the OUT event, as is when the FROM object (heart) goes OUT the INTO oject (heart).
        self.collisionHandler.addOutPattern('%fn-out-%in')

        
        # localPlayer globals
        self.localColor = Colors['black']
        
        base.cam.setPos(0,0,100)
        base.cam.setHpr(0,-90,0)

        # This is used to store which keys are currently pressed.
        self.keyMap = {
            "left": 0, "right": 0, "forward": 0, "backward": 0}
 
        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left", True])
        self.accept("arrow_right", self.setKey, ["right", True])
        self.accept("arrow_up", self.setKey, ["forward", True])
        self.accept("arrow_down", self.setKey, ["backward", True])
        self.accept("arrow_left-up", self.setKey, ["left", False])
        self.accept("arrow_right-up", self.setKey, ["right", False])
        self.accept("arrow_up-up", self.setKey, ["forward", False])
        self.accept("arrow_down-up", self.setKey, ["backward", False])
        
        
        #self.accept('playersensor-into-doorcnode', self.loadRoom2)
        #self.accept('playersensor-outof-doorcnode', self.test)
        
        
        taskMgr.add(self.move, "moveTask")
        
        #** let start the collision check loop, called each 20th of second
        #taskMgr.add(self.traverseTask, "tsk_traverse")
        
        self.loadPlayerModel()
        
        self.loadRoom('example')
        
        self.setupColliders()
        
        #self.toggle_collisions()



    def loadPlayerModel(self):
        self.player = loader.loadModel(PlayerModel)
        self.player.reparentTo(render)
        self.player.setPos(0,-15,1)
        self.player.setScale(1,1,1)
        self.player.setColor(self.localColor)
        self.player.setCollideMask(BitMask32.allOff())
        
        
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



    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value



    # Moves the player around
    def move(self, task):
        dt = globalClock.getDt()

        if self.keyMap["left"]:
            self.player.setX(self.player.getX() - PlayerWalkSpeed)
        if self.keyMap["right"]:
            self.player.setX(self.player.getX() + PlayerWalkSpeed)
        if self.keyMap["forward"]:
            self.player.setY(self.player.getY() + PlayerWalkSpeed)
        if self.keyMap["backward"]:
            self.player.setY(self.player.getY() - PlayerWalkSpeed)

        return task.cont



    def loadRoom(self, test):
        print test
        
        # TEMP
        self.unloadRoom()
        
        self.localColor = Colors['yellow']
        self.player.setY(-24)
        self.player.setColor(self.localColor)

        self.dummyRoom = render.attachNewNode("Dummy room")
 
        roomcol = loader.loadModel(Rooms['room_0'])
        roomcol.reparentTo(self.dummyRoom)
        roomcol.setScale(7,3.5,1)
        roomcol.setPos(0,0,0)
        roomcol.setColor(self.localColor)


        # Let's mask our collision surfaces
        #floorcollider=roomcol.find("**/Plane")
        #floorcollider.node().setIntoCollideMask(FLOOR_MASK)
        wallcollider=roomcol.find("**/Plane")
        wallcollider.node().setIntoCollideMask(WALL_MASK)


        
        # Temp
        doorNode = render.attachNewNode("Dummy door")
        doorNode.reparentTo(self.dummyRoom)
        doorNode.setPos(0, -27, 0)
        #** ...then we set the collision geometry; we need first a CollisionNode...
        doorSensor = doorNode.attachNewNode(CollisionNode('doorcnode_0'))
        #...then we add to that our CollisionSphere geometry primitive.
        doorSensor.node().addSolid(CollisionTube(-14, 0, 0, 14, 0, 0, 1.5))
        doorSensor.node().setFromCollideMask(BitMask32.allOff())
        doorSensor.node().setIntoCollideMask(DOOR_MASK)
        doorSensor.show()

        self.accept('playersensor-into-doorcnode_0', self.loadRoom2)



    def loadRoom2(self, test):
        print test
        
        # TEMP
        self.unloadRoom()
        
        self.localColor = Colors['green']
        self.player.setY(24)
        self.player.setColor(self.localColor)

        self.dummyRoom = render.attachNewNode("Dummy room")
 
        roomcol = loader.loadModel(Rooms['room_2'])
        roomcol.reparentTo(self.dummyRoom)
        roomcol.setScale(7,3.5,1)
        roomcol.setPos(0,0,0)
        roomcol.setColor(self.localColor)


        wallcollider=roomcol.find("**/Plane")
        wallcollider.node().setIntoCollideMask(WALL_MASK)



        # Temp
        doorNode = render.attachNewNode("Dummy door")
        doorNode.reparentTo(self.dummyRoom)
        doorNode.setPos(0, 27, 0)
        #** ...then we set the collision geometry; we need first a CollisionNode...
        doorSensor = doorNode.attachNewNode(CollisionNode('doorcnode_1'))
        #...then we add to that our CollisionSphere geometry primitive.
        doorSensor.node().addSolid(CollisionTube(-14, 0, 0, 14, 0, 0, 1.5))
        doorSensor.node().setFromCollideMask(BitMask32.allOff())
        doorSensor.node().setIntoCollideMask(DOOR_MASK)
        doorSensor.show()

        self.accept('playersensor-into-doorcnode_1', self.loadRoom)



    def unloadRoom(self):
        try:
            self.dummyRoom.removeNode()
        except:
            print 'Nothing 2 remove'



    def setupColliders(self):
        # Tell collider what to check for
        self.wallHandler.addCollider(self.playerCollider, self.player) 

        # Adding to trav turns it into a from object( moving object )
        base.cTrav.addCollider(self.playerCollider, self.wallHandler)

        # Adding to trav turns it into a from object( moving object )
        base.cTrav.addCollider(self.playerSensor, self.collisionHandler)



    def toggle_collisions(self):
        base.cTrav.showCollisions(base.render)
        l=base.render.findAllMatches("**/+CollisionNode")


 
app = MyApp()
app.run()