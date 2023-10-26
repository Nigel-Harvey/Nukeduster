import pygame
from data import constants


class Tile:
    last_used_tile_num = None
    last_used_tile_coords = None

    def __init__(self, x_coord, y_coord, width, length, colour, hover_colour, reveal_colour, tile_num, tile_num_x, tile_num_y):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.rectangle = pygame.Rect(x_coord, y_coord, width, length)
        self.colour = colour
        self.reveal_colour = reveal_colour
        self.hover_colour = hover_colour
        self.font = pygame.font.Font(None, 36)
        self.hovering = False                   # start without hover active
        self.flagged = False                    # start without tile flagged
        self.revealed = False                   # start without tile revealed 
        self.nuke = False                       # start without the tile being a nuke
        self.adj_nukes = 0                      # start with the value of adja cent nukes being int 0
        self.text = ""                          # start with the text being an empty string
        self.text_colour = constants.BLACK      # start with the text colour being BLACK
        self.tile_num = tile_num                # save tile num (for nuke generation exclusion and Tile instances)
        self.tile_num_x = tile_num_x
        self.tile_num_y = tile_num_y
        # self.img_flag = pygame.image.load("data\\risk_skull_24p.png")
        self.img_flag = pygame.image.load("data\\death_24p.png")
        self.img_nuke = pygame.image.load("data\\nuclear_bomb_24p.png")
        self.is_left_clicked = False
        self.is_right_clicked = False

    def draw(self, screen):
        if self.hovering:
            pygame.draw.rect(screen, self.hover_colour, self.rectangle)
        else:
            pygame.draw.rect(screen, self.colour, self.rectangle)

        # if the tile isn't a nuke
        if self.nuke == 0:
            # set text and colour of text based on the # of adjacent nukes
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

        # renders chosen text
        text_surface = self.font.render(self.text, True, self.text_colour)
        text_rectangle = text_surface.get_rect(center=self.rectangle.center)

        # draw onto the screen
        screen.blit(text_surface, text_rectangle)
        
        # if flagged, put the image of the flag in the tile
        if self.flagged:
            screen.blit(self.img_flag, (self.x_coord, self.y_coord))

        # if a nuke that isn't flagged and is revealed, put the image of the nuke in the tile
        if self.nuke and self.revealed and not self.flagged:
            screen.blit(self.img_nuke, (self.x_coord, self.y_coord))

    def handle_tile_event(self, event):
        # if the mouse cursor moves
        if event.type == pygame.MOUSEMOTION:
            # set hovering to True if the mouse curser is within the tile coordinates
            self.hovering = self.rectangle.collidepoint(event.pos)
        
        # if a mouse button is clicked and the mouse button was a left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rectangle.collidepoint(event.pos):
                # set left clicked variable for other files to access
                self.is_left_clicked = True

        # if a mouse button is clicked and the mouse button was a right click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.rectangle.collidepoint(event.pos):
                # set left clicked variable for other files to access
                self.is_right_clicked = True
