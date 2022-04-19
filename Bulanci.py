import pygame
from pygame.locals import *
import sys
import random

WINDOW_SIZE = 728
TILE_SIZE = 28
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_BLUE = (0, 50, 255)
DARK_TURQUOISE = (3, 54, 73)
GREEN = (3, 133, 5)
RED = (214, 28, 8)
GREY = (204, 195, 198)
YELLOW = (255, 255, 0)
PINK = (255, 51, 153)

#constants for movement
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#global variables to be used
FPS_CLOCK = None
DISPLAY_SURFACE = None
BASIC_FONT = None
BUTTONS = None

class Map:
    def __init__(self):
        self.map = []
        self.map_width = 26
        self.map_height = 26

    def generate_map(self, file):
        given_file = open(f'{file}', 'r')

        lines = given_file.readlines()

        for line in lines:
            row = []
            for c in line:
                if c.isdigit() == True:
                    row.append(c)
            self.map.append(row)

        given_file.close()

class Bulanek:
    def __init__(self, player, x, y):
        self.player = player
        self.x_position = x
        self.y_position  = y
        self.health = 3
        self.direction = UP

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT, BUTTONS
    
    mapa = str(input("Kterou mapu chcete hrat?") + ".txt")
    
    pygame.init()
    game_map = Map()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Bulanci ale tanci")

    game_map.generate_map(mapa)
    player1 = Bulanek(1, 0, TILE_SIZE*2)
    player2 = Bulanek(2, (TILE_SIZE*24+1), TILE_SIZE*2)
    
    while True:
        draw_map(game_map)
        draw_bulanek(player1)
        draw_bulanek(player2)        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
                
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def draw_tile(row, line, tile_type):
    top, left = (row * TILE_SIZE), (line * TILE_SIZE)
    if tile_type == "1":
        #type 1 are bricks
        pygame.draw.rect(DISPLAY_SURFACE, RED, (left, top, TILE_SIZE, TILE_SIZE))
    if tile_type == "2":
        #type 2 are undestructible blocks
        pygame.draw.rect(DISPLAY_SURFACE, GREY, (left, top, TILE_SIZE, TILE_SIZE))
    if tile_type == "3":
        #type 3 are blocks where you can not stand
        pygame.draw.rect(DISPLAY_SURFACE, BRIGHT_BLUE, (left, top, TILE_SIZE, TILE_SIZE))
    if tile_type == "4":
        #type 4 is black background
        pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left, top, TILE_SIZE, TILE_SIZE))

def draw_map(game_map):
    DISPLAY_SURFACE.fill(GREEN)
    for row in range(game_map.map_height):
        for line in range(game_map.map_width):
            if game_map.map[row][line] != 0:
                draw_tile(row, line, game_map.map[row][line])
                
def draw_bulanek(bulanek):
    if bulanek.player == 1:
        pygame.draw.rect(DISPLAY_SURFACE, PINK, (bulanek.x_position, bulanek.y_position, TILE_SIZE*2, TILE_SIZE*2))
    if bulanek.player == 2:
        pygame.draw.rect(DISPLAY_SURFACE, YELLOW, (bulanek.x_position, bulanek.y_position, TILE_SIZE*2, TILE_SIZE*2))


def terminate():
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()
