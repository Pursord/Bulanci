import pygame
from pygame.locals import *
import sys
import random

WINDOW_SIZE = 728
TILE_SIZE = 28
FPS = 30
BUTTON_SIZE = TILE_SIZE * 2
GAP_SIZE = 16

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
NAVYBLUE = (60, 60, 100)
BLUE = (0, 0, 255)

BGCOLOR = BLACK
HIGHLIGHTCOLOR = BLUE
TEXTCOLOR = WHITE

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
        given_file = open(f"maps/{file}", 'r')

        lines = given_file.readlines()

        for line in lines:
            row = []
            for c in line:
                if c.isdigit():
                    row.append(c)
            self.map.append(row)

        given_file.close()

class Bulanek:
    def __init__(self, player, x, y, team):
        self.player = player
        self.x_position = x
        self.y_position = y
        self.team = team
        self.move_speed = 0
        self.reload = 0
        self.health = 7
        self.direction = UP

class Projectile:
    def __init__(self, x, y, direction, team):
        self.x = x
        self.y = y
        self.direction = direction
        self.team = team

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT, BUTTONS

    """
    choice = input("Kterou mapu chcete hrat?")
    if not choice:
        choice = "Deadly_garden"
    mapa = choice + ".txt"
    """
    
    pygame.init()
    game_map = Map()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Bulanci ale tanci")

    mapa = menu(game_map)
    game_map.generate_map(mapa)
    player1 = Bulanek(1, 0, TILE_SIZE*2, 1)
    player2 = Bulanek(2, (TILE_SIZE*24), TILE_SIZE*2, 2)

    bullets = []

    while True:

        key = pygame.key.get_pressed()
        if check_game_state(player1, player2) is not None:
            win = check_game_state(player1, player2)
            end_screen(game_map, win)
        check_game_state(player1, player2)
        draw_map(game_map)
        draw_bulanek(player1)
        draw_bulanek(player2)
        draw_bullet(bullets)
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            if player1.reload == 0:
                if key[K_c]:
                    bullets.append (Projectile(player1.x_position + TILE_SIZE, player1.y_position + TILE_SIZE, player1.direction, player1.team))
                    player1.reload = 5
            else:
                player1.reload -= 1
            if player2.reload == 0:                         
                if key[K_SLASH]: 
                    bullets.append (Projectile(player2.x_position + TILE_SIZE, player2.y_position + TILE_SIZE, player2.direction, player2.team))
                    player2.reload = 5
            else:
                player2.reload -= 1
        
        handle_movement(game_map, player1, player2)

        b = 0
        for bullet in bullets:
            if bullet.direction == LEFT:
                bullet.x -= TILE_SIZE
            if bullet.direction == RIGHT:
                bullet.x += TILE_SIZE
            if bullet.direction == UP:
                bullet.y -= TILE_SIZE
            if bullet.direction == DOWN:
                bullet.y += TILE_SIZE

            if (bullet.direction == UP or bullet.direction == DOWN):
                if check_hit(game_map, bullet.x - 15, bullet.y) or check_hit(game_map, bullet.x, bullet.y):
                    check_hit(game_map, bullet.x, bullet.y)
                    remove_bullet(bullets, b)
            if (bullet.direction == LEFT or bullet.direction == RIGHT):
                if check_hit(game_map, bullet.x, bullet.y - 15) or check_hit(game_map, bullet.x, bullet.y):
                    check_hit(game_map, bullet.x, bullet.y)
                    remove_bullet(bullets, b)
            if player_hit(player1, bullet):
                player1.health -= 1
                respawn(player1)
                remove_bullet(bullets, b)
            if player_hit(player2, bullet):
                player2.health -= 1
                respawn(player2)
                remove_bullet(bullets, b)
            
            b += 1
                                
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def draw_tile(row, line, tile_type):
    top, left = (row * TILE_SIZE), (line * TILE_SIZE)
    if tile_type == "1":
        #type 1 are bricks
        image = pygame.image.load("sprites/brick.png")
        DISPLAY_SURFACE.blit(image, (left, top))
        pass
    if tile_type == "2":
        #type 2 are undestructible blocks
        image = pygame.image.load("sprites/stone.png")
        DISPLAY_SURFACE.blit(image, (left, top))
        pass
    if tile_type == "3":
        #type 3 are blocks where you can not stand
        image = pygame.image.load("sprites/water.png")
        DISPLAY_SURFACE.blit(image, (left, top))
        pass
    if tile_type == "4":
        #type 4 is a black background
        pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left, top, TILE_SIZE, TILE_SIZE))
        pass
    if tile_type == "8":
        #type 8 are bridges
        image = pygame.image.load("sprites/bridge.png")
        DISPLAY_SURFACE.blit(image, (left, top))
        pass
    if tile_type == "9":
        #type 9 is a white background
        pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left, top, TILE_SIZE, TILE_SIZE))
    if tile_type == "5":
        #type 5 are teleporters
        pygame.draw.rect(DISPLAY_SURFACE, DARK_TURQUOISE, (left, top, TILE_SIZE, TILE_SIZE))
        
def draw_map(game_map):
    background = pygame.image.load("sprites/background.png")
    DISPLAY_SURFACE.blit(background, (0 , 0))
    for row in range(game_map.map_height):
        for line in range(game_map.map_width):
            if game_map.map[row][line] != 0:
                draw_tile(row, line, game_map.map[row][line])
                
def draw_bulanek(bulanek):
    if bulanek.player == 1:
        if bulanek.direction == LEFT:
            image = pygame.image.load("sprites/bulanek1_left.png")
            DISPLAY_SURFACE.blit(image, (bulanek.x_position, bulanek.y_position))
        if bulanek.direction == RIGHT:
            image = pygame.image.load("sprites/bulanek1_right.png")
            DISPLAY_SURFACE.blit(image, (bulanek.x_position, bulanek.y_position))
        if bulanek.direction == UP:
            image = pygame.image.load("sprites/bulanek1_back.png")
            DISPLAY_SURFACE.blit(image, (bulanek.x_position, bulanek.y_position))
        if bulanek.direction == DOWN:
            image = pygame.image.load("sprites/bulanek1_front.png")
            DISPLAY_SURFACE.blit(image, (bulanek.x_position, bulanek.y_position))

    if bulanek.player == 2:
        if bulanek.direction == LEFT:
            image = pygame.image.load("sprites/bulanek2_left.png")
            DISPLAY_SURFACE.blit(image, (bulanek.x_position, bulanek.y_position))
        if bulanek.direction == RIGHT:
            image = pygame.image.load("sprites/bulanek2_right.png")
            DISPLAY_SURFACE.blit(image, (bulanek.x_position, bulanek.y_position))
        if bulanek.direction == UP:
            image = pygame.image.load("sprites/bulanek2_back.png")
            DISPLAY_SURFACE.blit(image, (bulanek.x_position, bulanek.y_position))
        if bulanek.direction == DOWN:
            image = pygame.image.load("sprites/bulanek2_front.png")
            DISPLAY_SURFACE.blit(image, (bulanek.x_position, bulanek.y_position))

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

def remove_bullet(bullets, b):
    if 0 <= b < len(bullets):
        bullets.pop(b)
        
def check_hit(game_map, x, y):
    line, row = x/TILE_SIZE, y/TILE_SIZE
    line = round(line)
    row = round(row)
    if row >= 0 and line >= 0 and row < 26 and line < 26:
        if game_map.map[row][line] == "2":
            return True
        if game_map.map[row][line] == "1":
            game_map.map[row][line] = "0"
            return True
    return False

def player_hit(player, bullet):
    if bullet.x in range(player.x_position, (player.x_position + 3*TILE_SIZE)) and bullet.y in range(player.y_position, (player.y_position + 3*TILE_SIZE)):
        if bullet.team != player.team:
            return True

def check_move(game_map, x, y):
    line, row = x/TILE_SIZE, y/TILE_SIZE
    line = round(line)
    row = round(row)
    if row >= 0 and line >= 0 and row < 26 and line < 26:
        if game_map.map[row][line] == "0" or game_map.map[row][line] == "4" or game_map.map[row][line] == "9" or game_map.map[row][line] == "8":
            return True
    return False

def player_colission(player_m, player_ch):
    if player_m.direction == UP:
        if not ((player_m.y_position - TILE_SIZE) in range(player_ch.y_position, (player_ch.y_position + 2*TILE_SIZE)) and player_m.x_position in range(player_ch.x_position, (player_ch.x_position + 2*TILE_SIZE))):
            return True
    if player_m.direction == DOWN:
        if not ((player_m.y_position + 3*TILE_SIZE) in range(player_ch.y_position, (player_ch.y_position + 2*TILE_SIZE)) and player_m.x_position in range(player_ch.x_position, (player_ch.x_position + 2*TILE_SIZE))):
            return True
    if player_m.direction == LEFT:
        if not ((player_m.x_position - TILE_SIZE) in range(player_ch.x_position, (player_ch.x_position + 2*TILE_SIZE)) and player_m.y_position in range(player_ch.y_position, (player_ch.y_position + 2*TILE_SIZE))):
            return True
    if player_m.direction == RIGHT:
        if not ((player_m.x_position + 3*TILE_SIZE) in range(player_ch.x_position, (player_ch.x_position + 2*TILE_SIZE)) and player_m.y_position in range(player_ch.y_position, (player_ch.y_position + 2*TILE_SIZE))):
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
                if player_colission(player1, player2):
                    player2.y_position -= speed
                    player2.move_speed = speed_limit
        if keys[pygame.K_DOWN]:
            player2.direction = DOWN
            y = (player2.y_position + TILE_SIZE*2)
            if check_move(game_map, (player2.x_position), y) and check_move(game_map, (player2.x_position + TILE_SIZE), y):
                if player_colission(player1, player2):
                    player2.y_position += speed
                    player2.move_speed = speed_limit
        if keys[pygame.K_LEFT]:
            player2.direction = LEFT
            x = (player2.x_position - TILE_SIZE)
            if check_move(game_map, x, player2.y_position) and check_move(game_map, x, (player2.y_position + TILE_SIZE)):
                if player_colission(player1, player2):
                    player2.x_position -= speed
                    player2.move_speed = speed_limit
        if keys[pygame.K_RIGHT]:
            player2.direction = RIGHT
            x = (player2.x_position + TILE_SIZE*2)
            if check_move(game_map, x, player2.y_position) and check_move(game_map, x, (player2.y_position + TILE_SIZE)):
                if player_colission(player1, player2):
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
                if player_colission(player2, player1):
                    player1.y_position -= speed
                    player1.move_speed = speed_limit
        if keys[pygame.K_s]:
            player1.direction = DOWN
            y = (player1.y_position + TILE_SIZE*2)
            if check_move(game_map, (player1.x_position), y) and check_move(game_map, (player1.x_position + TILE_SIZE), y):
                if player_colission(player2, player1):
                    player1.y_position += speed
                    player1.move_speed = speed_limit
        if keys[pygame.K_a]:
            player1.direction = LEFT
            x = (player1.x_position - TILE_SIZE)
            if check_move(game_map, x, player1.y_position) and check_move(game_map, x, (player1.y_position + TILE_SIZE)):
                if player_colission(player2, player1):
                    player1.x_position -= speed
                    player1.move_speed = speed_limit
        if keys[pygame.K_d]:
            player1.direction = RIGHT
            x = (player1.x_position + TILE_SIZE*2)
            if check_move(game_map, x, player1.y_position) and check_move(game_map, x, (player1.y_position + TILE_SIZE)):
                if player_colission(player2, player1):
                    player1.x_position += speed
                    player1.move_speed = speed_limit
    else:
        player1.move_speed -= 1
        
    pass

def check_game_state(player1, player2):
    if player1.health == 0:
        win = "Player 2"
        return win
    if player2.health == 0:
        win = "Player 1"
        return win

def respawn(player):
    spawn = random.randrange(4)
    if spawn == 0:
        player.x_position, player.y_position = 0, TILE_SIZE*2
    if spawn == 1:
        player.x_position, player.y_position = (TILE_SIZE*24), TILE_SIZE*2
    if spawn == 2:
        player.x_position, player.y_position = 0, (TILE_SIZE*22)
    if spawn == 3:
        player.x_position, player.y_position = (TILE_SIZE*24), (TILE_SIZE*22)



def end_screen(game_map, player):
    mouse_coordinates = None
    font = pygame.font.Font('freesansbold.ttf', 30)
    font_big = pygame.font.Font('freesansbold.ttf', 40)
    mouse_coordinates = 0, 0

    while True:
        DISPLAY_SURFACE.fill(BGCOLOR)
        
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEMOTION:
                mouse_coordinates = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_coordinates = event.pos
                mouse_clicked = True
                    
        if mouse_coordinates is not None:
            x, y = mouse_coordinates
                

        if (200 + BUTTON_SIZE) >= x >= 200 and (400 + BUTTON_SIZE) >= y >= 400:
            pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHTCOLOR, (200 - GAP_SIZE / 2, 400 - GAP_SIZE / 2, BUTTON_SIZE + GAP_SIZE, BUTTON_SIZE + GAP_SIZE))
        elif 528 >= x >= (528 - BUTTON_SIZE) and (400 + BUTTON_SIZE) >= y >= 400:
            pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHTCOLOR, (528 - BUTTON_SIZE - GAP_SIZE / 2, 400 - GAP_SIZE / 2, BUTTON_SIZE + GAP_SIZE, BUTTON_SIZE + GAP_SIZE))
                
        pygame.draw.rect(DISPLAY_SURFACE, GREEN, (200, 400, BUTTON_SIZE, BUTTON_SIZE))
        pygame.draw.rect(DISPLAY_SURFACE, RED, (528 - BUTTON_SIZE, 400, BUTTON_SIZE, BUTTON_SIZE))

        text_surface_object = font_big.render("Congratulations, " + player + "!", True, TEXTCOLOR)
        text_rect_object = text_surface_object.get_rect()
        text_rect_object.center = (362, 100)
        DISPLAY_SURFACE.blit(text_surface_object, text_rect_object)
        text_surface_object2 = font_big.render("You won the game!", True, TEXTCOLOR)
        text_rect_object2 = text_surface_object2.get_rect()
        text_rect_object2.center = (362, 200)
        DISPLAY_SURFACE.blit(text_surface_object2, text_rect_object2)
        text_surface_object3 = font_big.render("Would you like to play again?", True, TEXTCOLOR)
        text_rect_object3 = text_surface_object3.get_rect()
        text_rect_object3.center = (362, 300)
        DISPLAY_SURFACE.blit(text_surface_object3, text_rect_object3)

                
        if mouse_clicked:
            x, y = mouse_coordinates 
            if x and y is not None:
                if (200 + BUTTON_SIZE) >= x >= 200 and (400 + BUTTON_SIZE) >= y >= 400:
                    main()
                    return
                elif 528 >= x >= (528 - BUTTON_SIZE) and (400 + BUTTON_SIZE) >= y >= 400:
                    terminate()

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def menu(game_map):
    font = pygame.font.Font('freesansbold.ttf', 30)
    font_big = pygame.font.Font('freesansbold.ttf', 45)
    mouse_coordinates = 0, 0
    while True:
        DISPLAY_SURFACE.fill(BGCOLOR)
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEMOTION:
                mouse_coordinates = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_coordinates = event.pos
                mouse_clicked = True              
        x, y = mouse_coordinates 
        if mouse_clicked:
            file_name = ["board.txt", "Bulanek_factory.txt", "Deadly_garden.txt", "intergalaxial_spaceship.txt", "Mysterious_island.txt", "Secret_laboratory.txt"]
            for number, name in enumerate(file_name):
                if (100 + 528) >= x >= 100 and (250 - (BUTTON_SIZE / 2) + (number * (GAP_SIZE + BUTTON_SIZE))) + BUTTON_SIZE >= y >= 250 - (BUTTON_SIZE / 2) + (number * (GAP_SIZE + BUTTON_SIZE)):
                    return name
        
        for number in  range(6):
            if (100 + 528) >= x >= 100 and (250 - (BUTTON_SIZE / 2) + (number * (GAP_SIZE + BUTTON_SIZE))) + BUTTON_SIZE >= y >= 250 - (BUTTON_SIZE / 2) + (number * (GAP_SIZE + BUTTON_SIZE)):
                pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHTCOLOR, (100 -  GAP_SIZE / 2, 250 - (BUTTON_SIZE / 2) + (number * (GAP_SIZE + BUTTON_SIZE)) -  GAP_SIZE / 2, 528 + GAP_SIZE, BUTTON_SIZE + GAP_SIZE))

        """
        if (100 + 528) >= x >= 100 and (250 - (BUTTON_SIZE / 2) + BUTTON_SIZE) >= y >= 250 - (BUTTON_SIZE / 2):
            pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHTCOLOR, (100 -  GAP_SIZE / 4, 250 - (BUTTON_SIZE / 2) -  GAP_SIZE / 4, 528 + GAP_SIZE / 2, BUTTON_SIZE + GAP_SIZE / 2))
        elif (340 + BUTTON_SIZE) >= x >= 340 and (220 + BUTTON_SIZE) >= y >= BUTTON_SIZE:
            pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHTCOLOR, (334, 214, BUTTON_SIZE, BUTTON_SIZE + 12))
        """
        
        text_surface_object = font_big.render("BULANCI,", True, TEXTCOLOR)
        text_rect_object = text_surface_object.get_rect()
        text_rect_object.center = (362, 80)
        DISPLAY_SURFACE.blit(text_surface_object, text_rect_object)
        
        text_surface_object2 = font_big.render("ANEB TANKY V PREVLECENI", True, TEXTCOLOR)
        text_rect_object2 = text_surface_object2.get_rect()
        text_rect_object2.center = (362, 130)
        DISPLAY_SURFACE.blit(text_surface_object2, text_rect_object2)

        text_surface_object3 = font.render("Choose a map:", True, TEXTCOLOR)
        text_rect_object3 = text_surface_object3.get_rect()
        text_rect_object3.center = (362, 190)
        DISPLAY_SURFACE.blit(text_surface_object3, text_rect_object3)        
            
        maps = ["Board", "Bulanek factory", "Deadly garden", "Intergalaxial spaceship", "Mysterious island", "Secret laboratory"]
        for number, name in enumerate(maps):
            pygame.draw.rect(DISPLAY_SURFACE, NAVYBLUE, (100, 250 - (BUTTON_SIZE / 2) + (number * (GAP_SIZE + BUTTON_SIZE)), 528, BUTTON_SIZE))
            text_surface_object = font.render(f"{name}", True, TEXTCOLOR)
            text_rect_object = text_surface_object.get_rect()
            text_rect_object.center = (362, 250 + (number * (GAP_SIZE + BUTTON_SIZE)))
            DISPLAY_SURFACE.blit(text_surface_object, text_rect_object)


        pygame.display.update()
        FPS_CLOCK.tick(FPS)



def terminate():
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()

