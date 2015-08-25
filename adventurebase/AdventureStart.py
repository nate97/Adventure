from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task.Task import Task
from panda3d.core import *
import sys
import yaml

from pandac.PandaModules import CollisionHandlerFloor, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionTube, CollisionTraverser, BitMask32, CollisionRay, NodePath

from AdventureGlobals import *

from dna.DNAParser import *


from player import *

class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)

        # Panda settings
        base.cam.setPos(0,0,100)
        base.cam.setHpr(0,-90,0)

        base.setBackgroundColor(0.6,0.6,0.6)


        ###### Collisions ######
        base.cTrav = CollisionTraverser()
        self.collisionHandler = CollisionHandlerEvent()
        self.wallHandler = CollisionHandlerPusher()
        
        self.collisionHandler.addInPattern('%fn-into-%in')

        # this is on the other hand the relative call for the OUT event, as is when the FROM object (heart) goes OUT the INTO oject (heart).
        self.collisionHandler.addOutPattern('%fn-out-%in')

        
        # localPlayer globals
        self.localColor = Colors['black']
        

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


        taskMgr.add(self.move, "moveTask")
        

        dnafile = 'dna/room_yellow_castle.yaml'
        
        
        # NEW
        self.setupPlayer()
        
        self.dnaParser = DNAParser(self)
        
        
        self.dnaParser.createRoom(dnafile)
        
        self.setupColliders()

        




    def setupPlayer(self):
        # Load up player class
        self.localPlayer = LocalPlayer()
        
        # Load up player object
        self.localPlayer.loadPlayerModel(PlayerModel)
        
        # Make player object avalible to this class
        self.player = self.localPlayer.player
        
        # Set player color
        self.localPlayer.setPos((0,-15,1))
        
        # Setup player collisions
        self.localPlayer.setCollisions()



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



    # Dose basic setup for the next room and keeps
    # the player avatar in place!
    def transition(self, newroom, exittunnel, coll):
        
        self.dnaParser.createRoom(newroom)
        
        self.positionCalculator(exittunnel)



    # Calculates where to place the player when he
    # exits a tunnel
    def positionCalculator(self, tunnel):
        
        # Get position of tunnel the player is exiting from
        tunnelX = self.dnaParser.models[tunnel].getX()
        tunnelY = self.dnaParser.models[tunnel].getY()
        tunnelhpr = self.dnaParser.models[tunnel].getH()
        
        if tunnelhpr == 90:
            if self.player.getX() > tunnelX:
                self.player.setX(tunnelX + 5)
            else:
                self.player.setX(tunnelX - 5)
        
        else:
            if self.player.getY() > tunnelY:
                self.player.setY(tunnelY + 5)
            else:
                self.player.setY(tunnelY - 5)





    def setupColliders(self):
        # Tell collider what to check for
        
        # TEMP # 
        test = self.localPlayer.playerCollider
        
        test2 = self.localPlayer.playerSensor
        
        self.wallHandler.addCollider(test, self.player) 

        # Adding to trav turns it into a from object( moving object )
        base.cTrav.addCollider(test, self.wallHandler)

        # Adding to trav turns it into a from object( moving object )
        base.cTrav.addCollider(test2, self.collisionHandler)



    def toggle_collisions(self):
        base.cTrav.showCollisions(base.render)
        l=base.render.findAllMatches("**/+CollisionNode")

test = MyApp()
test.run()