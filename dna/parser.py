from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task.Task import Task
from panda3d.core import *
import sys
import yaml



Colors = {'black':(0,0,0,1),
                'white': (1,1,1,1),
                'gray':(0.6,0.6,0.6,1),
                'red':(1,0,0,1),
                'green':(0,1,0,1),
                'blue':(0,0,1,1),
                'orange':(1,0.5,0,1),
                'pink':(1,0.5,0.5,1),
                'yellow':(1,1,0,1)
                }



class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        self.models = {}
        
        
        dnafile = '/home/nathan/Documents/Git/Adventure/adventurebase/test.yaml'
        
        self.createRoom(dnafile)


        # localPlayer globals
        self.localColor = Colors['black']
        
        base.cam.setPos(0,0,100)
        base.cam.setHpr(0,-90,0)





    ### Builds the room the player is currently in ###
    def createRoom(self, dnafile):
        
        ### First things first we open the dna file ###
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
            
            if type == 'door':
                print 'Adding collision'

                coll_list = dna[nodes]['collision']
                collision = tuple(coll_list)

                moveto_room = dna[nodes]['room']
                self.createGraphicNode(name, type, model, pos, scale, color, collision, moveto_room)

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
    def createGraphicNode(self, name, type, model, pos, scale, color, collision = None, moveto_room = None):

            # Load a collision node
            if collision != None:
                print 'colllllllllllllllllllll'
                print collision
                self.models[name] = render.attachNewNode(name)
                self.models[name].reparentTo(render)
                self.models[name].setPos(pos)
                
                
                # then we set the collision geometry; we need first a CollisionNode
                sensor = self.models[name].attachNewNode(CollisionNode(name))
                #...then we add to that our CollisionSphere geometry primitive.
                sensor.node().addSolid(CollisionTube(-14,0,0,14,0,0,1.5))
                sensor.node().setFromCollideMask(BitMask32.allOff())
                sensor.node().setIntoCollideMask(1)
                sensor.show()

                self.accept('playersensor-into-' + name, self.createRoom, [moveto_room])


            # Load a default graphical node
            else:
                print name
                print 'yaaaaaaaaaaaaa'
                self.models[name] = loader.loadModel(model)
                self.models[name].reparentTo(render)
                self.models[name].setPos(pos)
                self.models[name].setScale(scale)
                self.models[name].setColor(color)






app = MyApp()
app.run()