from pandac.PandaModules import BitMask32
import os

# Get current directory the application was launched in
mdir = os.getcwd()

# Resource path
Resources = (mdir + '/' + 'resources/')

# Collision masks
WALL_MASK=BitMask32.bit(1)
DOOR_MASK=BitMask32.bit(2)
GATE_MASK=BitMask32.bit(3)

# Colors
Colors = {'black':(0,0,0,1),
                'white': (1,1,1,1),
                'gray':(0.6,0.6,0.6,1),
                'red':(1,0,0,1),
                'green':(0,1,0.2,1),
                'lime green': (0.4,0.7,0.2,1),
                'lime yellow': (0.6,0.7,0.2,1),
                'blue':(0,0,1,1),
                'orange':(1,0.5,0,1),
                'pink':(1,0.5,0.5,1),
                'yellow':(1,1,0,1)
                }

# Settings for the player
PlayerModel = (Resources + 'models/players/player.egg')
PlayerWalkSpeed = 0.5
PlayerPos = (0,-15,1)