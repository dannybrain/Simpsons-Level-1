# Simpsons Level-1
""" tilemap.py: 
    - Map : map class
"""

__author__ = "Daniel Biehle"
__email__ = "dannybrain@dannybrain.org"
__version__ = 0.1

from settings import *


class Map():
    """ Map class 

    public attributes:
    - data : the actual array of the map
    - width/height is the actual width/height of the map
    in pixel while tilewidth/tileheight is the nb of tiles
    """
    def __init__(self, filename):
        self.data = []
        with open(filename, 'r') as f:
            for lines in f:
                self.data.append(lines)

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
    