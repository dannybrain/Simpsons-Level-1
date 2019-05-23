#!/usr/bin/env python
"""Simpsons Level-1 A simple platformer

   Inspired by Mario-Level-1 and by the  amazing
   "Game development with pygame" serie by KidsCanCode
"""
__author__ = "Daniel Biehle"
__email__ = "dannybrain@dannybrain.org"
__version__ = 0.1

from os import path
import pygame as pg
from settings import *
from sprites import Player, Wall
from tilemap import Map, Camera

class Game:
    """Main game class

        public attributes:
        - sprite groups : all_sprites, walls, player
        - map : simple class representing the map (read from map.txt)
        - dt : delta (tick)
    """

    def __init__(self):
        "initialize game window, etc"
        pg.init()
        pg.mixer.init()
        #pg.key.set_repeat(*KEY_REPEAT)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.all_sprites = []
        self.map = None
        self.player = None
        self.walls = None
        self.camera = None
        self.player_img = None
        self.dt = 0

    def new(self):
        "start a new game"
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.load_data()
        self.camera = Camera(self.map.width, self.map.height)
        self.run()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.load_map(game_folder)
        sprites_folder = path.join(game_folder, "spritesheets")
        self.load_sprites(sprites_folder)

    def load_sprites(self, sprites_folder):
        homer_img_path = path.join(sprites_folder, "homerx.png")
        self.player.set_image(pg.image.load(homer_img_path).convert_alpha())

    def load_map(self, game_folder):
        """ load map and initialise self.player and instanciates Walls"""
        self.map = Map(path.join(game_folder, MAP_FILE))
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == MAP_WALL:
                    Wall(self, col, row)
                if tile == MAP_PLAYER:
                    self.player = Player(self, col, row)

    def run(self):
        "Game Loop"
        self.playing = True
        while self.playing:
            #self.dt = self.clock.tick(FPS) / 800
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        "Game Loop - Update"
        self.all_sprites.update()
        self.camera.update(self.player)

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

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def draw(self):
        "Game Loop - draw"
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        #self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # *after* drawing everything, flip the display
        self.show_debug()
        pg.display.flip()

    def show_start_screen(self):
        "game splash/start screen"
        pass

    def show_go_screen(self):
        "game over/continue"
        pass

    def show_debug(self):
        self.debug(f"""x={int(self.player.pos.x)}
                    y={int(self.player.pos.y)}
                    dt={int(self.dt)}
                    acc={self.player.acc.x}
                    velx={self.player.vel.x}
                    vely={self.player.vel.y}
                    cameratopleft={self.camera.camera.topleft}""")

    def debug(self, text):
        "display message on screen : debug purpose"
        font = pg.font.Font(pg.font.get_default_font(), 11)
        antialias = True
        color = RED
        debug_msg = font.render(text, antialias, color)
        self.screen.blit(debug_msg, (0, 0))

def main():
    mygame = Game()
    mygame.show_start_screen()
    while mygame.running:
        mygame.new()
        mygame.show_go_screen()

    pg.quit()

if __name__ == '__main__':
    main()
