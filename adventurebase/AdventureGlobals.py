from pandac.PandaModules import BitMask32
# Resource path
Resources = ('../resources/')

# Collision masks
WALL_MASK=BitMask32.bit(1)
DOOR_MASK=BitMask32.bit(2)
# Colors
Colors = {'black':(0,0,0,1),
                'gray':(0.6,0.6,0.6,1),
                'red':(1,0,0,1),
                'green':(0,1,0,1),
                'blue':(0,0,1,1),
                'orange':(1,0.5,0,1),
                'pink':(1,0.5,0.5,1),
                'yellow':(1,1,0,1)
                }
# All models for each rooms
Rooms = {'room_0':(Resources + 'room_start_yellow.egg'),
         'room_1': (Resources + 'room_yellow.egg')
         }
# Settings for the player
PlayerModel = (Resources + 'player.egg')
PlayerWalkSpeed = 0.5