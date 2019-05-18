# Simpsons Level-1
""" tilemap.py:
    - Map : map class
"""

__author__ = "Daniel Biehle"
__email__ = "dannybrain@dannybrain.org"
__version__ = 0.1

import pygame as pg
from settings import *

class Camera:
    """ Camera class, used to draw a portion of the map
    """
    def __init__(self, width: int, height: int):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)


    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit to scrolling map
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)

class Map:
    """ Map class

    public attributes:
    - data : the actual array of the map
    - width/height is the actual width/height of the map
    in pixel while tilewidth/tileheight is the nb of tiles
    """
    def __init__(self, filename: str):
        self.data = []
        with open(filename, 'r') as f:
            for lines in f:
                self.data.append(lines.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

    def __repr__(self):
        return  f"""Map tilewidth: {self.tilewidth}
                  \rMap tileheight: {self.tileheight}
                  \rMap width: {self.width}
                  \rMap height: {self.height}
                 """
                