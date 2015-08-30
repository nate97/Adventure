import sys
import yaml

from DNANode import *
from DNATunnel import *
from adventurebase.AdventureGlobals import *

from pandac.PandaModules import CollisionHandlerFloor, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionTube, CollisionTraverser, BitMask32, CollisionRay, NodePath



class DNAParser():

    def __init__(self, main):
        
        print 'Imported DNAParser'
        
        ### Dna globals ###
        # We store all loaded up models here
        self.models = {}
        self.classes = {}
        # This is the common color of the current room we are in!
        self.localColor = Colors['black']
        
        
        # Call back to the main class
        self.main = main
        


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

            self.classes[name] = DNATunnel(self)
            
            self.classes[name].setType(type)
            self.classes[name].setName(name)
            self.classes[name].setPos(pos)
            self.classes[name].setHpr(hpr)
            self.classes[name].setScale(scale)
            self.classes[name].setExit(exittunnel)
            self.classes[name].setNextRoom(newroom)
            
            # Now we actually create the model
            self.classes[name].createDoor()
                        
            
            
        # If the type of the object is not a tunnel then it is just a default model
        else:
            
            # Setup all the properties this type of object needs first
            
            # TESTING THIS
            self.classes[name] = DNANode()
            
            self.classes[name].setType(type)
            self.classes[name].setName(name)
            self.classes[name].setModel(model)
            self.classes[name].setPos(pos)
            self.classes[name].setHpr(hpr)
            self.classes[name].setScale(scale)
            self.classes[name].setColor(color)
            
            # Now we actually create the model
            self.classes[name].createModel()
            

            # TEMPORARY
            if type == 'room':
                self.localColor = color
                self.main.player.setColor(self.localColor)



    ### Destroys all classes in the current room the player is in ###
    def destroyRoom(self):

        for classes in self.classes:
            self.classes[classes].destroy()
            
        #print self.classes
