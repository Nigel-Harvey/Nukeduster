# Auther:   Nigel Harvey
# Purpose:  Be the runnable file that will create a window in which the user can play minesweeper 
#           using their mouse with the GUI to click and navigate through the game

import pygame
import sys
from data import constants

screen_state = constants.MENU

def change_state(new_state):
    global screen_state
    screen_state = new_state

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


def difficulty_easy_action():
    print("Easy Mode selected")
    change_state(constants.EASY)
    # pygame.display.set_mode((constants.EASY_WIDTH, constants.EASY_LENGTH))

def difficulty_medium_action():
    print("Medium Mode is not available yet")
    # global screen_state
    # screen_state = constants.MEDIUM
    # pygame.display.set_mode((constants.MEDIUM_WIDTH, constants.MEDIUM_LENGTH))

def difficulty_hard_action():
    print("Hard Mode is not available yet")
    # global screen_state
    # screen_state = constants.HARD
    # pygame.display.set_mode((constants.HARD_WIDTH, constants.HARD_LENGTH))

def quit_action():
    pygame.quit()
    sys.exit()


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


class MenuScreen:
    def __init__(self, screen_type):
        self.screen_type = screen_type
        # create UI elements for the menu screen
        self.button_list = []
        self.but_difficulty_easy =   Button(100, 675, 100, 50, "Easy", constants.WHITE, constants.GREY, difficulty_easy_action)
        self.but_difficulty_medium = Button(250, 675, 100, 50, "Medium", constants.WHITE, constants.GREY, difficulty_medium_action)
        self.but_difficulty_hard =   Button(400, 675, 100, 50, "Hard", constants.WHITE, constants.GREY, difficulty_hard_action)
        self.but_quit =              Button(530, 760, 60, 30, "Quit", constants.WHITE, constants.GREY, quit_action)
        self.txt_welcome =           TextBox(200, 50, "Welcome to", 50, constants.WHITE)
        self.txt_nuke_duster =       TextBox(200, 100, "Nukeduster", 64)

        self.txt_welcome.set_position((constants.MENU_WIDTH - self.txt_welcome.width) / 2, 50)
        self.txt_nuke_duster.set_position((constants.MENU_WIDTH - 240) / 2, 100)
        
        self.img_nuke = pygame.image.load("Minesweeper\data\\nuclear-bomb.png")

        self.button_list += self.but_difficulty_easy, self.but_difficulty_medium, self.but_difficulty_hard, self.but_quit

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
    # 9x9 tiles
    # 10 bombs
    def __init__(self, screen_type):
        self.screen_type = screen_type


        # load in game data and set clock to 0


        # wait for first click, then start the clock

    def update(self):
        pass

    def draw(self):
        pass

class MediumScreen:
    def __init__(self, screen_type):
        self.screen_type = screen_type

    def update(self):
        pass

    def draw(self):
        pass

class HardScreen:
    def __init__(self, screen_type):
        self.screen_type = screen_type

    def update(self):
        pass

    def draw(self):
        pass





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