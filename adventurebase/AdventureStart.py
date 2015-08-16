from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task.Task import Task
from panda3d.core import *
import sys
import yaml

from pandac.PandaModules import CollisionHandlerFloor, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionTube, CollisionTraverser, BitMask32, CollisionRay, NodePath

from AdventureGlobals import *

class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)

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
        
        

        
        taskMgr.add(self.move, "moveTask")
        


        dnafile = '/home/nathan/Documents/Git/Adventure/resources/dna/room_yellow_castle.yaml'
        
        
        self.loadPlayerModel()
        
        self.createRoom(dnafile)


        
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



    # Dose basic setup for the next room and keeps
    # the player avatar in place!
    def initTransition(self, dnafile, tunnel, coll):
        
        self.createRoom(dnafile)

        # Get position of tunnel the player is leaving
        
        tunnelpos = self.models[tunnel].getY()
        if tunnelpos > self.player.getY():
            self.player.setY(self.models[tunnel].getY() - 5)
        else:
            self.player.setY(self.models[tunnel].getY() + 5)



    ### Builds the room the player is currently in ###
    def createRoom(self, dnafile):
        
        # First things first make sure we clear everything!
        self.destroyRoom()
        
        
        ### Open the dna file ###
        with open(dnafile, 'r') as f:
            dna = yaml.load(f)

        ### Iterate over all the objects in the dna file. ###
        ### Remember we're doing this in a FOR LOOP!!!    ###
        for nodes in dna:
            print nodes
            
            ### COMMON PROPERTIES ###
            
            type = dna[nodes]['type']
            
            name = dna[nodes]['name']
            
            model = dna[nodes]['model']
            
            pos_list = dna[nodes]['pos']
            pos = tuple(pos_list)
            
            scale_list = dna[nodes]['scale']
            scale = tuple(scale_list)
            
            color_str = dna[nodes]['color']
            color = Colors[color_str]


            ### SPECIAL PROPERTIES ###
            
            
            if type == 'room':
                try:
                    self.player.setColor(color)
                except:pass
            
            
            if type == 'door':
                print 'Adding collision'

                coll_list = dna[nodes]['collision']
                collision = tuple(coll_list)

                moveto_room = dna[nodes]['room']
                
                tunnel = dna[nodes]['tunnel']
                
                self.createGraphicNode(name, type, model, pos, scale, color, collision, moveto_room, tunnel)

            else:
                # Create the node!!!
                self.createGraphicNode(name, type, model, pos, scale, color)



    ### Destroys all nodes in the current room the player is in ###
    def destroyRoom(self):
        for nodes in self.models:
            self.models[nodes].removeNode()



    ### Creates the object with the neccisary properties and appends ###
    ### the object into a dictionary so we can easily modify it      ###
    ### later on in the game.                                        ###
    def createGraphicNode(self, name, type, model, pos, scale, color, collision = None, moveto_room = None, tunnel = None):

            # Load a collision node
            if collision != None:
                self.models[name] = render.attachNewNode(name)
                self.models[name].reparentTo(render)
                self.models[name].setPos(pos)
                
                # then we set the collision geometry; we need first a CollisionNode
                sensor = self.models[name].attachNewNode(CollisionNode(name))
                #...then we add to that our CollisionSphere geometry primitive.
                sensor.node().addSolid(CollisionTube(-14,0,0,14,0,0,1.5))
                sensor.node().setFromCollideMask(BitMask32.allOff())
                sensor.node().setIntoCollideMask(DOOR_MASK)
                sensor.show()

                self.accept('playersensor-into-' + name, self.initTransition, [moveto_room, tunnel])


            # Load a default graphical node
            else:
                self.models[name] = loader.loadModel(model)
                self.models[name].reparentTo(render)
                self.models[name].setPos(pos)
                self.models[name].setScale(scale)
                self.models[name].setColor(color)



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