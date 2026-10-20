import pygame as pg
from pygame.sprite import Sprite
from andrew_hulse_ICP_egg_beater.settings import *
from andrew_hulse_ICP_egg_beater.utils import *
from os import path

vec = pg.math.Vector2

# Creates player class with Sprite as super class

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

# checking for collision with walls and the player.

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # print("collided with wall from x dir")
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # print("collided with wall from y dir")
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def collide_with_coins(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, True, collide_hit_rect)
        if hits:
            # print("collided with wall from x dir")
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, True, collide_hit_rect)
        if hits:
            # print("collided with wall from y dir")
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

# class for the player:
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_image()
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.vx, self.vy = 0,0
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE/2
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        # stuff with animation
        self.current_frame = 0
        self.last_update = 0
        # accounting for states of the player.
        self.jumping = False
        self.moving = False
        self.coins = 0

    # gets player input
    def get_keys(self):
        # self.vx,self.vy = 0,0
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            # self.vy = -PLAYER_SPEED
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_a]:
            # self.vx = -PLAYER_SPEED
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_s]:
            # self.vy = PLAYER_SPEED
            self.vel.y = PLAYER_SPEED
        if keys[pg.K_d]:
            # self.vx = PLAYER_SPEED
            self.vel.x = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
             self.vel *= 0.7071
    def load_image(self):
        self.idle_frames = self.spritesheet.get_image(0,0,TILESIZE, TILESIZE), self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
    def jump(self):
        pass
    # Updates the game every frame to check for collision, animation, inputs, etc.
    def update(self):
        self.get_keys()
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        if hits:
            self.coins += 1
            print(f"I have {self.coins} coins")

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

# class for the enemy/evil sponge bob:
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_image()
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        # stuff with animation
        self.current_frame = 0
        self.last_update = 0
        # mob state
        self.jumping = False
        self.moving = False



    def load_image(self):
        self.idle_frames = self.spritesheet.get_image(0,0,TILESIZE, TILESIZE), self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
    # Updates the game every frame to check for collision, animation, inputs, etc.
    def update(self):
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

# Making a green wall sprite.
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x * TILESIZE
        self.y = y * TILESIZE

# class Coin(Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.all_coins
#         Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         pg.draw.circle(self.image, GOLD, (TILESIZE/2, TILESIZE/2), TILESIZE)
#         self.rect = self.image.get_rect()
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE
#         self.x = x * TILESIZE
#         self.y = y * TILESIZE




