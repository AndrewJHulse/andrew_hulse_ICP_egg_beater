# This file was created by: Chris Cozort
# Content inspired by: Chris Bradfield.
# I do solemnly swear to create concise and informative comments.

'''
The game engine consists of three (4) basic components
Input - keys, buttons, voice, mouse, touch, breath, movement, joysick
Process - input processed (direction of control, magnitude)
Output - Draw new frames, pixels, sound, haptics (senses)

GOALS: Make a spatula for evil spongebob, beat evil spongebob by making an egg projectile and a collectible that gives the egg gun.
RULES: Don't get killed by evil spongebob
FEEDBACK: 
FREEDOM: 
'''

import pygame as pg
from os import path
from settings import *
from sprites import *
from utils import *


# the game class a blueprint for the whole game...
class Game:
    # 
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print('game class initialized')
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.score = 0
        self.highscore = 0

    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.game_save_file = path.join(self.game_dir,"highscore.txt")
        self.img_dir = path.join(self.game_dir, 'images')
        # sound stuff
        self.snd_dir = path.join(self.game_dir, 'sounds')
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "coin_pickup.mp3"))

        self.map = Map(path.join(self.game_dir, map))

        # file creation
        try:
            with open(self.game_save_file, 'x', encoding="utf-8") as file:
                file.write("Hello, World!")
            print("File created successfully.")
        except FileExistsError:
            print("File already exists. No action taken.")

        # opens the file and sets the highscore to 0
        with open(self.game_save_file, 'r') as f:
            try:
                self.highscore = int(f.read())
                print('high score set')
            except:
                self.highscore = 0
                print("high score is zero")
# all sprites being instantiated
    def new(self):
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_particles = pg.sprite.Group()
        self.all_tiles = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)

    def run(self):
        while self.running:
            # sets the delta time property and runs the tick function at FPS/1000
            self.dt = self.clock.tick(FPS) / 1000
            self.events() # this gets player input
            self.update() # this updates the game
            self.draw() # this draws sprites
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                with open(path.join(self.game_dir, self.game_save_file), 'w') as f:
                    f.write(str(self.score))
                if self.playing:
                    self.playing = False
                self.running = False
    # this helps change the game based on inputs
    def update(self):
        self.all_sprites.update()

    # draw text on screen anywhere 
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        # instantiate the Font class
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text("Frames per second: " + str(floor(1/self.dt) ), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(f"Coins:{self.player.coins} ", 24, WHITE, WIDTH/2, HEIGHT/9)
        self.draw_text(f"Highscore:{self.highscore} ", 24, WHITE, WIDTH/2, HEIGHT/11)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()
    g.run()

pg.quit()