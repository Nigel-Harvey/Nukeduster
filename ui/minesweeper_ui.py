# Auther:   Nigel Harvey
# Purpose:  Module that will create the game window in which the user can play minesweeper 
#           using their mouse with the GUI to click and navigate through the game

import pygame
import sys
from data import constants
from logic import minesweeper_logic as logic


global screen_state
screen_state = constants.MENU

def change_screen_state(new_state):
    global screen_state
    screen_state = new_state


global game_state
game_state = constants.WAITING  # start with game-state = 0, which is waiting mode

def change_game_state(new_state):
    global game_state
    game_state = new_state


class Button:
    def __init__(self, x_coord, y_coord, width, length, text, colour, hover_colour, action):
        self.rectangle =    pygame.Rect(x_coord, y_coord, width, length)
        self.text =         text
        self.colour =       colour
        self.hover_colour = hover_colour
        self.action =       action
        self.font =         pygame.font.Font(None, 36)
        self.hovering =     False

    def draw(self, screen):
        if self.hovering:
            pygame.draw.rect(screen, self.hover_colour, self.rectangle)
        else:
            pygame.draw.rect(screen, self.colour, self.rectangle)
        text_surface = self.font.render(self.text, True, constants.BLACK)
        text_rectangle = text_surface.get_rect(center=self.rectangle.center)
        screen.blit(text_surface, text_rectangle)

    def handle_event(self, event):
        # if the mouse cursor moves
        if event.type == pygame.MOUSEMOTION:
            # set hovering to True if the mouse curser is within the buttons coordinates
            self.hovering = self.rectangle.collidepoint(event.pos)
        
        # if a mouse button is clicked and the mousebutton was a left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rectangle.collidepoint(event.pos):
                self.action()


# define all the actions that differnent buttons have
def difficulty_easy_action():
    print("Easy Mode selected")
    change_screen_state(constants.EASY)
    pygame.display.set_mode((constants.EASY_WIDTH, constants.EASY_LENGTH))

def difficulty_medium_action():
    print("Medium Mode is not available yet")
    change_screen_state(constants.MEDIUM)
    pygame.display.set_mode((constants.MEDIUM_WIDTH, constants.MEDIUM_LENGTH))

def difficulty_hard_action():
    print("Hard Mode is not available yet")
    change_screen_state(constants.HARD)
    pygame.display.set_mode((constants.HARD_WIDTH, constants.HARD_LENGTH))

def quit_action():
    pygame.quit()
    sys.exit()

def reset_action():
    print("This button resets the game board")
    global game_state
    game_state = constants.RESET

def menu_action():
    print("Returning to menu")
    change_screen_state(constants.MENU)
    pygame.display.set_mode((constants.MENU_WIDTH, constants.MENU_LENGTH))

    # reset of the player goes from the game to the menu
    reset_action()


class Tile:
    last_used_tile_num = None
    last_used_tile_coords = None
    def __init__(self, x_coord, y_coord, width, length, colour, hover_colour, tile_num, tile_num_x, tile_num_y):
        self.rectangle =    pygame.Rect(x_coord, y_coord, width, length)
        self.colour =       colour
        self.hover_colour = hover_colour
        self.font =         pygame.font.Font(None, 36)
        self.hovering =     False               # start without hover active
        self.flagged =      False               # start without tile flagged
        self.revealed =     False               # start without tile revealed 
        self.nuke =         False               # start without the tile being a nuke
        self.adj_nukes =    0                   # start with the value of adjecent nukes being int 0
        self.text =         ""                  # start with the text being an empty string
        self.text_colour =  constants.BLACK     # start with the text colour being BLACK
        self.tile_num =     tile_num            # save tile num (need tile_num for bomb generation exclusion and referencing Tile instances)
        self.tile_num_x =   tile_num_x
        self.tile_num_y =   tile_num_y
        self.img_flag = pygame.image.load("data\\risk_skull_24p.png")
        # self.img_flag = pygame.image.load("data\\death_24p.png")
        self.img_nuke = pygame.image.load("data\\nuclear_bomb_24p.png")

    def draw(self, screen):
        if self.hovering:
            pygame.draw.rect(screen, self.hover_colour, self.rectangle)
        else:
            pygame.draw.rect(screen, self.colour, self.rectangle)

        # if the tile isn't a nuke
        if self.nuke == 0:
            # set text and colour of text based on the # of adject nukes
            match self.adj_nukes:
                case 1:
                    self.text_colour = constants.BLUE
                    self.text = "1"
                case 2:
                    self.text_colour = constants.RED
                    self.text = "2"
                case 3:
                    self.text_colour = constants.GREEN
                    self.text = "3"
                case 4:
                    self.text_colour = constants.ORANGE
                    self.text = "4"
                case 5:
                    self.text_colour = constants.PINK
                    self.text = "5"
                case 6:
                    self.text_colour = constants.BLUE_LIGHT
                    self.text = "6"
                case 7:
                    self.text_colour = constants.GREEN_DARK
                    self.text = "7"
                case 8:
                    self.text_colour = constants.PURPLE
                    self.text = "8"

        text_surface = self.font.render(self.text, True, self.text_colour)
        text_rectangle = text_surface.get_rect(center=self.rectangle.center)
        screen.blit(text_surface, text_rectangle)
        
        # if flagged, put the image of the flag in the tile
        if self.flagged:
            x = self.tile_num_x*(constants.TILE_WIDTH + constants.SPACE_BETWEEN_TILES) + 2
            y = self.tile_num_y*(constants.TILE_WIDTH + constants.SPACE_BETWEEN_TILES) + 2 + 45
            screen.blit(self.img_flag, (x, y))

        # if a nuke that isn't flagged and is revealed, put the image of the nuke in the tile
        if self.nuke and self.revealed and not self.flagged:
            x = self.tile_num_x*(constants.TILE_WIDTH + constants.SPACE_BETWEEN_TILES) + 2
            y = self.tile_num_y*(constants.TILE_WIDTH + constants.SPACE_BETWEEN_TILES) + 2 + 45
            screen.blit(self.img_nuke, (x, y))

    def handle_event(self, event):
        # if the mouse cursor moves
        if event.type == pygame.MOUSEMOTION:
            # set hovering to True if the mouse curser is within the tile coordinates
            self.hovering = self.rectangle.collidepoint(event.pos)
        
        # if a mouse button is clicked and the mousebutton was a left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rectangle.collidepoint(event.pos):
                # run through logic to see if the tile_reveal function should be called
                global game_state
                if logic.left_click(self.revealed, self.flagged, game_state):
                    # if the game is in WAITING (hasn't begun) then set it to INITIATING after the first left click on a tile
                    if game_state == constants.WAITING:
                        game_state = constants.INITIATING
                    # Set the previously clicked tile. This affects tiles being revealed and prevents multiple reveals of the same tile
                    Tile.last_used_tile_num = self.tile_num
                    Tile.last_used_tile_coords = self.tile_num_x, self.tile_num_y

        # if a mouse button is clicked and the mousebutton was a right click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.rectangle.collidepoint(event.pos):
                if logic.right_click(self.revealed, game_state):
                    # toggle the flag
                    self.flagged = not self.flagged


class TextBox:
    def __init__(self, width, length, text, font_size=24, colour=constants.BLACK):
        self.width = width
        self.length = length
        self.rect = None
        self.text = text
        self.font = pygame.font.Font(None, font_size)  # You can specify a font file or use None for default font
        self.color = colour

    def set_position(self, x_coord, y_coord):
        self.rect = pygame.Rect(x_coord, y_coord, self.width, self.length)

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.rect.topleft)


# class Screen:

#     def __init__(self):
#         self.


class MenuScreen:
    def __init__(self, screen_type):
        self.screen_type = screen_type
        # create UI elements for the menu screen
        self.button_list = []
        self.but_difficulty_easy =   Button(100, 690, 100, 50, "Easy", constants.WHITE, constants.GREY, difficulty_easy_action)
        self.but_difficulty_medium = Button(250, 690, 100, 50, "Medium", constants.WHITE, constants.GREY, difficulty_medium_action)
        self.but_difficulty_hard =   Button(400, 690, 100, 50, "Hard", constants.WHITE, constants.GREY, difficulty_hard_action)
        self.but_quit =              Button(530, 760, 60, 30, "Quit", constants.WHITE, constants.GREY, quit_action)
        self.button_list += self.but_difficulty_easy, self.but_difficulty_medium, self.but_difficulty_hard, self.but_quit
        self.txt_welcome =           TextBox(200, 25, "Welcome to", 50, constants.WHITE)
        self.txt_nuke_duster =       TextBox(200, 75, "Nukeduster", 64)
        self.txt_welcome.set_position((constants.MENU_WIDTH - self.txt_welcome.width) / 2, 35)
        self.txt_nuke_duster.set_position((constants.MENU_WIDTH - 240) / 2, 85)
        
        self.img_nuke = pygame.image.load("data\\nuclear_bomb_big.png")

    def draw(self, game_screen):
        game_screen.fill(constants.PURPLE)           # sets the screen fill and overwrites other things
        self.but_difficulty_easy.draw(game_screen)
        self.but_difficulty_medium.draw(game_screen)
        self.but_difficulty_hard.draw(game_screen)
        self.but_quit.draw(game_screen)
        self.txt_welcome.draw(game_screen)
        self.txt_nuke_duster.draw(game_screen)
        game_screen.blit(self.img_nuke, (45, 150))


class EasyScreen:
    def __init__(self, screen_type):
        self.screen_type = screen_type
        # create UI elements for the menu screen
        self.button_list = []
        self.but_menu =     Button(10, constants.EASY_LENGTH - (30 + 10), 80, 30, "Menu", constants.WHITE, constants.GREY, menu_action)
        self.but_quit =     Button(constants.EASY_WIDTH - (80 + 10), constants.EASY_LENGTH - (30 + 10), 80, 30, "Quit", constants.WHITE, constants.GREY, quit_action)
        self.but_reset =    Button(constants.EASY_WIDTH/2 - 40, 10, 80, 30, "Reset", constants.WHITE, constants.GREY, reset_action)
        self.button_list += self.but_menu, self.but_quit, self.but_reset
        
        self.grid_width = constants.EASY_GRID_WIDTH
        self.grid_length = constants.EASY_GRID_LENGTH
        self.nukes = constants.EASY_NUKES
        self.revealed_safe = 0

        self.txt_game_result = TextBox(80, 30, "", 36, constants.WHITE)
        # TODO set this position
        self.txt_game_result.set_position(constants.EASY_WIDTH/2 - self.txt_game_result.length + 5, constants.EASY_LENGTH - (30 + 10))

        self.tile_list = tile_generation(self.grid_width, self.grid_length, 0, 45)
        # load in game data and set clock to 0
        # wait for first click, then start the clock

    def draw(self, game_screen):
        game_screen.fill(constants.GREEN_DARK)           # sets the screen fill and overwrites other things
        for button in self.button_list:
            button.draw(game_screen)
        for row in self.tile_list:
            for tile in row:
                tile.draw(game_screen)
        self.txt_game_result.draw(game_screen)


class MediumScreen:
    def __init__(self, screen_type):
        self.screen_type = screen_type
        # create UI elements for the menu screen
        self.button_list = []
        self.but_menu =              Button(10, constants.MEDIUM_LENGTH - (30 + 10), 80, 30, "Menu", constants.WHITE, constants.GREY, menu_action)
        self.but_quit =              Button(constants.MEDIUM_WIDTH - (80 + 10), constants.MEDIUM_LENGTH - (30 + 10), 80, 30, "Quit", constants.WHITE, constants.GREY, quit_action)
        self.button_list += self.but_menu, self.but_quit

        self.tile_list = tile_generation(constants.MEDIUM_GRID_WIDTH, constants.MEDIUM_GRID_LENGTH, 0, 45)

        self.game_state =   constants.WAITING  # start with game-state = 0, which is waiting mode


    def draw(self, game_screen):
        game_screen.fill(constants.ORANGE)           # sets the screen fill and overwrites other things
        self.but_menu.draw(game_screen)
        self.but_quit.draw(game_screen)
        for row in self.tile_list:
            for tile in row:
                type(tile)
                tile.draw(game_screen)


class HardScreen:
    def __init__(self, screen_type):
        self.screen_type = screen_type
        # create UI elements for the menu screen
        self.button_list = []
        self.but_menu =              Button(10, constants.HARD_LENGTH - (30 + 10), 80, 30, "Menu", constants.WHITE, constants.GREY, menu_action)
        self.but_quit =              Button(constants.HARD_WIDTH - (80 + 10), constants.HARD_LENGTH - (30 + 10), 80, 30, "Quit", constants.WHITE, constants.GREY, quit_action)
        self.button_list += self.but_menu, self.but_quit
        self.game_state =   constants.WAITING       # start with game-state = 0, which is waiting mode
        self.tile_list = tile_generation(constants.HARD_GRID_WIDTH, constants.HARD_GRID_LENGTH, 0, 45)

    def draw(self, game_screen):
        game_screen.fill(constants.RED)           # sets the screen fill and overwrites other things
        self.but_menu.draw(game_screen)
        self.but_quit.draw(game_screen)
        for row in self.tile_list:
            for tile in row:
                type(tile)
                tile.draw(game_screen)


def tile_generation(x_tiles, y_tiles, x_coord_offset=0, y_coord_offset=0):
    # generate a 2D list to store all the tile objects
    tile_list = [[0 for i in range(y_tiles)] for j in range(x_tiles)]
    
    # generate all the tile objects
    y_coord = constants.SPACE_BETWEEN_TILES + y_coord_offset            # init the y coordinate with an offset of 2 pixels + a set offset purely for visuals
    for row in range(y_tiles):              # loop through all rows, which are represented by y
        x_coord = constants.SPACE_BETWEEN_TILES + x_coord_offset        # init the x coordinate with an offset of 2 pixels + a set offset purely for visuals
        for column in range(x_tiles):       # loop through all columns, which are represented by x
            # store a Tile instance in the tile_list  list at the correct indexes 
            tile_list[column][row] = Tile(x_coord, y_coord, 25, 25, constants.GREY, constants.GREY_LIGHT, (column + row*y_tiles), column, row)
            x_coord += constants.SPACE_BETWEEN_TILES + constants.TILE_WIDTH     # increase the x coordinate so that tiles don't overlap
        y_coord += constants.SPACE_BETWEEN_TILES + constants.TILE_WIDTH         # increase the y coordinate so that tiles don't overlap
    return tile_list

# TODO Keep this around for scoreboard implementation
# class TextInputBox:
#     def __init__(self, x_coord, y_coord, width, length):
#         self.rectangle = pygame.Rect(x_coord, y_coord, width, length)
#         self.text = ""
#         self.font = pygame.font.Font(None, 32)
#         self.active = False

#     def draw(self, screen):
#         color = pygame.Color('dodgerblue2' if self.active else 'dodgerblue1')
#         pygame.draw.rect(screen, color, self.rectangle, 2)
#         text_surface = self.font.render(self.text, True, constants.BLACK)
#         # might need x not x_coord
#         screen.blit(text_surface, (self.rectangle.x_coord + 5, self.rectangle.y_coord + 5))

#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             if self.rectangle.collidepoint(event.pos):
#                 self.active = not self.active
#             else:
#                 self.active = False
#         if self.active:
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     # Perform an action when Enter is pressed, e.g., submit the text
#                     print("Submitted:", self.text)
#                 elif event.key == pygame.K_BACKSPACE:
#                     # Handle backspace key to delete characters
#                     self.text = self.text[:-1]
#                 else:
#                     self.text += event.unicode