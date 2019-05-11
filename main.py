#!/usr/bin/env python
# Simpsons Level-1
# A simple platformer inspired by Mario-Level-1 and by the
# amazing "Game development with pygame" serie by KidsCanCode

__author__ = "Daniel Biehle"
__email__ = "dannybrain@dannybrain.org"
__version__ = 0.1

from os import path
import pygame as pg
from settings import *
from sprites import Player, Wall

class Game:
    "Main Game class"

    def __init__(self):
        "initialize game window, etc"
        pg.init()
        pg.mixer.init()
        pg.key.set_repeat(*KEY_REPEAT)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.all_sprites = []
        self.map_data = []
        self.player = None
        self.walls = None

    def new(self):
        "start a new game"
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        #self.all_sprites.add(self.player)
        self.load_data()
        self.run()

    def load_data(self):
        mapdir = path.dirname(__file__)
        with open(path.join(mapdir, MAP_FILE), 'r') as f:
            for lines in f:
                self.map_data.append(lines)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == MAP_WALL:
                    Wall(self, col, row)
                if tile == MAP_PLAYER:
                    self.player = Player(self, col, row)

    def run(self):
        "Game Loop"
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        "Game Loop - Update"
        self.all_sprites.update()

    def events(self):
        "Game Loop - events"
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_q, pg.K_ESCAPE):
                    self.running = False
                    self.playing = False
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def draw(self):
        "Game Loop - draw"
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        "game splash/start screen"
        pass

    def show_go_screen(self):
        "game over/continue"
        pass


def main():
    mygame = Game()
    mygame.show_start_screen()
    while mygame.running:
        mygame.new()
        mygame.show_go_screen()

    pg.quit()

if __name__ == '__main__':
    main()
