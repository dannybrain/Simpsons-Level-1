# Simpsons Level-1
""" Sprites.py : group sprites and maps used in the game

    - Player : main player (homer or bart currently)
    - Walls : walls
    - Map : map data and function to load data from txt
"""

__author__ = "Daniel Biehle"
__email__ = "dannybrain@dannybrain.org"
__version__ = 0.1

import pygame as pg
from pygame.math import Vector2 as vec
from settings import *

class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.acc = vec(0, 0)

    def set_image(self, img):
        self.image = img
        self.rect = self.image.get_rect()

    def get_keys(self):
        # acceleration is 0 unless a key is pressed
        self.acc = vec(0, GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE]:
            self.jump()

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def jump(self):
        # jump only if on a platform
        if self.vel.y <= 0:
            #self.rect.x += 1
            #hits = pg.sprite.spritecollide(self, self.game.walls, False)
            #self.rect.x -= 1
            #if hits:
            self.vel.y = -40

    def update(self):
        self.get_keys()
        self.move()

    def move(self):
        # physics...
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.x = self.pos.x
        self.check_collision(direction='x')
        self.rect.y = self.pos.y
        self.check_collision(direction='y')

    def check_collision(self, direction='x'):
        if direction == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if direction == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y


class Wall(pg.sprite.Sprite):
    """ Wall class """

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        