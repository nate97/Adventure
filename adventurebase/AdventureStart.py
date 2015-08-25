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

        self.models = {}


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
        
        self.dnaParser = DNAParser()
        
        
        self.dnaParser.createRoom(dnafile)
        
        #self.createRoom(dnafile)

        #self.setupColliders()
        
        #self.toggle_collisions()



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
        
        self.createRoom(newroom)
        
        self.positionCalculator(exittunnel)



    # Calculates where to place the player when he
    # exits a tunnel
    def positionCalculator(self, tunnel):
        
        # Get position of tunnel the player is exiting from
        tunnelX = self.models[tunnel].getX()
        tunnelY = self.models[tunnel].getY()
        tunnelhpr = self.models[tunnel].getH()
        
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



    ### Builds the room the player is currently in ###
    def createRoom(self, dnafile):
        
        ### First things first make sure everything ###
        ### in the scene is already clear           ###
        self.destroyRoom()
        
        # Append path to file name
        dnafile = Resources + dnafile
        
        ### We open the dna file ###
        with open(dnafile, 'r') as f:
            dna = yaml.load(f)

        ### Iterate over objects in the dna file.    ###
        ### Remember we're doing this in a FOR LOOP! ###
        for nodes in dna:
            
            # Setup default properties
            type = None
            name = ''
            model = ''
            pos = (0,0,0)
            hpr = (0,0,0)
            scale = (1)
            color = (1)
            exittunnel = None
            newroom = None
            
            
            ### REQUIRED PROPERTIES ###
            type = dna[nodes]['type']
            
            name = dna[nodes]['name']
            
            
            ### OPTIONAL PROPERTIES ###
            if 'model' in dna[nodes]:
                modelname = dna[nodes]['model']
                # Append path to file name
                model = Resources + modelname
                
            if 'pos' in dna[nodes]:
                pos_list = dna[nodes]['pos']
                pos = tuple(pos_list)
                
            if 'hpr' in dna[nodes]:
                hpr_list = dna[nodes]['hpr']
                hpr = tuple(hpr_list)
                
            if 'scale' in dna[nodes]:
                scale_list = dna[nodes]['scale']
                scale = tuple(scale_list)
                
            if 'color' in dna[nodes]:
                color_str = dna[nodes]['color']
                color = Colors[color_str]
            
            if 'exittunnel' in dna[nodes]:
                exittunnel = dna[nodes]['exittunnel']
                
            if 'newroom' in dna[nodes]:
                newroom = dna[nodes]['newroom']


            # Call the first method into the process of 
            # adding the object into the game
            self.prepareNode(type, name, model, pos, hpr, scale, color, exittunnel, newroom)



    def prepareNode(self, type, name, model, pos, hpr, scale, color, exittunnel, newroom):
        #print 'Preparing node'
        #print (type, name, model, pos, hpr, scale, color, exittunnel, newroom)

        ### This is so we call the corrosponding methods based ###
        ### on what kind of object we are going to load        ###

        # If the object is a tunnel...
        if type == 'tunnel':
            self.createDoor(type, name, pos, hpr, scale, exittunnel, newroom)
            
        # If the type of the object is not a tunnel...
        else:
            self.createModel(type, name, model, pos, hpr, scale, color)

            # TEMPORARY
            if type == 'room':
                self.localColor = color
                self.localPlayer.setColor(self.localColor)



    ### Creates the model with the required properties and appends ###
    ### the object into a dictionary so we can easily modify it      ###
    def createModel(self, type, name, model, pos, hpr, scale, color):
        self.models[name] = loader.loadModel(model)
        self.models[name].reparentTo(render)
        self.models[name].setPos(pos)
        self.models[name].setHpr(hpr)
        self.models[name].setScale(scale)
        self.models[name].setColor(color)



    # This is for building a generic dummy node for other
    # nodes to be parented to
    def createDummy(self, type, name, pos, hpr, scale):
        self.models[name] = render.attachNewNode(name)
        self.models[name].reparentTo(render)
        self.models[name].setPos(pos)
        self.models[name].setHpr(hpr)
        self.models[name].setScale(scale)



    # Create a specific type of object called a door 
    def createDoor(self, type, name, pos, hpr, scale, exittunnel, newroom):
        
        # Builds a dummy with the name supplied for our collision
        # to be appended to
        self.createDummy(type, name, pos, hpr, scale)
        
        # Set the collision geometry; we need first a CollisionNode
        sensor = self.models[name].attachNewNode(CollisionNode(name))
        # We add that to our CollisionSphere geometry primitive
        sensor.node().addSolid(CollisionTube(-14,0,0,14,0,0,1.5))
        sensor.node().setFromCollideMask(BitMask32.allOff())
        sensor.node().setIntoCollideMask(DOOR_MASK)
        sensor.show()
        
        # Collision logic
        self.accept('playersensor-into-' + name, self.transition, [newroom, exittunnel])



    ### Destroys all nodes in the current room the player is in ###
    def destroyRoom(self):
        for nodes in self.models:
            self.models[nodes].removeNode()



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