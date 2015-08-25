import sys
import yaml
from adventurebase.AdventureGlobals import *
from pandac.PandaModules import CollisionHandlerFloor, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionTube, CollisionTraverser, BitMask32, CollisionRay, NodePath
from direct.actor.Actor import Actor
from direct.task.Task import Task



class DNAParser():

    def __init__(self, main):
        
        self.main = main
        
        print 'Imported '
        self.models = {}


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
                #self.localPlayer.setColor(self.localColor)



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
        self.main.accept('playersensor-into-' + name, self.main.transition, [newroom, exittunnel])



    ### Destroys all nodes in the current room the player is in ###
    def destroyRoom(self):
        for nodes in self.models:
            self.models[nodes].removeNode()