import sys
import yaml

class Test():

    def __init__(self):
        
        self._functions = {"pos": self.setPos,
                           "scale": self.setScale,
                           "type": self.setType,
                           "name":self.setName
                           }
        
        print 'Start'
        
        self.parseYAML('room_yellow.yaml')
        
        
        
    # Calls the function based on the current header we're iterating over in the yaml file
    def callFunction(self, header, arg):
        self._functions[header](arg)
        
        
        
    # This parses the current yaml file we've been given
    def parseYAML(self, dnafile):
        # Open the yaml file for reading
        with open(dnafile, 'r') as f:
            dna = yaml.load(f)
        
        
        # Iterate over every node in the yaml file
        for nodes in dna:
            
            print ''
            # Get every header (setting) for the node
            for header in dna[nodes]:
                
                # Parse the arg out for this setting
                arg = dna[nodes][header]
                
                # Call the appropriate function based on the header
                self.callFunction(header, arg)
                
                
                
    def setType(self, type):
        print 'Type: type'
        print type
        
        
        
    def setName(self, name):
        print 'Type: name'
        print name
        
        
        
    def setPos(self, pos):
        print 'Type: pos'
        print pos
        
        
        
    def setScale(self, scale):
        print 'Type: scale'
        print scale



test = Test()