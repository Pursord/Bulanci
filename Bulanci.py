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
BROWN = (150, 75, 0)
GOLD = (212, 175, 55)

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
        given_file = open(file, 'r')

        lines = given_file.readlines()

        for line in lines:
            row = []
            for c in line:
                if c.isdigit():
                    row.append(c)
            self.map.append(row)

        given_file.close()

class Bulanek:
    def __init__(self, player, x, y):
        self.player = player
        self.x_position = x
        self.y_position = y
        self.move_speed = 0
        self.reload = 0
        self.health = 3
        self.direction = UP

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT, BUTTONS

    choice = input("Kterou mapu chcete hrat?")
    if not choice:
        choice = "Deadly_garden"
    mapa = choice + ".txt"
    
    pygame.init()
    game_map = Map()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Bulanci ale tanci")

    game_map.generate_map(mapa)
    player1 = Bulanek(1, 0, TILE_SIZE*2)
    player2 = Bulanek(2, (TILE_SIZE*24), TILE_SIZE*2)

    bullets = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            if event.type == KEYUP and event.key == K_c :
                bullets.append (Projectile(player1.x_position + TILE_SIZE, player1.y_position + TILE_SIZE, player1.direction))
            if event.type == KEYUP and event.key == K_SLASH :
                bullets.append (Projectile(player2.x_position + TILE_SIZE, player2.y_position + TILE_SIZE, player2.direction))
        
        handle_movement(game_map, player1, player2)
        
        for bullet in bullets:                         
            if bullet.direction == LEFT:
                bullet.x -= TILE_SIZE
            if bullet.direction == RIGHT:
                bullet.x += TILE_SIZE
            if bullet.direction == UP:
                bullet.y -= TILE_SIZE
            if bullet.direction == DOWN:
                bullet.y += TILE_SIZE

                
        draw_map(game_map)
        draw_bulanek(player1)
        draw_bulanek(player2)
        draw_bullet(bullets)
                                
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
        #type 4 is a black background
        pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left, top, TILE_SIZE, TILE_SIZE))
    if tile_type == "8":
        #type 8 are bridges
        pygame.draw.rect(DISPLAY_SURFACE, BROWN, (left, top, TILE_SIZE, TILE_SIZE))
    if tile_type == "9":
        #type 9 is a white background
        pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left, top, TILE_SIZE, TILE_SIZE))
    if tile_type == "5":
        #type 5 are teleporters
        pygame.draw.rect(DISPLAY_SURFACE, DARK_TURQUOISE, (left, top, TILE_SIZE, TILE_SIZE))
        
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

def draw_bullet(bullets):
    for bullet in bullets:                                
            if bullet.direction == LEFT:
                rect = pygame.Rect(0, 0, 20, 10)
                rect.center = (bullet.x, bullet.y)
                pygame.draw.rect(DISPLAY_SURFACE, GOLD, rect)
            if bullet.direction == RIGHT:
                rect = pygame.Rect(0, 0, 20, 10)
                rect.center = (bullet.x, bullet.y)
                pygame.draw.rect(DISPLAY_SURFACE, GOLD, rect)
            if bullet.direction == UP:
                rect = pygame.Rect(0, 0, 10, 20)
                rect.center = (bullet.x, bullet.y)
                pygame.draw.rect(DISPLAY_SURFACE, GOLD, rect)
            if bullet.direction == DOWN:
                rect = pygame.Rect(0, 0, 10, 20)
                rect.center = (bullet.x, bullet.y)
                pygame.draw.rect(DISPLAY_SURFACE, GOLD, rect)
        
    
def check_move(game_map, x, y):
    line, row = x/TILE_SIZE, y/TILE_SIZE
    line = round(line)
    row = round(row)
    if row >= 0 and line >= 0 and row < 26 and line < 26:
        if game_map.map[row][line] == "0" or game_map.map[row][line] == "4" or game_map.map[row][line] == "9":
            return True
    return False

def handle_movement(game_map, player1, player2):
    speed = TILE_SIZE
    speed_limit = 2
    keys = pygame.key.get_pressed()

    #handles movement for the 2nd player
    if player2.move_speed == 0:
        if keys[pygame.K_UP]:
            player2.direction = UP
            y = (player2.y_position - TILE_SIZE)
            if check_move(game_map, (player2.x_position), y) and check_move(game_map, (player2.x_position + TILE_SIZE), y):
                player2.y_position -= speed
                player2.move_speed = speed_limit
        if keys[pygame.K_DOWN]:
            player2.direction = DOWN
            y = (player2.y_position + TILE_SIZE*2)
            if check_move(game_map, (player2.x_position), y) and check_move(game_map, (player2.x_position + TILE_SIZE), y):
                player2.y_position += speed
                player2.move_speed = speed_limit
        if keys[pygame.K_LEFT]:
            player2.direction = LEFT
            x = (player2.x_position - TILE_SIZE)
            if check_move(game_map, x, player2.y_position) and check_move(game_map, x, (player2.y_position + TILE_SIZE)):
                player2.x_position -= speed
                player2.move_speed = speed_limit
        if keys[pygame.K_RIGHT]:
            player2.direction = RIGHT
            x = (player2.x_position + TILE_SIZE*2)
            if check_move(game_map, x, player2.y_position) and check_move(game_map, x, (player2.y_position + TILE_SIZE)):
                player2.x_position += speed
                player2.move_speed = speed_limit
    else:
        player2.move_speed -= 1

    #handles movement for the 1st player
    if player1.move_speed == 0:
        if keys[pygame.K_w]:
            player1.direction = UP
            y = (player1.y_position - TILE_SIZE)
            if check_move(game_map, (player1.x_position), y) and check_move(game_map, (player1.x_position + TILE_SIZE), y):
                player1.y_position -= speed
                player1.move_speed = speed_limit
        if keys[pygame.K_s]:
            player1.direction = DOWN
            y = (player1.y_position + TILE_SIZE*2)
            if check_move(game_map, (player1.x_position), y) and check_move(game_map, (player1.x_position + TILE_SIZE), y):
                player1.y_position += speed
                player1.move_speed = speed_limit
        if keys[pygame.K_a]:
            player1.direction = LEFT
            x = (player1.x_position - TILE_SIZE)
            if check_move(game_map, x, player1.y_position) and check_move(game_map, x, (player1.y_position + TILE_SIZE)):
                player1.x_position -= speed
                player1.move_speed = speed_limit
        if keys[pygame.K_d]:
            player1.direction = RIGHT
            x = (player1.x_position + TILE_SIZE*2)
            if check_move(game_map, x, player1.y_position) and check_move(game_map, x, (player1.y_position + TILE_SIZE)):
                player1.x_position += speed
                player1.move_speed = speed_limit
    else:
        player1.move_speed -= 1
        
    pass

def terminate():
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()
